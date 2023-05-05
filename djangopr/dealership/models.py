from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField

class TrackableMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract: True

class Car(TrackableMixin):
    model = models.CharField(max_length=100)
    characteristics  = models.JSONField()
    

    def __str__(self):
        return self.model

class Supplier(TrackableMixin):
    company_name = models.CharField(max_length=100)
    date_of_foundation = models.DateTimeField(blank=True)
    number_of_buyers = models.IntegerField(default=0, editable=False)
    specification = models.JSONField()
    cars = models.ManyToManyField(Car, through='SupplierCars')

    def __str__(self):
        return self.company_name
    
class Dealership(TrackableMixin):
    company_name = models.CharField(max_length=100)
    location = CountryField()
    specification =models.JSONField()
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', editable=False)
    cars = models.ManyToManyField(Car, through='DealershipCars')

    def __str__(self):
        return self.company_name


class SupplierCars(TrackableMixin):
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    car = models.ForeignKey(Car,  on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    quantity = models.PositiveIntegerField(default =0)

    def __str__(self):
        return self.company_name


class DealershipCars(TrackableMixin):
    dealership_id = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    car  =models.ForeignKey(Car, on_delete=models.CASCADE)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price =MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    quantity = models.PositiveIntegerField(default =0)


class CustomerProfile(TrackableMixin):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', editable=False)

    def __str__(self):
        return str(self.name) + ' ' + str(self.surname)


class Offer(TrackableMixin):
    customer_id = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    max_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    def __str__(self):
        return self.pk



class DealershipDiscount(TrackableMixin):
    dealership_id = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    discount_start = models.DateTimeField()
    discount_end = models.DateTimeField()
    discount = models.DecimalField(max_digits=3, decimal_places=2)
    discount_name = models.CharField(max_length=100)
    discount_description = models.TextField()
    def __str__(self):
        return self.pk


class DealershipUniqueCustomers(TrackableMixin):
    dealership_id = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    number_of_purchases = models.PositiveIntegerField(default =0)

    def __str__(self):
        return self.customer_id




class SupplierDiscount(TrackableMixin):
    supplier_id = models.OneToOneField(Supplier, primary_key=True, on_delete=models.CASCADE)
    required_number_of_purchases = models.PositiveIntegerField()
    primary_client_discount = models.DecimalField(max_digits=3, decimal_places=2, blank=True)

    def __str__(self):
        return self.pk


class SupplierSales(TrackableMixin):
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    dealership_id = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    sale_date = models.DateTimeField(auto_now=True)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    def __str__(self):
        return self.pk


class SupplierUniqueCustomers(TrackableMixin):
    dealership_id = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    is_regular_customer = models.BooleanField(default=False)
    number_of_purchases = models.PositiveIntegerField(default=0),
    discount = models.DecimalField(max_digits=3, decimal_places=2, blank=True)

    def __str__(self):
        return self.dealership_id


