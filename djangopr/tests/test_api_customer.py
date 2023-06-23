from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from dealership.factory import (
    CustomerFactory,
    DealershipCustomerSalesFactory,
    UserFactory,
)
from dealership.models import Customer

from users.models import User

CUSTOMER_ENDPOINT = "/api/v1/customer/"


class CustomerApiTestCase(APITestCase):
    def get_authorized_client(self):
        client = APIClient()
        client.force_authenticate(user=self.customer.user)
        return client

    def get_another_user_authorized_client(self):
        client = APIClient()
        client.force_authenticate(user=self.another_user)
        return client

    def setUp(self):
        self.unauthorized_client = APIClient()
        self.customer = CustomerFactory(name="Test Name")
        self.history = DealershipCustomerSalesFactory(customer=self.customer)
        self.another_user = UserFactory(role="dealership")

    def test_get_customers(self):
        response = self.unauthorized_client.get(f"{CUSTOMER_ENDPOINT}")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 1)

    def test_get_customer(self):
        response = self.unauthorized_client.get(
            f"{CUSTOMER_ENDPOINT}{self.customer.pk}/"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["name"], self.customer.name)

    def test_update_customer(self):
        expected_data = {
            "name": "Test Customer 2",
            "surname": "Test Surname",
            "country": "GB",
            "order": {"max_price": "", "car_model": ""},
        }

        response = self.unauthorized_client.put(
            f"{CUSTOMER_ENDPOINT}{self.customer.pk}/", expected_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client = self.get_another_user_authorized_client()
        response = client.put(
            f"{CUSTOMER_ENDPOINT}{self.customer.pk}/", expected_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        client = self.get_authorized_client()
        response = client.put(
            f"{CUSTOMER_ENDPOINT}{self.customer.pk}/", expected_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], expected_data["name"])

        self.customer.refresh_from_db()
        self.assertEqual(response.data["name"], self.customer.name)

    def test_delete_customer(self):
        response = self.unauthorized_client.delete(
            f"{CUSTOMER_ENDPOINT}{self.customer.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client = self.get_another_user_authorized_client()
        response = client.delete(f"{CUSTOMER_ENDPOINT}{self.customer.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        client = self.get_authorized_client()
        response = client.delete(f"{CUSTOMER_ENDPOINT}{self.customer.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.customer.refresh_from_db()
        response = client.get(f"{CUSTOMER_ENDPOINT}")
        self.assertEquals(len(response.data), 0)

    def test_get_history(self):
        response = self.unauthorized_client.get(
            f"{CUSTOMER_ENDPOINT}{self.customer.pk}/history/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        client = self.get_authorized_client()
        incorrect_id = 10
        response = client.get(f"{CUSTOMER_ENDPOINT}{incorrect_id}/history/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = client.get(f"{CUSTOMER_ENDPOINT}{self.customer.id}/history/")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
