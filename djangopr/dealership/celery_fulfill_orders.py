from _decimal import Decimal
from django.db.models import Min, Q, Value
from django.db.models.functions import JSONObject

from dealership.models import (
    Customer,
    Dealership,
    DealershipCars,
    DealershipCustomerSales,
    DealershipDiscount,
    DealershipUniqueCustomers,
)


def check_orders():
    min_car_price = (
        DealershipCars.objects.exclude(price__lte=0)
        .values("price")
        .aggregate(min_price=Min("price"))["min_price"]
    )
    customers_with_orders = Customer.objects.filter(
        ~Q(order__max_price=""), balance__gte=min_car_price
    ).order_by("-updated_at")

    if not customers_with_orders:
        return

    (
        customers_updated,
        dealership_cars_updated,
        dealerships_updated,
        dealership_sales_updated,
    ) = buy_car(customers_with_orders)

    Customer.objects.all().update(
        order=JSONObject(max_price=Value(""), car_model=Value(""))
    )

    Customer.objects.bulk_update(customers_updated, ["balance"])
    DealershipCars.objects.bulk_update(dealership_cars_updated, ["quantity"])
    Dealership.objects.bulk_update(dealerships_updated, ["balance"])
    DealershipCustomerSales.objects.bulk_create(dealership_sales_updated)


def buy_car(customers_with_orders):
    customers_updated = []
    dealership_cars_updated = []
    dealerships_updated = []
    dealership_sales_updated = []

    for customer in customers_with_orders:
        selected_cars = DealershipCars.objects.filter(
            Q(car__model=customer.order["car_model"])
            & Q(price__lte=Decimal(customer.order["max_price"]))
            & Q(quantity__gt=0)
        )

        if not selected_cars:
            continue

        cheapest_car_id, cheapest_car_price = get_cheapest_car(selected_cars)

        cheapest_car = selected_cars.get(pk=cheapest_car_id)

        cheapest_car.quantity -= 1
        dealership_cars_updated.append(cheapest_car)

        dealership = Dealership.objects.get(pk=cheapest_car.dealership_id)
        dealership.balance += cheapest_car_price
        dealerships_updated.append(dealership)

        customer.balance -= cheapest_car_price
        customers_updated.append(customer)

        dealership_sales_updated.append(
            DealershipCustomerSales(
                dealership=dealership,
                customer=customer,
                car=cheapest_car.car,
                price=cheapest_car_price,
            )
        )

        add_dealership_customers(dealership, customer)

    return (
        customers_updated,
        dealership_cars_updated,
        dealerships_updated,
        dealership_sales_updated,
    )


def add_dealership_customers(dealership, customer):
    obj, created = DealershipUniqueCustomers.objects.get_or_create(
        dealership=dealership,
        customer=customer,
        defaults={"number_of_purchases": 0},
    )
    obj.number_of_purchases += 1
    obj.save()


def get_cheapest_car(selected_cars):
    car_price_list = []

    for car in selected_cars:
        discount_price = get_discount_price(car, car.dealership)
        car_price_list.append((car.id, discount_price))

    cheapest_car = sorted(car_price_list, key=lambda car: car[1])[0]
    return cheapest_car


def get_discount_price(car, dealership):
    discount = DealershipDiscount.objects.filter(
        car=car.car, dealership=dealership
    ).first()

    if discount is None:
        return car.price

    discount_price = (
        car.price * (Decimal(100.00) - Decimal(discount.percent)) / Decimal(100.00)
    )
    return discount_price
