from rest_framework import permissions, viewsets, mixins
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdminUser
from .serializers import *


# Customer
class CustomerViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


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
    GenericViewSet,
):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminOrReadOnly]


class DealershipViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Dealership.objects.all()
    serializer_class = DealershipSerializer
    permission_classes = [IsAuthenticated]


class DealershipFullViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet
):
    queryset = Dealership.objects.all()
    serializer_class = DealershipFullSerializer
    permission_classes = [IsAdminUser]


class DealershipDiscountViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = DealershipDiscountSerializer
    queryset = DealershipDiscount.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class DealershipUniqueCustomersView(ListAPIView):
    serializer_class = DealershipUniqueCustomersSerializer

    def get_queryset(self):
        queryset = DealershipUniqueCustomers.objects.filter(
            dealership_id=self.kwargs["pk"]
        )
        return queryset

    permission_classes = [IsAdminUser]


class DealershipCustomerSalesView(ListAPIView):
    serializer_class = DealershipCustomerSalesSerializer

    def get_queryset(self):
        queryset = DealershipCustomerSales.objects.filter(
            dealership_id=self.kwargs["pk"]
        )
        return queryset

    permission_classes = [IsAdminUser]


class DealershipSupplierSalesView(ListAPIView):
    serializer_class = SupplierDealershipSalesSerializer

    def get_queryset(self):
        queryset = SupplierDealershipSales.objects.filter(
            dealership_id=self.kwargs["pk"]
        )
        return queryset

    permission_classes = [IsAdminUser]


class DealershipCarsView(ListAPIView):
    serializer_class = DealershipCarsSerializer

    def get_queryset(self):
        queryset = DealershipCars.objects.filter(dealership_id=self.kwargs["pk"])
        return queryset


#


class SupplierViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAdminOrReadOnly]


class SupplierDealershipSalesView(ListAPIView):
    serializer_class = SupplierDealershipSalesSerializer

    def get_queryset(self):
        queryset = SupplierDealershipSales.objects.filter(supplier_id=self.kwargs["pk"])
        return queryset

    permission_classes = [IsAdminUser]


class SupplierCarsView(ListAPIView):
    serializer_class = SupplierCarsSerializer

    def get_queryset(self):
        queryset = SupplierCars.objects.filter(supplier_id=self.kwargs["pk"])
        return queryset
