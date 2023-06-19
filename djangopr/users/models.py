from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "Customer"
        DEALERSHIP = "Dealership"
        SUPPLIER = "Supplier"

    role = models.CharField(choices=Role.choices, null=True, max_length=20)
    REQUIRED_FIELDS = ['email', 'role']
