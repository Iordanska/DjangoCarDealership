from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from dealership.factory import DealershipDiscountFactory, SupplierDiscountFactory
from dealership.models import (
    Car,
    Customer,
    Dealership,
    DealershipDiscount,
    Supplier,
    SupplierDiscount,
)
from users.models import User


class CarApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.data = {
            "model": "Test Model 1",
            "registration_year": 2003,
        }
        self.car = Car.objects.create(**self.data)

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Car.objects.get().model, "Test model 2")

    def test_delete_car(self):
        car = Car.objects.get()
        url = reverse("car-detail", kwargs={"pk": car.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Car.objects.count(), 0)


class CustomerApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.data = {
            "name": "Test Name",
            "surname": "Test Surname",
            "country": "GB",
            "user": self.user,
        }
        self.customer = Customer.objects.create(**self.data)

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Customer.objects.get().name, "Test Customer 2")

    def test_delete_customer(self):
        customer = Customer.objects.get()
        url = reverse("customer-detail", kwargs={"pk": customer.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)

    def test_get_history(self):
        customer = Customer.objects.get()
        url = reverse("customer-history", kwargs={"pk": customer.id})
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class DealershipApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.data = {
            "company_name": "Test Dealer 1",
            "location": "GB",
            "user": self.user,
        }
        self.dealership = Dealership.objects.create(**self.data)

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dealership.objects.get().company_name, "Test Dealer 2")

    def test_delete_dealership(self):
        dealership = Dealership.objects.get()
        url = reverse("dealership-detail", kwargs={"pk": dealership.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Dealership.objects.count(), 0)

    def test_get_dealership_customers(self):
        dealership = Dealership.objects.get()
        url = reverse("dealership-customers", kwargs={"pk": dealership.id})
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_dealership_customer_history(self):
        dealership = Dealership.objects.get()
        url = reverse("dealership-history-customers", kwargs={"pk": dealership.id})
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_dealership_supplier_history(self):
        dealership = Dealership.objects.get()
        url = reverse("dealership-history-suppliers", kwargs={"pk": dealership.id})
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class DealershipDiscountApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.dealership = DealershipDiscountFactory(name="Test Discount")

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
        }

        response = self.client.post(url, data, format="json")
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
        }
        response = self.client.put(url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DealershipDiscount.objects.get().name, "Test Discount 2")

    def test_delete_discount(self):
        discount = DealershipDiscount.objects.get()
        url = reverse("dealershipdiscount-detail", kwargs={"pk": discount.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DealershipDiscount.objects.count(), 0)


class SupplierApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.data = {
            "company_name": "Test Supplier 1",
            "user": self.user,
        }
        self.supplier = Supplier.objects.create(**self.data)

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Supplier.objects.get().company_name, "Test Supplier 2")

    def test_delete_supplier(self):
        supplier = Supplier.objects.get()
        url = reverse("supplier-detail", kwargs={"pk": supplier.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Supplier.objects.count(), 0)

    def test_get_supplier_customers(self):
        supplier = Supplier.objects.get()
        url = reverse("supplier-customers", kwargs={"pk": supplier.id})
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_supplier_history(self):
        supplier = Supplier.objects.get()
        url = reverse("supplier-history", kwargs={"pk": supplier.id})
        response = self.client.get(url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class SupplierDiscountApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.supplier = SupplierDiscountFactory(name="Test Discount")

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
        }
        response = self.client.post(url, data, format="json")
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
        }
        response = self.client.put(url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SupplierDiscount.objects.get().name, "Test Discount 2")

    def test_delete_discount(self):
        discount = SupplierDiscount.objects.get()
        url = reverse("supplierdiscount-detail", kwargs={"pk": discount.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SupplierDiscount.objects.count(), 0)
