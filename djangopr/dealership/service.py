from django.db.models import Q

from dealership.models import (
    Customer,
    Dealership,
    DealershipCars,
    DealershipCustomerSales,
    DealershipUniqueCustomers,
)


def check_orders():
    customers_with_orders = Customer.objects.exclude(order__max_price="").order_by(
        "-updated_at"
    )
    if customers_with_orders is None:
        return
    for customer in customers_with_orders:
        buy_car(customer, customer.order)
        customer.order["max_price"] = ""
        customer.order["car_model"] = ""
        customer.save()


def buy_car(customer, order):
    cheapest_car = (
        DealershipCars.objects.filter(
            Q(car__model=order["car_model"])
            & Q(price__lte=float(order["max_price"]))
            & Q(quantity__gt=0)
        )
        .order_by("price")
        .first()
    )

    if cheapest_car is None:
        return

    cheapest_car.quantity -= 1
    cheapest_car.save()

    dealership = Dealership.objects.get(pk=cheapest_car.dealership_id)
    dealership.balance += cheapest_car.price
    dealership.save()

    customer.balance -= cheapest_car.price
    customer.save()

    add_dealership_customer_history(
        dealership, customer, cheapest_car.car, cheapest_car.price
    )
    add_dealership_customers(dealership, customer)


def add_dealership_customer_history(dealership, customer, car, price):
    DealershipCustomerSales.objects.create(
        dealership=dealership, customer=customer, car=car, price=price
    )


def add_dealership_customers(dealership, customer):
    obj, created = DealershipUniqueCustomers.objects.get_or_create(
        dealership=dealership,
        customer=customer,
        defaults={"number_of_purchases": 0},
    )
    obj.number_of_purchases += 1
    obj.save()
