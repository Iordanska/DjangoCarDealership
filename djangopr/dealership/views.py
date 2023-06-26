from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from core.filters import (
    CarsFilter,
    CustomerFilter,
    DealershipDiscountFilter,
    DealershipFilter,
)
from core.mixins import CustomDestroyModelMixin

from dealership.models import (
    Car,
    Customer,
    Dealership,
    DealershipCustomerSales,
    DealershipDiscount,
    DealershipUniqueCustomers,
    Supplier,
    SupplierDealershipSales,
    SupplierDiscount,
    SupplierUniqueCustomers,
)
from dealership.permissions import IsAdminOrReadOnly, IsOwner, IsOwnerOrReadOnly
from dealership.serializers import (
    CarSerializer,
    CustomerSerializer,
    DealershipCustomerSalesSerializer,
    DealershipDiscountSerializer,
    DealershipSerializer,
    DealershipUniqueCustomersSerializer,
    SupplierDealershipSalesSerializer,
    SupplierDiscountSerializer,
    SupplierSerializer,
    SupplierUniqueCustomersSerializer,
)


class CustomerViewSet(
    CustomDestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = CustomerFilter
    search_fields = ["surname"]
    ordering_fields = ["surname"]
    permission_classes = [IsOwnerOrReadOnly | IsAdminUser]

    @action(
        methods=["get"],
        detail=True,
        serializer_class=DealershipCustomerSalesSerializer,
    )
    def history(self, request, pk=None):
        customer_id = self.kwargs["pk"]

        queryset = DealershipCustomerSales.objects.filter(
            customer=customer_id,
            customer__user=request.user.id,
        )
        if request.user.is_staff:
            queryset = DealershipCustomerSales.objects.filter(
                customer=customer_id,
            )

        if not queryset:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet,
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
    )
    def customers(self, request, pk=None):
        dealership_id = self.kwargs["pk"]

        queryset = DealershipUniqueCustomers.objects.filter(
            dealership=dealership_id,
            dealership__user=request.user.id,
        )

        if request.user.is_staff:
            queryset = DealershipUniqueCustomers.objects.filter(
                dealership=dealership_id,
            )

        if not queryset:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=True,
        serializer_class=DealershipCustomerSalesSerializer,
    )
    def history_customers(self, request, pk=None):
        dealership_id = self.kwargs["pk"]

        queryset = DealershipCustomerSales.objects.filter(
            dealership=dealership_id,
            dealership__user=request.user.id,
        )

        if request.user.is_staff:
            queryset = DealershipCustomerSales.objects.filter(
                dealership=dealership_id,
            )

        if not queryset:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=True,
        serializer_class=SupplierDealershipSalesSerializer,
    )
    def history_suppliers(self, request, pk=None):
        dealership_id = self.kwargs["pk"]

        queryset = SupplierDealershipSales.objects.filter(
            dealership=dealership_id,
            dealership__user=request.user.id,
        )

        if request.user.is_staff:
            queryset = SupplierDealershipSales.objects.filter(
                dealership=dealership_id,
            )

        if not queryset:
            return Response(status=status.HTTP_404_NOT_FOUND)

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


class SupplierViewSet(
    CustomDestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["company_name"]
    ordering_fields = ["company_name", "number_of_buyers"]
    permission_classes = [IsOwnerOrReadOnly | IsAdminUser]

    @action(
        methods=["get"],
        detail=True,
        serializer_class=SupplierUniqueCustomersSerializer,
    )
    def customers(self, request, pk=None):
        supplier_id = self.kwargs["pk"]

        queryset = SupplierUniqueCustomers.objects.filter(
            supplier=supplier_id,
            supplier__user=request.user.id,
        )

        if request.user.is_staff:
            queryset = SupplierUniqueCustomers.objects.filter(
                supplier=supplier_id,
            )

        if not queryset:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=True,
        serializer_class=SupplierDealershipSalesSerializer,
    )
    def history(self, request, pk=None):
        supplier_id = self.kwargs["pk"]

        queryset = SupplierDealershipSales.objects.filter(
            supplier=supplier_id,
            supplier__user=request.user.id,
        )

        if request.user.is_staff:
            queryset = SupplierDealershipSales.objects.filter(
                supplier=supplier_id,
            )

        if not queryset:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SupplierDiscountViewSet(
    CustomDestroyModelMixin,
    ModelViewSet,
):
    serializer_class = SupplierDiscountSerializer
    queryset = SupplierDiscount.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["name"]
    ordering_fields = ["percent", "end_date"]
    permission_classes = [IsAdminOrReadOnly]
