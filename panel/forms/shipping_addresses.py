from django.forms import ModelForm
from core.models import ShippingAddress





class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'address_1', 'address_2', 'city','state','postal_code','reference'
        ]
