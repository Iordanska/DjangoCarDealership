from djmoney.models.fields import MoneyField
from rest_framework import serializers

from .models import (Car, Customer, Dealership, DealershipCars,
                     DealershipCustomerSales, DealershipDiscount,
                     DealershipUniqueCustomers, Supplier, SupplierCars,
                     SupplierDealershipSales)


class CustomerSerializer(serializers.ModelSerializer):
    def get_balance(self, obj):
        if self.context["request"].user == obj.user or self.context["request"].user.is_staff:
            return obj.balance.amount
        else:
            return None

    balance = serializers.SerializerMethodField("get_balance")

    class Meta:
        model = Customer
        fields = ("name", "surname", "gender", "date_of_birth", "country", "balance")


class PriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipCars
        fields = ("dealership_id", "price", "quantity")


class CarSerializer(serializers.ModelSerializer):
    price_list = PriceListSerializer(
        many=True, source="dealershipcars_set", read_only=True
    )

    class Meta:
        model = Car
        fields = (
            "model",
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


class DealershipSerializer(serializers.ModelSerializer):
    def get_balance(self, obj):
        if self.context["request"].user == obj.user or self.context["request"].user.is_staff:
            return obj.balance.amount
        else:
            return None

    cars = DealershipCarsSerializer(
        many=True, source="dealershipcars_set", read_only=True
    )
    balance = serializers.SerializerMethodField("get_balance")

    class Meta:
        model = Dealership
        fields = ("cars", "company_name", "location", "specification", "balance")


class DealershipDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipDiscount
        fields = (
            "dealership_id",
            "name",
            "description",
            "percent",
            "start_date",
            "end_date",
        )


class DealershipUniqueCustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipUniqueCustomers
        fields = ("dealership_id", "customer_id", "number_of_purchases")


class DealershipCustomerSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipCustomerSales
        fields = ("customer_id", "dealership_id", "car_id", "price")


class SupplierCarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierCars
        fields = ("supplier_id", "car", "price", "quantity")


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
        fields = ("supplier_id", "dealership_id", "car_id", "price")
