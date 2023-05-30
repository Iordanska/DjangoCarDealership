from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(DealershipUniqueCustomers)
admin.site.register(Car)
admin.site.register(DealershipDiscount)
admin.site.register(Dealership)
admin.site.register(DealershipCars)
admin.site.register(Supplier)
admin.site.register(SupplierDiscount)
admin.site.register(SupplierCars)
admin.site.register(Order)
admin.site.register(DealershipCustomerSales)
admin.site.register(SupplierUniqueCustomers)
