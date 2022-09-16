from django import forms

from core.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        exclude = (
            'status', 'user'
        )
        model = Order