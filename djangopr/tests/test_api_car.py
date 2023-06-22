from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from dealership.factory import CarFactory
from users.models import User

CAR_ENDPOINT = "/api/v1/car/"
class CarApiTestCase(APITestCase):
    def get_authorized_client(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="test")
        self.unauthorized_client = APIClient()
        self.car = CarFactory(model="Test Car 1")
        self.car.user = self.user

    def test_get_cars(self):
        response = self.unauthorized_client.get(f'{CAR_ENDPOINT}')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data),1)

    def test_get_car(self):
        response = self.unauthorized_client.get(f'{CAR_ENDPOINT}{self.car.pk}/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['model'], self.car.model)

    def test_create_car(self):

        expected_data = {
            "model": "Test model 2",
            "registration_year": "2000",
        }

        response = self.unauthorized_client.post(f'{CAR_ENDPOINT}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client = self.get_authorized_client()
        response = client.post(f'{CAR_ENDPOINT}', expected_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data['model'], expected_data['model'])

        self.car.refresh_from_db()
        response = client.get(f'{CAR_ENDPOINT}')
        self.assertEquals(len(response.data), 2)

    def test_update_car(self):

        expected_data = {
            "model": "Test model 2",
            "registration_year": "2000",
        }

        response = self.unauthorized_client.put(f'{CAR_ENDPOINT}{self.car.pk}/', expected_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client = self.get_authorized_client()
        response = client.put(f'{CAR_ENDPOINT}{self.car.pk}/',expected_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['model'], expected_data['model'])

        self.car.refresh_from_db()
        self.assertEqual(response.data['model'], self.car.model)


    def test_delete_car(self):
        response = self.unauthorized_client.delete(f'{CAR_ENDPOINT}{self.car.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client = self.get_authorized_client()
        response = client.delete(f'{CAR_ENDPOINT}{self.car.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.car.refresh_from_db()
        response = client.get(f'{CAR_ENDPOINT}')
        self.assertEquals(len(response.data), 0)

