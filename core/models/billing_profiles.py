from django.db import models
from core.models.user import User

from core.constants import TYPE_PAYMENT
from paymentsAPI.stripe.card import create_card
class BillingProfileManager(models.Manager):
    
    def create_by_stripe_token(self, user, stripe_token):
        if user.has_customer() and stripe_token:
            source = create_card(user, stripe_token)

            return self.create(card_id=source.id,
                                last4=source.last4,
                                token=stripe_token,
                                brand=source.brand,
                                user=user,
                                type_payment='stripe',
                                default=not user.has_billing_profiles()
                            )

class BillingProfile(models.Model):

    type_payment = models.CharField(choices=TYPE_PAYMENT, max_length=50, null=False, blank=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    token = models.CharField(max_length=50, null=False, blank=False)

    card_id = models.CharField(max_length=50, null=False, blank=False)

    last4 = models.CharField(max_length=4, null=False, blank=False)

    brand = models.CharField(max_length=10, null=False, blank=False)

    default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.card_id