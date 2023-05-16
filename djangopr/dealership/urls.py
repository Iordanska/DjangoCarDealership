from django.urls import include, path
from rest_framework import routers

from .views import *

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
    path(
        "api/v1/dealership/<int:pk>/customers", DealershipUniqueCustomersView.as_view()
    ),
    path(
        "api/v1/dealership/<int:pk>/history/customers",
        DealershipCustomerSalesView.as_view(),
    ),
    path(
        "api/v1/dealership/<int:pk>/history/suppliers",
        SupplierDealershipSalesView.as_view(),
    ),
    path("api/v1/dealership/<int:pk>/cars", DealershipCarsView.as_view()),
    path("api/v1/supplier/<int:pk>/history", SupplierDealershipSalesView.as_view()),
    path("api/v1/supplier/<int:pk>/cars", SupplierCarsView.as_view()),
]
