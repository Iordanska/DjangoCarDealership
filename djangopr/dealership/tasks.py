from celery import shared_task

from .service import check_orders
from .service2 import dealership_buy_cars


@shared_task
def check_orders_task():
    check_orders()


@shared_task
def dealership_buy_cars_task():
    dealership_buy_cars()
