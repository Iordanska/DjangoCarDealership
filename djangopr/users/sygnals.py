from django.db.models.signals import  post_save
from django.dispatch import receiver

from dealership.models import Customer, Dealership, Supplier
from users.models import User

#
@receiver(signal=post_save, sender=User)
def profile_handler(sender,instance, created,*args,**kwargs):
        if created:
            if instance.role == 'Customer':
                Customer.objects.create(user=instance)
            if instance.role == 'Dealership':
                Dealership.objects.create(user=instance)
            if instance.role == 'Supplier':
                Supplier.objects.create(user=instance)