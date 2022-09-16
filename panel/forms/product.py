from django import forms

from core.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        exclude = (
            'company', 'last_updated', 'slug'
        )
        model = Product