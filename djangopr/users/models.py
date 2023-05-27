from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'Customer'
        DEALERSHIP = 'Dealership'
        SUPPLIER =  'Supplier'

    role = models.CharField(choices=Role.choices, blank=True, null=True, max_length=20)