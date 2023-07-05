import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangopr.settings")

app = Celery("djangopr", broker='redis://localhost:6379/0')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'dealership.tasks.fulfill_orders_task',
        'schedule': crontab(),
    },
    'every-10-minute': {
        'task': 'dealership.tasks.dealership_buy_cars_task',
        'schedule': crontab(minute="*/10"),
    },
}
