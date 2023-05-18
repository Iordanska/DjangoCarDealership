from django.urls import include, path
from rest_framework import routers

from .views import (CarViewSet, CustomerFullViewSet, CustomerViewSet,
                    DealershipDiscountViewSet, DealershipFullViewSet,
                    DealershipViewSet, SupplierViewSet)

router = routers.SimpleRouter()
router.register(r"cars", CarViewSet)
router.register(r"customer", CustomerViewSet)
router.register(r"customer_profile", CustomerFullViewSet)
router.register(r"dealership", DealershipViewSet)
router.register(r"dealership_profile", DealershipFullViewSet)
router.register(r"supplier", SupplierViewSet)
router.register(r"discounts", DealershipDiscountViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
