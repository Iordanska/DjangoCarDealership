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


class DealershipApiTestCase(APITestCase):
    def login(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="test")
        self.client = APIClient()
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
        url = reverse("dealership-list")
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(Dealership.objects.count(), 1)

    def test_get_dealership(self):
        dealership = Dealership.objects.get()
        url = reverse("dealership-detail", kwargs={"pk": dealership.id})
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(Dealership.objects.count(), 1)

    def test_update_dealership(self):
        dealership = Dealership.objects.get()
        url = reverse("dealership-detail", kwargs={"pk": dealership.id})

        updated_data = {
            "company_name": "Test Dealer 2",
            "location": "GB",
        }
        response = self.client.put(url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client = self.login()
        response = client.put(url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dealership.objects.get().company_name, "Test Dealer 2")

    def test_delete_dealership(self):
        dealership = Dealership.objects.get()
        url = reverse("dealership-detail", kwargs={"pk": dealership.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client = self.login()
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Dealership.objects.count(), 0)

    def test_get_dealership_customers(self):
        dealership = Dealership.objects.get()
        url = reverse("dealership-customers", kwargs={"pk": dealership.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        client = self.login()
        response = client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_dealership_customer_history(self):
        dealership = Dealership.objects.get()
        url = reverse("dealership-history-customers", kwargs={"pk": dealership.id})

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        client = self.login()
        response = client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_dealership_supplier_history(self):
        dealership = Dealership.objects.get()
        url = reverse("dealership-history-suppliers", kwargs={"pk": dealership.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        client = self.login()
        response = client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class DealershipDiscountApiTestCase(APITestCase):
    def login(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="test")
        self.client = APIClient()
        self.dealership = DealershipDiscountFactory(name="Test Discount 1")
        self.dealership.user = self.user

    def test_get_discounts(self):
        url = reverse("dealershipdiscount-list")
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(DealershipDiscount.objects.count(), 1)

    def test_get_discount(self):
        discount = DealershipDiscount.objects.get()
        url = reverse("dealershipdiscount-detail", kwargs={"pk": discount.id})
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(DealershipDiscount.objects.count(), 1)

    def test_create_discount(self):
        url = reverse("dealershipdiscount-list")
        data = {
            "name": "Test Discount 2",
            "description": "Test Description",
            "dealership": "1",
            "car": "1",
            "start_date": timezone.now(),
            "end_date": timezone.now() + timedelta(days=1),
        }
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client = self.login()
        response = client.post(url, data, format="json")
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(DealershipDiscount.objects.count(), 2)

    def test_update_discount(self):
        discount = DealershipDiscount.objects.get()
        url = reverse("dealershipdiscount-detail", kwargs={"pk": discount.id})

        updated_data = {
            "name": "Test Discount 2",
            "description": "Test Description",
            "dealership": "1",
            "car": "1",
            "start_date": timezone.now(),
            "end_date": timezone.now() + timedelta(days=1),
        }
        response = self.client.put(url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client = self.login()
        response = client.put(url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DealershipDiscount.objects.get().name, "Test Discount 2")

    def test_delete_discount(self):
        discount = DealershipDiscount.objects.get()
        url = reverse("dealershipdiscount-detail", kwargs={"pk": discount.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client = self.login()
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DealershipDiscount.objects.count(), 0)
