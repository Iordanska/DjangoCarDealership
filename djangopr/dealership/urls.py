from django.urls import include, path
from rest_framework import routers

from dealership.views import (
    CarViewSet,
    CustomerViewSet,
    DealershipDiscountViewSet,
    DealershipViewSet,
    SupplierDiscountViewSet,
    SupplierViewSet,
)

router = routers.SimpleRouter()

router.register(r"car", CarViewSet)
router.register(r"customer", CustomerViewSet)
router.register(r"dealership", DealershipViewSet)
router.register(r"supplier", SupplierViewSet)
router.register(r"discount_dealership", DealershipDiscountViewSet)
router.register(r"discount_supplier", SupplierDiscountViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
