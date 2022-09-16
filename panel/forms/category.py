from itertools import product
from django import forms

from core.models import Category, Product

def get_category_form(company):

    class CategoryForm(forms.ModelForm):
        
        products = forms.ModelMultipleChoiceField(
            queryset=Product.objects.filter(company=company)
            )

        class Meta:
            exclude = (
                'company',
            )
            model = Category

    return CategoryForm