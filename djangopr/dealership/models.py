from django.db import models


class Supplier(models.Model):
    id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=100)
    date_of_foundation = models.DateTimeField()
    number_of_buyers = models.IntegerField()
    stock_id = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)

    created= models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


class Dealership(models.Model):
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    cars_type = models.CharField(max_length=100)
    balance = models.FloatField()
    stock_id = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name



class Car(models.Model):
    id = models.IntegerField(primary_key=True)
    model = models.CharField(max_length=100)
    supplier = models.ManyToManyField(Supplier)
    drive_type = models.CharField(max_length=100)
    engine_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.model


class CustomerProfile(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    balance = models.FloatField()
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name) + ' ' + str(self.surname)


class Offer(models.Model):
    id = models.IntegerField(primary_key=True)
    customer_id = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    max_price = models.FloatField()
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pk

class CarFeatures(models.Model):
    dealership_id = models.OneToOneField(Dealership, primary_key=True, on_delete=models.CASCADE)
    drive_type = models.CharField(max_length=100)
    engine_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class DealershipCarList(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    dealership_id = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    popularity = models.FloatField()
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supplier_price = models.FloatField()
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class DealershipDiscount(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    dealership_id = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    discount_start = models.DateTimeField()
    discount_end = models.DateTimeField()
    discount = models.FloatField()
    discount_name = models.CharField(max_length=100)
    discount_description = models.TextField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pk


class DealershipCustomers(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    dealership_id = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    number_of_purchases = models.IntegerField()
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_id


class DealershipStock(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    stock_id = models.ForeignKey(Dealership, to_field="stock_id", on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pk


class SupplierDiscount(models.Model):
    supplier_id = models.OneToOneField(Supplier, primary_key=True, on_delete=models.CASCADE)
    required_number_of_purchases = models.IntegerField()
    primary_client_discount = models.FloatField()
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pk


class SupplierSales(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    dealership_id = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    sale_date = models.DateTimeField(auto_now=True)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    price = models.FloatField()
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pk


class SupplierCustomers(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    dealership_id = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    is_regular_customer = models.BooleanField(default=False)
    number_of_purchases = models.IntegerField()
    discount = models.FloatField(blank=True)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dealership_id


class SupplierStock(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    stock_id = models.ForeignKey(Supplier, to_field="stock_id", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.stock_id
