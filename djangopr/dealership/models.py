from django.db import models
from django_countries.fields import CountryField
from djangopr.core.mixins import DateAndActiveMixin
from djangopr.core.validators import date_validator, year_validator
from djmoney.models.fields import MoneyField


def specification_default():
    return {
        "registration_year": "",
        "transmission": "",
        "power": "",
        "fuel": "",
        "drive_type": "",
    }


def order_default():
    return {
        "user_id": "",
        "max_price": "",
        "car_model": "",
    }


def discount_default():
    return {
        "discount": [
            {"num_of_purchases": "percent"},
        ],
    }


class CustomerProfile(DateAndActiveMixin):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    class Gender(models.TextChoices):
        M = "M", "male"
        F = "F", "female"

    gender = models.CharField(max_length=1, choices=Gender.choises, default=Gender.M)
    date_of_birth = models.DateField(validators=[date_validator])
    country = CountryField()
    balance = MoneyField(
        max_digits=14, decimal_places=2, default_currency="USD", editable=False
    )
    order = models.JSONField("Order", default=order_default)

    def __str__(self):
        return str(self.name) + " " + str(self.surname)


class Car(DateAndActiveMixin):
    model = models.CharField(max_length=100)
    power = models.DecimalField(max_digits=3, decimal_places=2)

    class Transmission(models.TextChoices):
        MANUAL = "manual"
        AUTOMATIC = "automatic"
        SEMI_AUTOMATIC = "semi-automatic"

    transmission = models.CharField(
        max_length=20, choices=Transmission.choises, default=Transmission.MANUAL
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
        max_length=20, choices=DriveType.choises, default=DriveType.REAR
    )
    registration_year = models.SmallIntegerField(validators=[year_validator])

    def __str__(self):
        return self.model


class Supplier(DateAndActiveMixin):
    cars = models.ManyToManyField(Car, through="SupplierCars")
    company_name = models.CharField(max_length=100)
    date_of_foundation = models.DateTimeField(blank=True, validators=[date_validator])
    number_of_buyers = models.IntegerField(default=0, editable=False)
    specification = models.JSONField("Specification", default=specification_default)
    discount = models.JSONField("Discount", default=discount_default)
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
    name = models.CharField(max_length=100)
    description = models.TextField()
    percent = models.DecimalField(max_digits=3, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return str(self.pk) + " " + str(self.name)


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
