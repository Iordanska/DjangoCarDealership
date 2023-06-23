from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from dealership.factory import (
    SupplierFactory,
    SupplierDiscountFactory,
    SupplierDealershipSalesFactory,
    SupplierUniqueCustomersFactory,
    UserFactory,
)
from users.models import User

SUPPLIER_ENDPOINT = "/api/v1/supplier/"
SUPPLIER_DISCOUNT_ENDPOINT = "/api/v1/discount_supplier/"


class SupplierApiTestCase(APITestCase):
    def get_authorized_client(self):
        client = APIClient()
        client.force_authenticate(user=self.supplier.user)
        return client

    def get_another_user_authorized_client(self):
        client = APIClient()
        client.force_authenticate(user=self.another_user)
        return client

    def setUp(self):
        self.unauthorized_client = APIClient()
        self.supplier = SupplierFactory(company_name="Test Supplier 1")
        self.customers = SupplierUniqueCustomersFactory(supplier=self.supplier)
        self.history = SupplierDealershipSalesFactory(supplier=self.supplier)
        self.another_user = UserFactory(role="dealership")

    def test_get_suppliers(self):
        response = self.unauthorized_client.get(f"{SUPPLIER_ENDPOINT}")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 1)

    def test_get_supplier(self):
        response = self.unauthorized_client.get(
            f"{SUPPLIER_ENDPOINT}{self.supplier.pk}/"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["company_name"], self.supplier.company_name)

    def test_update_supplier(self):
        expected_data = {
            "company_name": "Test Supplier 2",
        }
        response = self.unauthorized_client.put(
            f"{SUPPLIER_ENDPOINT}{self.supplier.pk}/", expected_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client = self.get_another_user_authorized_client()
        response = client.put(
            f"{SUPPLIER_ENDPOINT}{self.supplier.pk}/", expected_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        client = self.get_authorized_client()
        response = client.put(
            f"{SUPPLIER_ENDPOINT}{self.supplier.pk}/", expected_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["company_name"], expected_data["company_name"])

        self.supplier.refresh_from_db()
        self.assertEqual(response.data["company_name"], self.supplier.company_name)

    def test_delete_supplier(self):
        response = self.unauthorized_client.delete(
            f"{SUPPLIER_ENDPOINT}{self.supplier.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client = self.get_another_user_authorized_client()
        response = client.delete(f"{SUPPLIER_ENDPOINT}{self.supplier.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        client = self.get_authorized_client()
        response = client.delete(f"{SUPPLIER_ENDPOINT}{self.supplier.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.supplier.refresh_from_db()
        response = client.get(f"{SUPPLIER_ENDPOINT}")
        self.assertEquals(len(response.data), 0)

    def test_get_supplier_customers(self):
        response = self.unauthorized_client.get(
            f"{SUPPLIER_ENDPOINT}{self.supplier.pk}/customers/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        client = self.get_another_user_authorized_client()
        response = client.get(f"{SUPPLIER_ENDPOINT}{self.supplier.pk}/customers/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        client = self.get_authorized_client()
        incorrect_id = 10
        response = client.get(f"{SUPPLIER_ENDPOINT}{incorrect_id}/customers/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        client = self.get_authorized_client()
        response = client.get(f"{SUPPLIER_ENDPOINT}{self.supplier.pk}/customers/")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_supplier_history(self):
        response = self.unauthorized_client.get(
            f"{SUPPLIER_ENDPOINT}{self.supplier.pk}/history/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        client = self.get_another_user_authorized_client()
        response = client.get(f"{SUPPLIER_ENDPOINT}{self.supplier.pk}/history/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        client = self.get_authorized_client()
        incorrect_id = 10
        response = client.get(f"{SUPPLIER_ENDPOINT}{incorrect_id}/history/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        client = self.get_authorized_client()
        response = client.get(f"{SUPPLIER_ENDPOINT}{self.supplier.pk}/history/")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SupplierDiscountApiTestCase(APITestCase):
    def get_authorized_client(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="test")
        self.unauthorized_client = APIClient()
        self.discount = SupplierDiscountFactory(name="Test Discount 1")
        self.discount.user = self.user

    def test_get_discounts(self):
        response = self.unauthorized_client.get(f"{SUPPLIER_DISCOUNT_ENDPOINT}")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 1)

    def test_get_discount(self):
        response = self.unauthorized_client.get(
            f"{SUPPLIER_DISCOUNT_ENDPOINT}{self.discount.pk}/"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["name"], self.discount.name)

    def test_create_discount(self):
        expected_data = {
            "name": "Test Discount 2",
            "description": "Test Description",
            "supplier": "1",
            "car": "1",
            "start_date": timezone.now(),
            "end_date": timezone.now() + timedelta(days=1),
        }
        response = self.unauthorized_client.post(f"{SUPPLIER_DISCOUNT_ENDPOINT}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client = self.get_authorized_client()
        response = client.post(f"{SUPPLIER_DISCOUNT_ENDPOINT}", expected_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data["name"], expected_data["name"])

        self.discount.refresh_from_db()
        response = client.get(f"{SUPPLIER_DISCOUNT_ENDPOINT}")
        self.assertEquals(len(response.data), 2)

    def test_update_discount(self):
        expected_data = {
            "name": "Test Discount 2",
            "description": "Test Description",
            "supplier": "1",
            "car": "1",
            "start_date": timezone.now(),
            "end_date": timezone.now() + timedelta(days=1),
        }
        response = self.unauthorized_client.put(
            f"{SUPPLIER_DISCOUNT_ENDPOINT}{self.discount.pk}/", expected_data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client = self.get_authorized_client()
        response = client.put(
            f"{SUPPLIER_DISCOUNT_ENDPOINT}{self.discount.pk}/", expected_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], expected_data["name"])

        self.discount.refresh_from_db()
        self.assertEqual(response.data["name"], self.discount.name)

    def test_delete_discount(self):
        response = self.unauthorized_client.delete(
            f"{SUPPLIER_DISCOUNT_ENDPOINT}{self.discount.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client = self.get_authorized_client()
        response = client.delete(f"{SUPPLIER_DISCOUNT_ENDPOINT}{self.discount.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.discount.refresh_from_db()
        response = client.get(f"{SUPPLIER_DISCOUNT_ENDPOINT}")
        self.assertEquals(len(response.data), 0)
