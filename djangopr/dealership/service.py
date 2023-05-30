from django.db.models import Q

from dealership.models import (Customer, Dealership, DealershipCars,
                               DealershipCustomerSales,
                               DealershipUniqueCustomers, Order)


def check_orders():
    orders = Order.objects.all().order_by("-created_at")
    if orders is None:
        return
    for order in orders:
        buy_car(order)
        order.is_active = False
        order.save()


def buy_car(order):
    cheapest_car = (
        DealershipCars.objects.filter(
            Q(car=order.car) & Q(price__lte=order.max_price) & Q(quantity__gt=0)
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

    customer = Customer.objects.get(pk=order.customer_id)
    customer.balance -= cheapest_car.price
    customer.save()

    add_dealership_customer_history(dealership, customer, order.car, cheapest_car.price)
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
