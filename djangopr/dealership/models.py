from datetime import datetime

from core.mixins import DateAndActiveMixin
from django.core.exceptions import ValidationError
from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField


def date_validator(value):
    if value < datetime(1901, 1, 1) or value > datetime.now():
        raise ValidationError(
            _("%(value)s is not a correct date."),
            params={"value": value},
        )


def year_validator(value):
    if value < 1960 or value > datetime.now().year:
        raise ValidationError(
            _("%(value)s is not a correct year!"),
            params={"value": value},
        )


def specification_default():
    return {
        "registration_year": "",
        "transmission": "",
        "power": "",
        "fuel": "",
        "drive_type": "",
    }


def offer_default():
    return {
        "user_id": "",
        "max_price": "",
        "car_model": "",
    }


class CustomerProfile(DateAndActiveMixin):
    M = "M"
    F = "F"

    GENDER_CHOICES = ((M, "Male"), (F, "Female"))

    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=M)
    date_of_birth = models.DateField(validators=[date_validator])
    country = CountryField()
    balance = MoneyField(
        max_digits=14, decimal_places=2, default_currency="USD", editable=False
    )
    offer = models.JSONField("Offer", default=offer_default)

    def __str__(self):
        return str(self.name) + " " + str(self.surname)


class Car(DateAndActiveMixin):
    DIESEL = "diesel"
    PETROL = "petrol"
    ELECTRIC = "electric"
    OTHER = "other"

    FUEL_CHOICES = (
        (DIESEL, "Diesel"),
        (PETROL, "Petrol"),
        (ELECTRIC, "Electric"),
        (OTHER, "Other"),
    )

    MANUAL = "manual"
    AUTOMATIC = "automatic"
    SEMI_AUTOMATIC = "semi-automatic"

    TRANSMISSION_CHOICES = (
        (MANUAL, "Manual"),
        (AUTOMATIC, "Autimatic"),
        (SEMI_AUTOMATIC, "Semi-automatic"),
    )

    FRONT = "front-wheel"
    REAR = "rear-wheel"
    ALL = "4X4"

    DRIVE_TYPE_CHOICES = (
        (FRONT, "Front-wheel"),
        (REAR, "Rear-wheel"),
        (ALL, "4X4"),
    )

    model = models.CharField(max_length=100)
    registration_year = models.SmallIntegerField(validators=[year_validator])
    power = models.DecimalField(max_digits=3, decimal_places=2)
    transmission = models.CharField(
        max_length=20, choices=TRANSMISSION_CHOICES, default=MANUAL
    )
    fuel = models.CharField(max_length=20, choices=FUEL_CHOICES, default=DIESEL)
    drive_type = models.CharField(
        max_length=20, choices=DRIVE_TYPE_CHOICES, default=REAR
    )

    def __str__(self):
        return self.model


class Supplier(DateAndActiveMixin):
    cars = models.ManyToManyField(Car, through="SupplierCars")
    company_name = models.CharField(max_length=100)
    date_of_foundation = models.DateTimeField(blank=True, validators=[date_validator])
    number_of_buyers = models.IntegerField(default=0, editable=False)
    specification = models.JSONField("Specification", default=specification_default)
    number_of_purchases_for = models.PositiveIntegerField()
    primary_client_discount = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True
    )

    def __str__(self):
        return self.company_name


class SupplierCars(DateAndActiveMixin):
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")
    quantity = models.PositiveIntegerField(default=0)


class Dealership(DateAndActiveMixin):
    cars = models.ManyToManyField(Car, through="DealershipCars")
    company_name = models.CharField(max_length=100)
    location = CountryField()
    specification = models.JSONField("Specification", default=specification_default)
    balance = MoneyField(
        max_digits=14, decimal_places=2, default_currency="USD", editable=False
    )


class DealershipCars(DateAndActiveMixin):
    dealership_id = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")
    quantity = models.PositiveIntegerField(default=0)


class DealershipDiscount(DateAndActiveMixin):
    dealership_id = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    percent = models.DecimalField(max_digits=3, decimal_places=2)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.pk


class DealershipUniqueCustomers(DateAndActiveMixin):
    dealership_id = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    number_of_purchases = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.customer_id


class DealershipCustomerSales(DateAndActiveMixin):
    dealership_id = models.ForeignKey(
        Dealership, on_delete=models.CASCADE, editable=False
    )
    customer_id = models.ForeignKey(
        CustomerProfile, on_delete=models.CASCADE, editable=False
    )
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE, editable=False)
    price = MoneyField(
        max_digits=14, decimal_places=2, default_currency="USD", editable=False
    )

    def __str__(self):
        return self.pk


class SupplierDealershipSales(DateAndActiveMixin):
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE, editable=False)
    dealership_id = models.ForeignKey(
        Dealership, on_delete=models.CASCADE, editable=False
    )
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE, editable=False)
    price = MoneyField(
        max_digits=14, decimal_places=2, default_currency="USD", editable=False
    )

    def __str__(self):
        return self.pk
