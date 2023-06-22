from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from dealership.factory import (
    DealershipFactory,
    DealershipDiscountFactory,
    DealershipCustomerSalesFactory,
    DealershipUniqueCustomersFactory,
    SupplierDealershipSalesFactory,
)
from dealership.models import Dealership, DealershipDiscount
from users.models import User

DEALERSHIP_ENDPOINT = "/api/v1/dealership/"
DEALERSHIP_DISCOUNT_ENDPOINT = "/api/v1/discount_dealership/"
class DealershipApiTestCase(APITestCase):
    def get_authorized_client(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="test")
        self.unauthorized_client = APIClient()
        self.dealership = DealershipFactory(company_name="Test Dealer 1")
        self.dealership.user = self.user
        self.customers = DealershipUniqueCustomersFactory(dealership=self.dealership)
        self.history_customer = DealershipCustomerSalesFactory(
            dealership=self.dealership
        )
        self.history_supplier = SupplierDealershipSalesFactory(
            dealership=self.dealership
        )

    def test_get_dealerships(self):
        response = self.unauthorized_client.get(f'{DEALERSHIP_ENDPOINT}')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 1)

    def test_get_dealership(self):
        response = self.unauthorized_client.get(f'{DEALERSHIP_ENDPOINT}{self.dealership.pk}/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['company_name'], self.dealership.company_name)

    def test_update_dealership(self):
        expected_data = {
            "company_name": "Test Dealer 2",
            "location": "GB",
        }
        response = self.unauthorized_client.put(f'{DEALERSHIP_ENDPOINT}{self.dealership.pk}/', expected_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client = self.get_authorized_client()
        response = client.put(f'{DEALERSHIP_ENDPOINT}{self.dealership.pk}/', expected_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['company_name'], expected_data['company_name'])

        self.dealership.refresh_from_db()
        self.assertEqual(response.data['company_name'], self.dealership.company_name)

    def test_delete_dealership(self):
        response = self.unauthorized_client.delete(f'{DEALERSHIP_ENDPOINT}{self.dealership.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client = self.get_authorized_client()
        response = client.delete(f'{DEALERSHIP_ENDPOINT}{self.dealership.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.dealership.refresh_from_db()
        response = client.get(f'{DEALERSHIP_ENDPOINT}')
        self.assertEquals(len(response.data), 0)

    def test_get_dealership_customers(self):
        response = self.unauthorized_client.get(f'{DEALERSHIP_ENDPOINT}{self.dealership.pk}/customers/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        client = self.get_authorized_client()
        response = client.get(f'{DEALERSHIP_ENDPOINT}{self.dealership.pk}/customers/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_dealership_customer_history(self):
        response = self.unauthorized_client.get(f'{DEALERSHIP_ENDPOINT}{self.dealership.pk}/history_customers/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        client = self.get_authorized_client()
        response = client.get(f'{DEALERSHIP_ENDPOINT}{self.dealership.pk}/history_customers/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_dealership_supplier_history(self):
        response = self.unauthorized_client.get(f'{DEALERSHIP_ENDPOINT}{self.dealership.pk}/history_suppliers/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        client = self.get_authorized_client()
        response = client.get(f'{DEALERSHIP_ENDPOINT}{self.dealership.pk}/history_suppliers/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DealershipDiscountApiTestCase(APITestCase):
    def get_authorized_client(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="test")
        self.unauthorized_client = APIClient()
        self.discount = DealershipDiscountFactory(name="Test Discount 1")
        self.discount.user = self.user

    def test_get_discounts(self):
        response = self.unauthorized_client.get(f'{DEALERSHIP_DISCOUNT_ENDPOINT}')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 1)

    def test_get_discount(self):
        response = self.unauthorized_client.get(f'{DEALERSHIP_DISCOUNT_ENDPOINT}{self.discount.pk}/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['name'], self.discount.name)

    def test_create_discount(self):
        expected_data = {
            "name": "Test Discount 2",
            "description": "Test Description",
            "dealership": "1",
            "car": "1",
            "start_date": timezone.now(),
            "end_date": timezone.now() + timedelta(days=1),
        }
        response = self.unauthorized_client.post(f'{DEALERSHIP_DISCOUNT_ENDPOINT}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client = self.get_authorized_client()
        response = client.post(f'{DEALERSHIP_DISCOUNT_ENDPOINT}', expected_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data['name'], expected_data['name'])

        self.discount.refresh_from_db()
        response = client.get(f'{DEALERSHIP_DISCOUNT_ENDPOINT}')
        self.assertEquals(len(response.data), 2)

    def test_update_discount(self):
        expected_data = {
            "name": "Test Discount 2",
            "description": "Test Description",
            "dealership": "1",
            "car": "1",
            "start_date": timezone.now(),
            "end_date": timezone.now() + timedelta(days=1),
        }
        response = self.unauthorized_client.put(f'{DEALERSHIP_DISCOUNT_ENDPOINT}{self.discount.pk}/', expected_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client = self.get_authorized_client()
        response = client.put(f'{DEALERSHIP_DISCOUNT_ENDPOINT}{self.discount.pk}/', expected_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], expected_data['name'])

        self.discount.refresh_from_db()
        self.assertEqual(response.data['name'], self.discount.name)

    def test_delete_discount(self):
        response = self.unauthorized_client.delete(f'{DEALERSHIP_DISCOUNT_ENDPOINT}{self.discount.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client = self.get_authorized_client()
        response = client.delete(f'{DEALERSHIP_DISCOUNT_ENDPOINT}{self.discount.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.discount.refresh_from_db()
        response = client.get(f'{DEALERSHIP_DISCOUNT_ENDPOINT}')
        self.assertEquals(len(response.data), 0)
