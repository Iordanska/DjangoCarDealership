from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from dealership.factory import CarFactory
from dealership.models import Car
from users.models import User


class CarApiTestCase(APITestCase):
    def login(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="test")
        self.client = APIClient()
        self.car = CarFactory(model="Test Car 1")
        self.car.user = self.user

    def test_get_cars(self):
        url = reverse("car-list")
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(Car.objects.count(), 1)

    def test_get_car(self):
        car = Car.objects.get()
        url = reverse("car-detail", kwargs={"pk": car.id})
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(Car.objects.count(), 1)

    def test_create_car(self):
        url = reverse("car-list")
        response = self.client.post(url, self.data, format="json")
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Car.objects.count(), 2)

    def test_update_car(self):
        car = Car.objects.get()
        url = reverse("car-detail", kwargs={"pk": car.id})

        updated_data = {
            "model": "Test model 2",
            "registration_year": "2000",
        }

        response = self.client.put(url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client = self.login()
        response = client.put(url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Car.objects.get().model, "Test model 2")

    def test_delete_car(self):
        car = Car.objects.get()
        url = reverse("car-detail", kwargs={"pk": car.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Car.objects.count(), 0)
