import django_filters as filters
from django.utils.translation import gettext_lazy as _
from core.models import Product


class ProductFilterSet(filters.FilterSet):
    class Meta:
        fields = {
            'title': ['icontains'],
            'available': ['icontains'],
            'stock': ['icontains'],
        }
        model = Product