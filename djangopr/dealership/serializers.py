from rest_framework import serializers

from .models import (
    Car,
    Customer,
    Dealership,
    DealershipCars,
    DealershipCustomerSales,
    DealershipDiscount,
    Supplier,
    SupplierCars,
    SupplierDealershipSales,
)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("name", "surname", "gender", "date_of_birth", "country")


class CustomerFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "name",
            "surname",
            "gender",
            "date_of_birth",
            "country",
            "order",
            "balance",
        )


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            "model",
            "power",
            "transmission",
            "fuel",
            "drive_type",
            "registration_year",
            "is_active",
        )
        extra_kwargs = {"is_active": {"write_only": True}}


class DealershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealership
        fields = ("company_name", "location", "specification")


class DealershipFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealership
        fields = ("company_name", "location", "specification", "balance")


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
            "is_active",
        )
        extra_kwargs = {"is_active": {"write_only": True}}


class DealershipUniqueCustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipDiscount
        fields = ("dealership_id", "customer_id", "number_of_purchases")


class DealershipCustomerSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipCustomerSales
        fields = ("customer_id", "dealership_id", "car_id", "price")


class DealershipCarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipCars
        fields = ("dealership_id", "car", "price", "quantity")


class SupplierSerializer(serializers.ModelSerializer):
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


class SupplierCarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierCars
        fields = ("supplier_id", "car", "price", "quantity")


class SupplierDealershipSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierDealershipSales
        fields = ("supplier_id", "dealership_id", "car_id", "price")
