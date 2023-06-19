from datetime import timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField

from core.mixins import DateAndActiveMixin
from core.validators import date_validator, year_validator
from users.models import User


def specification_default():
    return {
        "transmission": "",
        "fuel": "",
        "drive_type": "",
    }


def order_default():
    return {
        "max_price": "",
        "car_model": "",
    }


def discount_default():
    return ({"num_of_purchases": "percent"},)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Customer(DateAndActiveMixin):
    name = models.CharField(max_length=100, null=True)
    surname = models.CharField(max_length=100, null=True)

    class Gender(models.TextChoices):
        M = "M", "male"
        F = "F", "female"

    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.M)
    date_of_birth = models.DateField(validators=[date_validator], null=True)
    country = CountryField(null=True)
    balance = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        editable=False,
        default=0,
    )
    order = models.JSONField(default=order_default)
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)

    objects = ActiveManager()

    def __str__(self):
        return str(self.name) + " " + str(self.surname)


class Car(DateAndActiveMixin):
    model = models.CharField(max_length=100)
    power = models.PositiveIntegerField(default=150)

    class Transmission(models.TextChoices):
        MANUAL = "manual"
        AUTOMATIC = "automatic"
        SEMI_AUTOMATIC = "semi-automatic"

    transmission = models.CharField(
        max_length=20, choices=Transmission.choices, default=Transmission.MANUAL
    )

    class Fuel(models.TextChoices):
        DIESEL = "diesel"
        PETROL = "petrol"
        ELECTRIC = "electric"
        OTHER = "other"

    fuel = models.CharField(max_length=20, choices=Fuel.choices, default=Fuel.DIESEL)

    class DriveType(models.TextChoices):
        FRONT = "front"
        REAR = "rear"
        ALL_WHEEL = "all_wheel"

    drive_type = models.CharField(
        max_length=20, choices=DriveType.choices, default=DriveType.REAR
    )
    registration_year = models.SmallIntegerField(validators=[year_validator])
    objects = ActiveManager()

    def __str__(self):
        return self.model


class Supplier(DateAndActiveMixin):
    cars = models.ManyToManyField(Car, through="SupplierCars")
    company_name = models.CharField(max_length=100, null=True)
    date_of_foundation = models.DateField(null=True, validators=[date_validator])
    number_of_buyers = models.IntegerField(default=0, editable=False)
    specification = models.JSONField("Specification", default=specification_default)
    discount = models.JSONField("Discount", default=discount_default)
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)

    objects = ActiveManager()

    def __str__(self):
        return str(self.company_name)


class SupplierCars(DateAndActiveMixin):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")

    objects = ActiveManager()

    def __str__(self):
        return str(self.supplier) + " " + str(self.car)


class Dealership(DateAndActiveMixin):
    cars = models.ManyToManyField(
        Car, through="DealershipCars", related_name="dealership"
    )
    company_name = models.CharField(max_length=100, null=True)
    location = CountryField(null=True)
    specification = models.JSONField("Specification", default=specification_default)
    balance = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        editable=False,
        default=0,
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)

    objects = ActiveManager()

    def __str__(self):
        return str(self.company_name)


class DealershipCars(DateAndActiveMixin):
    dealership = models.ForeignKey(
        Dealership, on_delete=models.CASCADE, related_name="dealershipcars"
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")
    quantity = models.PositiveIntegerField(default=0)
    objects = ActiveManager()

    def __str__(self):
        return str(self.dealership) + " " + str(self.car)


class DealershipDiscount(DateAndActiveMixin):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    percent = models.FloatField(
        default=10, validators=[MinValueValidator(0.1), MaxValueValidator(100)]
    )
    start_date = models.DateTimeField(default=timezone.now())
    end_date = models.DateTimeField(default=timezone.now() + timedelta(days=1))

    objects = ActiveManager()

    def __str__(self):
        return str(self.pk) + " " + str(self.name)


class DealershipUniqueCustomers(DateAndActiveMixin):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, editable=False)
    number_of_purchases = models.PositiveIntegerField(default=0, editable=False)

    objects = ActiveManager()

    def __str__(self):
        return str(self.customer)


class SupplierDiscount(DateAndActiveMixin):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    percent = models.FloatField(
        default=10, validators=[MinValueValidator(0.1), MaxValueValidator(100)]
    )
    start_date = models.DateTimeField(default=timezone.now())
    end_date = models.DateTimeField(default=timezone.now() + timedelta(days=1))

    objects = ActiveManager()

    def __str__(self):
        return str(self.pk) + " " + str(self.name)


class DealershipCustomerSales(DateAndActiveMixin):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, editable=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, editable=False)
    price = MoneyField(
        max_digits=14, decimal_places=2, default_currency="USD", editable=False
    )

    def __str__(self):
        return str(self.pk)


class SupplierDealershipSales(DateAndActiveMixin):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, editable=False)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, editable=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, editable=False)
    price = MoneyField(
        max_digits=14, decimal_places=2, default_currency="USD", editable=False
    )

    objects = ActiveManager()

    def __str__(self):
        return str(self.pk)


class SupplierUniqueCustomers(DateAndActiveMixin):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, editable=False)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, editable=False)
    number_of_purchases = models.PositiveIntegerField(default=0, editable=False)

    objects = ActiveManager()

    def __str__(self):
        return str(self.supplier)
