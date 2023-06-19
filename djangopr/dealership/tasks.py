from celery import shared_task

from .celery_dealership_buy_cars import dealership_buy_cars
from .celery_fulfill_orders import check_orders


@shared_task
def fulfill_orders_task():
    check_orders()


@shared_task
def dealership_buy_cars_task():
    dealership_buy_cars()
