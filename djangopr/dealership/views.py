from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.filters import (CarsFilter, CustomerFilter, DealershipDiscountFilter,
                          DealershipFilter)
from core.mixins import CustomDestroyModelMixin

from .models import (Car, Customer, Dealership, DealershipCustomerSales,
                     DealershipDiscount, DealershipUniqueCustomers, Supplier,
                     SupplierDealershipSales)
from .permissions import IsAdminOrReadOnly, IsOwner, IsOwnerOrReadOnly
from .serializers import (CarSerializer, CustomerSerializer,
                          DealershipCustomerSalesSerializer,
                          DealershipDiscountSerializer, DealershipSerializer,
                          DealershipUniqueCustomersSerializer,
                          SupplierDealershipSalesSerializer,
                          SupplierSerializer)


class CustomerViewSet(
    CustomDestroyModelMixin,
    ModelViewSet,
):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = CustomerFilter
    search_fields = ["surname"]
    ordering_fields = ["surname"]
    permission_classes = [IsOwnerOrReadOnly | IsAdminUser]


class CarViewSet(
    CustomDestroyModelMixin,
    ModelViewSet,
):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = CarsFilter
    search_fields = ["model"]
    ordering_fields = ["dealershipcars__price"]
    permission_classes = [IsAdminOrReadOnly]


class DealershipViewSet(
    CustomDestroyModelMixin,
    ModelViewSet,
):
    queryset = Dealership.objects.all()
    serializer_class = DealershipSerializer
    lookup_field = "pk"
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = DealershipFilter
    search_fields = ["company_name"]
    ordering_fields = ["company_name", "dealershipcars__price"]
    permission_classes = [IsOwnerOrReadOnly | IsAdminUser]

    @action(
        methods=["get"],
        detail=True,
        serializer_class=DealershipUniqueCustomersSerializer,
        permission_classes=[IsOwner | IsAdminUser],
    )
    def customers(self, request, pk=None):
        queryset = DealershipUniqueCustomers.objects.filter(
            dealership=self.kwargs["pk"]
        )
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=True,
        serializer_class=DealershipCustomerSalesSerializer,
        permission_classes=[IsOwner | IsAdminUser],
    )
    def history_customers(self, request, pk=None):
        queryset = DealershipCustomerSales.objects.filter(dealership=self.kwargs["pk"])
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=True,
        serializer_class=SupplierDealershipSalesSerializer,
        permission_classes=[IsOwner | IsAdminUser],
    )
    def history_suppliers(self, request, pk=None):
        queryset = SupplierDealershipSales.objects.filter(dealership=self.kwargs["pk"])
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DealershipDiscountViewSet(
    CustomDestroyModelMixin,
    ModelViewSet,
):
    serializer_class = DealershipDiscountSerializer
    queryset = DealershipDiscount.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = DealershipDiscountFilter
    search_fields = ["name"]
    ordering_fields = ["percent", "end_date"]
    permission_classes = [IsAdminOrReadOnly]


class SupplierViewSet(ModelViewSet, CustomDestroyModelMixin):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["company_name"]
    ordering_fields = ["company_name", "number_of_buyers"]
    permission_classes = [IsOwnerOrReadOnly | IsAdminUser]

    @action(
        methods=["get"],
        detail=True,
        serializer_class=SupplierDealershipSalesSerializer,
        permission_classes=[IsOwner | IsAdminUser],
    )
    def history(self, request, pk=None):
        queryset = SupplierDealershipSales.objects.filter(supplier=self.kwargs["pk"])
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
