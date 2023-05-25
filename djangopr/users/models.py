from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'Customer'
        DEALERSHIP = 'Dealership'
        SUPPLIER =  'Supplier'

    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(choices=Role.choices, blank=True, null=True, max_length=20)

    REQUIRED_FIELDS = ["email", "role"]