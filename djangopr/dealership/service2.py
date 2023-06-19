from django.db.models import Count, Q

from dealership.models import (
    Car,
    Dealership,
    DealershipCars,
    DealershipCustomerSales,
    SupplierCars,
    SupplierDealershipSales,
    SupplierDiscount,
    SupplierUniqueCustomers,
)


def dealership_buy_cars():
    dealerships = Dealership.objects.all()
    for dealership in dealerships:
        selected_cars = select_cars(dealership)
        buy_cars(dealership, selected_cars)


def select_cars(dealership):
    if dealership.balance == 0:
        return

    q_objects = Q(quantity__gt=0)
    for key, value in dealership.specification.items():
        if value:
            q_objects.add(Q(**{"car" + "__" + key: value}), Q.AND)

    selected_cars = SupplierCars.objects.filter(q_objects)

    # Цена с учёток скидок
    car_price_list = get_discount_pricelist(dealership, selected_cars)
    # сортировка по новой цене
    car_list_sorted = sorted(car_price_list, key=lambda tup: tup[1])
    return car_list_sorted


#
#
def buy_cars(dealership, car_list_sorted):
    if car_list_sorted is None:
        return

    for obj in car_list_sorted:
        id = SupplierCars.objects.get(pk=obj[0])
        price = obj[1]

        while dealership.balance.amount >= price:
            change_balance(dealership, price)
            add_car(id.car, dealership)
            add_supplier_dealership_history(id.supplier, dealership, id.car, price)


def check_demand(dealership):
    DealershipSales = DealershipCustomerSales.objects.filter(dealership=dealership)

    if DealershipSales is None:
        return

    cars = (
        DealershipSales.objects.annotate(count=Count("car"))
        .order_by("-count")
        .values_list("car", flat=True)
    )

    best_cars = Car.objects.filter(car__in=cars)

    return best_cars


def get_discount_pricelist(dealership, cars):
    """Возвращает список (номер записи в базе, цена с учётом скидки)"""
    car_price_list = []

    for car in cars:
        car_price_list.append((car.id, get_car_discount_price(dealership, car)))

    return car_price_list


def get_car_discount_price(dealership, car):
    """Возвращает цену с учётом всех скидок"""
    new_price = None

    # цена со скидкой регулярного покупателя
    discount_price = get_regular_customer_discount_price(
        dealership, car.supplier, car.price
    )
    if discount_price:
        new_price = discount_price

    # проверить скидки
    discount_price = get_discount_price(car.id, car.supplier, car.price)
    if discount_price:
        if discount_price < new_price or new_price is None:
            new_price = discount_price

    if new_price is None:
        return car.price.amount

    return new_price.amount


def get_discount_price(car, supplier, price):
    """Возвращает цену с учётом скидки из таблицы скидок"""
    discount = SupplierDiscount.objects.filter(car=car, supplier=supplier).first()

    if discount is None:
        return

    return price * (100 - discount.percent) / 100


def get_regular_customer_discount_price(dealership, supplier, price):
    """Возвращает цену со скидкой регулярного покупателя"""
    num = SupplierUniqueCustomers.objects.filter(
        dealership=dealership, supplier=supplier
    ).first()

    if num is None:
        return

    num = num.number_of_purchases

    percent = None

    for key in supplier.discount.keys():
        if num < int(key):
            percent = percent
        else:
            percent = supplier.discount[key]

    if percent is None:
        return

    return price * (100 - float(percent)) / 100


#
#
def change_balance(dealership, price):
    dealership.balance.amount -= price


def add_car(car, dealership):
    obj, created = DealershipCars.objects.get_or_create(
        dealership=dealership,
        car=car,
        defaults={"quantity": 0, "price": 0},
    )
    obj.quantity += 1
    obj.save()


def add_supplier_dealership_history(supplier, dealership, car, price):
    SupplierDealershipSales.objects.create(
        supplier=supplier, dealership=dealership, car=car, price=price
    )


def add_supplier_customers(supplier, dealership):
    obj, created = SupplierUniqueCustomers.objects.get_or_create(
        supplier=supplier,
        dealership=dealership,
        defaults={"number_of_purchases": 0},
    )
    obj.number_of_purchases += 1
    obj.save()
