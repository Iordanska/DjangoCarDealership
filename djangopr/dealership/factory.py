import json

import factory
from django.db.models.signals import post_save
from django_countries.data import COUNTRIES
from factory import fuzzy
from factory.django import DjangoModelFactory

from users.models import User

from .models import (
    Car,
    Customer,
    Dealership,
    DealershipCars,
    DealershipDiscount,
    Supplier,
    SupplierCars,
    SupplierDiscount,
)


class JSONFactory(factory.DictFactory):
    """
    Use with factory.Dict to make JSON strings.
    """

    @classmethod
    def _generate(cls, create, attrs):
        obj = super()._generate(create, attrs)
        return json.dumps(obj)


@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("profile", fields=["username"])
    role = fuzzy.FuzzyChoice(["Customer", "Dealership", "Supplier"])
    email = factory.Faker("email")


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    country = factory.fuzzy.FuzzyChoice(COUNTRIES)
    gender = factory.fuzzy.FuzzyChoice(["M", "F"])
    date_of_birth = factory.Faker("date_of_birth")
    balance = factory.fuzzy.FuzzyDecimal(10000.00, 40000.00)
    order = factory.Dict(
        {
            "max_price": "",
            "car_model": "",
        },
        dict_factory=JSONFactory,
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = UserFactory(role="Customer")
        customer = model_class.objects.create(user=user, **kwargs)
        customer.save()

        return customer


class CarFactory(DjangoModelFactory):
    class Meta:
        model = Car

    model = factory.Faker("word")
    power = factory.fuzzy.FuzzyInteger(1, 300)
    transmission = factory.fuzzy.FuzzyChoice(["manual", "automatic", "semi-automatic"])
    fuel = factory.fuzzy.FuzzyChoice(["diesel", "petrol", "electric", "other"])
    drive_type = factory.fuzzy.FuzzyChoice(["front", "rear", "all_wheel"])
    registration_year = factory.fuzzy.FuzzyInteger(2000, 2020)


class DealershipFactory(DjangoModelFactory):
    class Meta:
        model = Dealership

    company_name = factory.Faker("first_name")
    location = factory.fuzzy.FuzzyChoice(COUNTRIES)
    balance = factory.fuzzy.FuzzyDecimal(50000.00, 100000.00)

    specification = factory.Dict(
        {
            "transmission": "",
            "fuel": "",
            "drive_type": "",
        },
        dict_factory=JSONFactory,
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = UserFactory(role="Dealership")
        dealership = model_class.objects.create(user=user, **kwargs)
        dealership.save()

        return dealership


class DealershipCarsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DealershipCars

    dealership = factory.SubFactory(DealershipFactory)
    car = factory.SubFactory(CarFactory)
    price = factory.fuzzy.FuzzyDecimal(10000, 20000)
    quantity = factory.fuzzy.FuzzyInteger(1, 100)


class DealershipDiscountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DealershipDiscount

    dealership = factory.SubFactory(DealershipFactory)
    car = factory.SubFactory(CarFactory)
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    percent = factory.fuzzy.FuzzyFloat(0.1, 100)


class SupplierFactory(DjangoModelFactory):
    class Meta:
        model = Supplier

    company_name = factory.Faker("first_name")
    date_of_foundation = factory.Faker("date_of_birth")
    discount = factory.Dict(
        {
            "0": "0",
        },
        dict_factory=JSONFactory,
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = UserFactory(role="Supplier")
        supplier = model_class.objects.create(user=user, **kwargs)
        supplier.save()

        return supplier


class SupplierCarsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SupplierCars

    supplier = factory.SubFactory(SupplierFactory)
    car = factory.SubFactory(CarFactory)
    price = factory.fuzzy.FuzzyDecimal(10000, 20000)


class SupplierDiscountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SupplierDiscount

    supplier = factory.SubFactory(SupplierFactory)
    car = factory.SubFactory(CarFactory)
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    percent = factory.fuzzy.FuzzyFloat(0.1, 100)
