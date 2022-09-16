from core.models import User
from django.db import models
from django_countries.fields import CountryField

class ShippingAddress(models.Model):
    user = models.ForeignKey(
        User, null=False, blank=False, on_delete=models.CASCADE
    )
    address_1 = models.TextField(
        max_length=200, blank=True, null=True
    )
    address_2 = models.TextField(
        max_length=200, blank=True, null=True
    )
    city = models.CharField(
        max_length=100
    )
    state = models.CharField(
        max_length=100
    )
    country = CountryField(
        blank=True, null=True, default='PE'
    )
    reference = models.CharField(
        max_length=300
    )
    postal_code = models.CharField(
        max_length=10, null=False, blank=False
    )
    default = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.postal_code

    def update_default(self, default=False):
        self.default = default
        self.save()
    
    def has_orders(self):
        return self.order_set.count() >= 1

    @property
    def address(self):
        return '{} - {} - {}'.format(self.city, self.state, self.country)



