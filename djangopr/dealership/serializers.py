from django_countries.serializers import CountryFieldMixin
from djmoney.models.fields import MoneyField
from rest_framework import serializers

from .models import (Car, Customer, Dealership, DealershipCars,
                     DealershipCustomerSales, DealershipDiscount,
                     DealershipUniqueCustomers, Supplier, SupplierCars,
                     SupplierDealershipSales)


class CustomerSerializer(CountryFieldMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    def get_balance(self, obj):
        if (
            self.context["request"].user == obj.user
            or self.context["request"].user.is_staff
        ):
            return obj.balance.amount
        else:
            return None

    balance = serializers.SerializerMethodField("get_balance")

    class Meta:
        model = Customer
        fields = (
            "id",
            "name",
            "surname",
            "gender",
            "date_of_birth",
            "country",
            "balance",
        )


class PriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipCars
        fields = ("price", "quantity")


class CarSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    price_list = PriceListSerializer(
        many=True, source="dealershipcars_set", read_only=True
    )

    class Meta:
        model = Car
        fields = (
            "id" "model",
            "power",
            "transmission",
            "fuel",
            "drive_type",
            "registration_year",
            "price_list",
        )


class DealershipCarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipCars
        fields = ("car", "price", "quantity")


class DealershipSerializer(CountryFieldMixin, serializers.ModelSerializer):
    def get_balance(self, obj):
        if (
            self.context["request"].user == obj.user
            or self.context["request"].user.is_staff
        ):
            return obj.balance.amount
        else:
            return None

    id = serializers.IntegerField(read_only=True)
    cars = DealershipCarsSerializer(many=True, source="dealershipcars", read_only=True)
    balance = serializers.SerializerMethodField("get_balance")

    class Meta:
        model = Dealership
        fields = ("id", "cars", "company_name", "location", "specification", "balance")


class DealershipDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipDiscount
        fields = (
            "dealership",
            "name",
            "description",
            "percent",
            "start_date",
            "end_date",
        )


class DealershipUniqueCustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipUniqueCustomers
        fields = ("dealership", "customer", "number_of_purchases")


class DealershipCustomerSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipCustomerSales
        fields = ("customer", "dealership", "car", "price")


class SupplierCarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierCars
        fields = ("supplier", "car", "price", "quantity")


class SupplierSerializer(serializers.ModelSerializer):
    cars = SupplierCarsSerializer(many=True, source="suppliercars_set", read_only=True)

    class Meta:
        model = Supplier
        fields = (
            "cars",
            "company_name",
            "date_of_foundation",
            "number_of_buyers",
            "specification",
            "discount",
        )


class SupplierDealershipSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierDealershipSales
        fields = ("supplier", "dealership", "car", "price")
