from django.urls import include, path
from rest_framework import routers

from .views import (CarViewSet, CustomerViewSet, DealershipDiscountViewSet,
                    DealershipViewSet, SupplierViewSet)

router = routers.SimpleRouter()
router.register(r"cars", CarViewSet)
router.register(r"customer", CustomerViewSet)
router.register(r"dealership", DealershipViewSet)
router.register(r"supplier", SupplierViewSet)
router.register(r"discounts", DealershipDiscountViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
