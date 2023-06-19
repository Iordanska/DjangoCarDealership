from _decimal import Decimal
from django.db.models import Q

from dealership.models import (
    Dealership,
    DealershipCars,
    SupplierCars,
    SupplierDealershipSales,
    SupplierDiscount,
    SupplierUniqueCustomers,
)


def dealership_buy_cars():
    dealerships_updated = []
    supplier_sales_updated = []
    dealerships = Dealership.objects.filter(balance__gte=0)
    for dealership in dealerships:
        selected_cars = select_cars(dealership)
        if not selected_cars:
            return
        dealership_updated, sales_updated = buy_cars(dealership, selected_cars)
        if dealership_updated:
            dealerships_updated.append(dealership_updated)
            supplier_sales_updated.append(sales_updated)

    if not dealerships_updated:
        return
    Dealership.objects.bulk_update(dealerships_updated, ["balance"])
    for supplier_sale in supplier_sales_updated:
        SupplierDealershipSales.objects.bulk_create(supplier_sale)


def select_cars(dealership):
    q_objects = Q()
    for key, value in dealership.specification.items():
        if value:
            q_objects.add(Q(**{"car__" + key: value}), Q.AND)

    selected_cars = SupplierCars.objects.filter(q_objects)

    # Цена с учёток скидок
    car_price_list = get_discount_pricelist(dealership, selected_cars)
    # сортировка по новой цене
    car_list_sorted = sorted(car_price_list, key=lambda car: car[1])
    return car_list_sorted


def buy_cars(dealership, car_list_sorted):
    sales_updated = []

    for car in car_list_sorted:
        supplier_car = SupplierCars.objects.get(pk=car[0])
        price = car[1]

        while dealership.balance.amount >= price:
            dealership.balance.amount -= price
            add_car(supplier_car.car, dealership)
            add_supplier_customers(supplier_car.supplier, dealership)
            sales_updated.append(
                SupplierDealershipSales(
                    supplier=supplier_car.supplier,
                    dealership=dealership,
                    car=supplier_car.car,
                    price=price,
                )
            )

    dealership_updated = dealership

    return dealership_updated, sales_updated


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
        if new_price is None or discount_price < new_price:
            new_price = discount_price

    if new_price is None:
        return car.price.amount

    return new_price


def get_discount_price(car, supplier, price):
    """Возвращает цену с учётом скидки из таблицы скидок"""
    discount = SupplierDiscount.objects.filter(car=car, supplier=supplier).first()

    if discount is None:
        return

    return (
        price.amount * (Decimal(100.00) - Decimal(discount.percent)) / Decimal(100.00)
    )


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
        if key == "number_of_purchases":
            return
        if num < int(key):
            percent = percent
        else:
            percent = supplier.discount[key]

    if percent is None:
        return

    return price * (Decimal(100.00) - Decimal(percent)) / Decimal(100)


def add_car(car, dealership):
    car, created = DealershipCars.objects.get_or_create(
        dealership=dealership,
        car=car,
        defaults={"quantity": 0, "price": 0},
    )
    car.quantity += 1
    car.save(update_fields=["quantity"])


def add_supplier_customers(supplier, dealership):
    supplier_customers, created = SupplierUniqueCustomers.objects.get_or_create(
        supplier=supplier,
        dealership=dealership,
        defaults={"number_of_purchases": 0},
    )
    if supplier_customers.number_of_purchases == 0:
        supplier.number_of_buyers += 1
        supplier.save(update_fields=["number_of_buyers"])

    supplier_customers.number_of_purchases += 1
    supplier_customers.save(update_fields=["number_of_purchases"])
