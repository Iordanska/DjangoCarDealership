from django.db import models
from rest_framework.mixins import DestroyModelMixin


class BaseTimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseActiveModel(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class DateAndActiveMixin(BaseTimestampedModel, BaseActiveModel):

    """
    Mixin that provides fields created, updated and is_active

    Includes
        - BaseTimestampedModel
        - BaseActivedModel
    """

    class Meta:
        abstract = True


class CustomDestroyModelMixin(DestroyModelMixin):

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
