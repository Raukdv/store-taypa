import django_filters as filters
from django.utils.translation import gettext_lazy as _
from core.models import Category


class CategoryFilterSet(filters.FilterSet):
    class Meta:
        fields = {
            'title': ['icontains'],
        }
        model = Category