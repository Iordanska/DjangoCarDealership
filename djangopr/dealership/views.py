from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from core.mixins import CustomDestroyModelMixin
from .models import (
    Car,
    Customer,
    Dealership,
    DealershipCars,
    DealershipCustomerSales,
    DealershipDiscount,
    DealershipUniqueCustomers,
    Supplier,
    SupplierCars,
    SupplierDealershipSales,
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdminUser
from .serializers import (
    CarSerializer,
    CustomerFullSerializer,
    CustomerSerializer,
    DealershipCarsSerializer,
    DealershipCustomerSalesSerializer,
    DealershipDiscountSerializer,
    DealershipFullSerializer,
    DealershipSerializer,
    DealershipUniqueCustomersSerializer,
    SupplierCarsSerializer,
    SupplierDealershipSalesSerializer,
    SupplierSerializer,
)
from core.filters import CarsFilter


class CustomerViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerFullViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Customer.objects.all()
    serializer_class = CustomerFullSerializer
    permission_classes = [IsOwnerOrAdminUser]


class CarViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    CustomDestroyModelMixin,
    GenericViewSet,
):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["model"]
    filterset_class = CarsFilter
    permission_classes = [IsAdminOrReadOnly]


class DealershipViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Dealership.objects.all()
    serializer_class = DealershipSerializer
    lookup_field = "pk"

    @action(methods=["get"], detail=True, serializer_class=DealershipCarsSerializer)
    def cars(self, request, pk=None):
        queryset = DealershipCars.objects.filter(dealership_id=self.kwargs["pk"])
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DealershipFullViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet
):
    queryset = Dealership.objects.all()
    serializer_class = DealershipFullSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUser]

    @action(
        methods=["get"],
        detail=True,
        serializer_class=DealershipUniqueCustomersSerializer,
    )
    def customers(self, request, pk=None):
        queryset = DealershipUniqueCustomers.objects.filter(
            dealership_id=self.kwargs["pk"]
        )
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["get"], detail=True, serializer_class=DealershipCustomerSalesSerializer
    )
    def history_customers(self, request, pk=None):
        queryset = DealershipCustomerSales.objects.filter(
            dealership_id=self.kwargs["pk"]
        )
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["get"], detail=True, serializer_class=SupplierDealershipSalesSerializer
    )
    def history_suppliers(self, request, pk=None):
        queryset = SupplierDealershipSales.objects.filter(
            dealership_id=self.kwargs["pk"]
        )
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DealershipDiscountViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    CustomDestroyModelMixin,
    GenericViewSet,
):
    serializer_class = DealershipDiscountSerializer
    queryset = DealershipDiscount.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class SupplierViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(
        methods=["get"],
        detail=True,
        serializer_class=SupplierDealershipSalesSerializer,
        permission_classes=[IsAdminUser],
    )
    def history(self, request, pk=None):
        queryset = SupplierDealershipSales.objects.filter(supplier_id=self.kwargs["pk"])
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True, serializer_class=SupplierCarsSerializer)
    def cars(self, request, pk=None):
        queryset = SupplierCars.objects.filter(supplier_id=self.kwargs["pk"])
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
