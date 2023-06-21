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
)
from dealership.models import Supplier, SupplierDiscount
from users.models import User


class SupplierApiTestCase(APITestCase):
    def login(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="test")
        self.client = APIClient()
        self.supplier = SupplierFactory(company_name="Test Supplier 1")
        self.supplier.user = self.user
        self.customers = SupplierUniqueCustomersFactory(supplier=self.supplier)
        self.history = SupplierDealershipSalesFactory(supplier=self.supplier)

    def test_get_suppliers(self):
        url = reverse("supplier-list")
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(Supplier.objects.count(), 1)

    def test_get_supplier(self):
        supplier = Supplier.objects.get()
        url = reverse("supplier-detail", kwargs={"pk": supplier.id})
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(Supplier.objects.count(), 1)

    def test_update_supplier(self):
        supplier = Supplier.objects.get()
        url = reverse("supplier-detail", kwargs={"pk": supplier.id})

        updated_data = {
            "company_name": "Test Supplier 2",
        }
        response = self.client.put(url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client = self.login()
        response = client.put(url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Supplier.objects.get().company_name, "Test Supplier 2")

    def test_delete_supplier(self):
        supplier = Supplier.objects.get()
        url = reverse("supplier-detail", kwargs={"pk": supplier.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client = self.login()
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Supplier.objects.count(), 0)

    def test_get_supplier_customers(self):
        supplier = Supplier.objects.get()
        url = reverse("supplier-customers", kwargs={"pk": supplier.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        client = self.login()
        response = client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_supplier_history(self):
        supplier = Supplier.objects.get()
        url = reverse("supplier-history", kwargs={"pk": supplier.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        client = self.login()
        response = client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class SupplierDiscountApiTestCase(APITestCase):
    def login(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="test")
        self.client = APIClient()
        self.supplier = SupplierDiscountFactory(name="Test Discount")
        self.supplier.user = self.user

    def test_get_discounts(self):
        url = reverse("supplierdiscount-list")
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(SupplierDiscount.objects.count(), 1)

    def test_get_discount(self):
        discount = Supplier.objects.get()
        url = reverse("supplierdiscount-detail", kwargs={"pk": discount.id})
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(SupplierDiscount.objects.count(), 1)

    def test_create_discount(self):
        url = reverse("supplierdiscount-list")
        data = {
            "name": "Test Discount 2",
            "description": "Test Description",
            "supplier": "1",
            "car": "1",
            "start_date": timezone.now(),
            "end_date": timezone.now() + timedelta(days=1),
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client = self.login()
        response = client.post(url, data, format="json")
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(SupplierDiscount.objects.count(), 2)

    def test_update_discount(self):
        discount = SupplierDiscount.objects.get()
        url = reverse("supplierdiscount-detail", kwargs={"pk": discount.id})

        updated_data = {
            "name": "Test Discount 2",
            "description": "Test Description",
            "supplier": "1",
            "car": "1",
            "start_date": timezone.now(),
            "end_date": timezone.now() + timedelta(days=1),
        }
        response = self.client.put(url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client = self.login()
        response = client.put(url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SupplierDiscount.objects.get().name, "Test Discount 2")

    def test_delete_discount(self):
        discount = SupplierDiscount.objects.get()
        url = reverse("supplierdiscount-detail", kwargs={"pk": discount.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client = self.login()
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SupplierDiscount.objects.count(), 0)
