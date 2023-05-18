from django_filters import rest_framework as filters

from dealership.models import Car


class CarsFilter(filters.FilterSet):
    power = filters.RangeFilter()
    transmission = filters.MultipleChoiceFilter(choices=Car.Transmission.choices)
    fuel = filters.MultipleChoiceFilter(choices=Car.Fuel.choices)
    drive_type = filters.MultipleChoiceFilter(choices=Car.DriveType.choices)
    registration_year = filters.RangeFilter()

    class Meta:
        model = Car
        fields = ["power", "transmission", "fuel", "drive_type", "registration_year"]
