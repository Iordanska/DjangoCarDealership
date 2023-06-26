from django.contrib import admin

from dealership.models import *

admin.site.register(Customer)
admin.site.register(DealershipUniqueCustomers)
admin.site.register(Car)
admin.site.register(DealershipDiscount)
admin.site.register(Dealership)
admin.site.register(DealershipCars)
admin.site.register(Supplier)
admin.site.register(SupplierDiscount)
admin.site.register(SupplierCars)
admin.site.register(DealershipCustomerSales)
admin.site.register(SupplierUniqueCustomers)
