from django_filters import rest_framework as filters
from django_countries import countries
from dealership.models import (
    Car,
    Customer,
    Dealership,
    DealershipUniqueCustomers,
    DealershipDiscount,
    Supplier,
)


class CarsFilter(filters.FilterSet):
    power = filters.RangeFilter()
    transmission = filters.MultipleChoiceFilter(choices=Car.Transmission.choices)
    fuel = filters.MultipleChoiceFilter(choices=Car.Fuel.choices)
    drive_type = filters.MultipleChoiceFilter(choices=Car.DriveType.choices)
    registration_year = filters.RangeFilter()
    dealershipcars__price = filters.RangeFilter(label="Price")

    class Meta:
        model = Car
        fields = [
            "power",
            "transmission",
            "fuel",
            "drive_type",
            "registration_year",
            "dealershipcars__price"
        ]


class CustomerFilter(filters.FilterSet):
    country = filters.ChoiceFilter(choices=countries)

    class Meta:
        model = Customer
        fields = ["country"]


class DealershipFilter(filters.FilterSet):
    location = filters.ChoiceFilter(choices=countries)
    dealershipcars__price = filters.RangeFilter(label="Price")

    class Meta:
        model = Dealership
        fields = ["location", "dealershipcars__price"]


class DealershipDiscountFilter(filters.FilterSet):
    percent = filters.RangeFilter()
    end_date = filters.DateFilter()

    class Meta:
        model = DealershipDiscount
        fields = ["percent", "end_date"]
