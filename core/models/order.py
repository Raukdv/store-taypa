from core.models import User, Cart
from core.models.shipping_addresses import ShippingAddress
from core.models.promocodes import PromoCode
from core.models.billing_profiles import BillingProfile
from core.models.charges import Charge
from core.constants import ORDER_STATUS

from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _

import uuid
import decimal

class Order(models.Model):

    company = models.ForeignKey(
        'core.Company', null=True, blank=True, on_delete=models.CASCADE, verbose_name=_("Company")
    )

    order_id = models.CharField(max_length=100, null=False, blank=False, unique=True)

    user = models.ForeignKey(
        User, null=False, blank=False, on_delete=models.CASCADE
    )

    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE
    )

    shipping_total = models.DecimalField(default=5, max_digits=8, decimal_places=2)

    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=10, null=True, blank=True, choices=ORDER_STATUS, default='inprogress'
    )

    shipping_address = models.ForeignKey(
        ShippingAddress, null=True, blank=True, on_delete=models.CASCADE
    )

    promo_code = models.OneToOneField(
        PromoCode, null=True, blank=True, on_delete=models.CASCADE
    )

    billing_profile = models.ForeignKey(
        BillingProfile, null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.order_id
    
    def apply_promo_code(self, code):
        if code:
            self.promo_code = code
            self.save()
            code.use()
        else:
            self.update_total()

    def get_or_set_billing_profile(self):
        if self.billing_profile:
            return self.billing_profile

        billing_profile = self.user.billing_profile
        if billing_profile:
            self.update_billing_profile(billing_profile)

        return billing_profile

    def update_billing_profile(self, billing_profile):
        self.billing_profile = billing_profile
        self.save()

    def get_or_set_shipping_address(self):
        if self.shipping_address:
            return self.shipping_address

        shipping_address = self.user.shipping_address
        if shipping_address:
            self.update_shipping_address(shipping_address)

        return shipping_address
    
    def update_shipping_address(self, shipping_address):
        self.shipping_address = shipping_address
        self.save()

    def cancel(self):
        self.status = 'cancelled' 
        self.save()

    def complete(self):
        self.status = 'pending'
        self.save()

    def update_total(self):
        self.total = self.get_total()
        self.save()
    
    def get_total(self):
        return self.cart.total + self.shipping_total - decimal.Decimal(self.get_discount())

    def get_discount(self):
        if self.promo_code:
            return self.promo_code.discount

        return 0
    @property
    def description(self):
        return 'Comprar por ({}) productos'.format(
            self.cart.products.count()
        )

def set_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())

def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()

def charge_by_status(sender, instance, *args, **kwargs):
    if instance.status == 'paid':
        charge = Charge.objects.create_charge(instance)

pre_save.connect(set_order_id, sender=Order)
pre_save.connect(set_total, sender=Order)
pre_save.connect(charge_by_status, sender=Order)
