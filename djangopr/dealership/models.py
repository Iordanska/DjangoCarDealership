from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField

from core.mixins import DateAndActiveMixin
from core.validators import date_validator, year_validator


def specification_default():
    return {
        "registration_year": "",
        "transmission": "",
        "power": "",
        "fuel": "",
        "drive_type": "",
    }


# def order_default():
#     return {
#         "user_id": "",
#         "max_price": "",
#         "car_model": "",
#     }


def discount_default():
    return {
        "discount": [
            {"num_of_purchases": "percent"},
        ],
    }


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
        default=100,
    )
    user = models.OneToOneField(User,limit_choices_to={'role':'Customer'}, on_delete=models.CASCADE, editable=False)

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
        FRONT = "front-wheel"
        REAR = "rear-wheel"
        ALL = "4X4"

    drive_type = models.CharField(
        max_length=20, choices=DriveType.choices, default=DriveType.REAR
    )
    registration_year = models.SmallIntegerField(validators=[year_validator])

    def __str__(self):
        return self.model

class Order(DateAndActiveMixin):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car=models.ForeignKey(Car, on_delete=models.CASCADE)
    max_price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
    )


class Supplier(DateAndActiveMixin):
    cars = models.ManyToManyField(Car, through="SupplierCars")
    company_name = models.CharField(max_length=100, null=True)
    date_of_foundation = models.DateField(null=True, validators=[date_validator])
    number_of_buyers = models.IntegerField(default=0, editable=False)
    specification = models.JSONField("Specification", default=specification_default)
    discount = models.JSONField("Discount", default=discount_default)
    user = models.OneToOneField(User, limit_choices_to={'role':'Supplier'}, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.company_name)


class SupplierCars(DateAndActiveMixin):
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.supplier_id) + " " + str(self.car)


class Dealership(DateAndActiveMixin):
    cars = models.ManyToManyField(Car, through="DealershipCars", related_name="dealership")
    company_name = models.CharField(max_length=100, null=True)
    location = CountryField(null=True)
    specification = models.JSONField("Specification", default=specification_default)
    balance = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        editable=False,
        default=50000,
    )
    user = models.OneToOneField(User, limit_choices_to={'role':'Dealership'},on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return str(self.company_name)


class DealershipCars(DateAndActiveMixin):
    dealership_id = models.ForeignKey(Dealership, on_delete=models.CASCADE, related_name="dealershipcars")
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.dealership_id) + " " + str(self.car)


class DealershipDiscount(DateAndActiveMixin):
    dealership_id = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    percent = models.FloatField(
        default=10, validators=[MinValueValidator(0.1), MaxValueValidator(100)]
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return str(self.pk) + " " + str(self.name)


class DealershipUniqueCustomers(DateAndActiveMixin):
    dealership_id = models.ForeignKey(
        Dealership, on_delete=models.CASCADE, editable=False
    )
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, editable=False)
    number_of_purchases = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return str(self.customer_id)


class DealershipCustomerSales(DateAndActiveMixin):
    dealership_id = models.ForeignKey(
        Dealership, on_delete=models.CASCADE, editable=False
    )
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, editable=False)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE, editable=False)
    price = MoneyField(
        max_digits=14, decimal_places=2, default_currency="USD", editable=False
    )

    def __str__(self):
        return str(self.pk)


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
        return str(self.pk)
