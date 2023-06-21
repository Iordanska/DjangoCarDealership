from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from dealership.factory import CustomerFactory, DealershipCustomerSalesFactory
from dealership.models import Customer

from users.models import User


class CustomerApiTestCase(APITestCase):
    def login(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username="testuser", password="test")
        self.customer = CustomerFactory(name="Test Name")
        self.customer.user = self.user
        self.history = DealershipCustomerSalesFactory(customer=self.customer)

    def test_get_customers(self):
        url = reverse("customer-list")
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(Customer.objects.count(), 1)

    def test_get_customer(self):
        customer = Customer.objects.get()
        url = reverse("customer-detail", kwargs={"pk": customer.id})
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(Customer.objects.count(), 1)

    def test_update_customer(self):
        customer = Customer.objects.get()
        url = reverse("customer-detail", kwargs={"pk": customer.id})

        updated_data = {
            "name": "Test Customer 2",
            "surname": "Test Surname",
            "country": "GB",
            "order": {"max_price": "", "car_model": ""},
        }

        response = self.client.put(url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client = self.login()
        response = client.put(url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Customer.objects.get().name, "Test Customer 2")

    def test_delete_customer(self):
        customer = Customer.objects.get()
        url = reverse("customer-detail", kwargs={"pk": customer.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client = self.login()
        response = client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)

    def test_get_history(self):
        customer = Customer.objects.get()
        url = reverse("customer-history", kwargs={"pk": customer.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        client = self.login()
        response = client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
