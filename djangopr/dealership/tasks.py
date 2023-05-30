from celery import shared_task

from .service import check_orders


@shared_task
def check_orders_task():
    check_orders()
