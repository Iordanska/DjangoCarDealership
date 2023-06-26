from _decimal import Decimal
from django_filters.compat import TestCase

from dealership.celery_fulfill_orders import check_orders
from dealership.factory import (
    CarFactory,
    CustomerFactory,
    DealershipCarsFactory,
    DealershipDiscountFactory,
    DealershipFactory,
)
from dealership.models import (
    DealershipCustomerSales,
    DealershipUniqueCustomers,
)


class FulfillOrdersTestCase(TestCase):
    def setUp(self):
        self.customer = CustomerFactory(
            balance=10000, order__max_price="9000", order__car_model="Reno"
        )
        self.car = CarFactory(model="Reno")
        self.dealership = DealershipFactory(balance=20000)
        self.dealership_cars = DealershipCarsFactory(
            dealership=self.dealership, car=self.car, price=7000, quantity=2
        )
        self.dealership_discount = DealershipDiscountFactory(
            dealership=self.dealership, car=self.car, percent=50
        )

    def test_check_orders(self):
        check_orders()
        self.dealership.refresh_from_db()
        self.dealership_cars.refresh_from_db()
        self.customer.refresh_from_db()

        self.assertEqual(self.customer.balance.amount, Decimal(6500))
        self.assertEqual(self.customer.order["max_price"], "")
        self.assertEqual(self.customer.order["car_model"], "")
        self.assertEqual(self.dealership.balance.amount, Decimal(23500))
        self.assertEqual(self.dealership_cars.quantity, 1)

        history = DealershipCustomerSales.objects.get(dealership=self.dealership)
        self.assertEqual(history.customer, self.customer)
        self.assertEqual(history.car, self.car)
        self.assertEqual(history.price.amount, Decimal(3500))

        unique_customers = DealershipUniqueCustomers.objects.get(
            dealership=self.dealership, customer=self.customer
        )
        self.assertEqual(unique_customers.id, self.customer.id)
        self.assertEqual(unique_customers.number_of_purchases, 1)
