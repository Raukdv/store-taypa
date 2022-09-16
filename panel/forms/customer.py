from django import forms

from core.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        exclude = (
            'company',
        )
        model = Customer
