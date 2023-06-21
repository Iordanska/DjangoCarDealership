from _decimal import Decimal
from django_filters.compat import TestCase

from dealership.celery_dealership_buy_cars import dealership_buy_cars
from dealership.factory import (
    CarFactory,
    DealershipFactory,
    SupplierCarsFactory,
    SupplierDiscountFactory,
    SupplierFactory,
)
from dealership.models import (
    Dealership,
    DealershipCars,
    Supplier,
    SupplierDealershipSales,
    SupplierUniqueCustomers,
)


class DealershipBuyCars(TestCase):
    def setUp(self):
        self.dealership = DealershipFactory(
            balance=17500,
            specification__transmission="automatic",
            specification__fuel="diesel",
        )
        self.dealership.specification["transmission"] = "automatic"
        self.dealership.specification["fuel"] = "diesel"
        self.car = CarFactory(model="Volga", transmission="automatic", fuel="diesel")
        self.supplier = SupplierFactory()
        self.supplier.discount = {
            4: 10,
        }
        self.supplier_cars = SupplierCarsFactory(
            supplier=self.supplier, car=self.car, price=7000
        )
        self.supplier_discount = SupplierDiscountFactory(
            supplier=self.supplier, car=self.car, percent=50
        )

    def test_dealership_buy_cars(self):
        dealership_buy_cars()
        dealership = Dealership.objects.get(id=1)
        supplier = Supplier.objects.get(id=1)
        dealership_cars = DealershipCars.objects.get(id=1)
        self.assertEqual(dealership.balance.amount, Decimal(0))
        self.assertEqual(dealership_cars.car.model, "Volga")
        self.assertEqual(dealership_cars.quantity, 5)

        history = SupplierDealershipSales.objects.filter(supplier=supplier)
        self.assertEqual(history.count(), 5)
        self.assertEqual(history[0].dealership, self.dealership)
        self.assertEqual(history[0].car, self.car)
        self.assertEqual(history[0].price.amount, Decimal(3500))

        unique_customers = SupplierUniqueCustomers.objects.get(
            supplier=supplier, dealership=dealership
        )
        self.assertEqual(dealership.id, self.dealership.id)
        self.assertEqual(unique_customers.number_of_purchases, 5)

        self.assertEqual(supplier.number_of_buyers, 1)
