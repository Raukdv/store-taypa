import django_filters as filters

from core.models import Customer


class CustomerFilterSet(filters.FilterSet):
    class Meta:
        fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'email': ['icontains'],
            'phone': ['icontains'],
        }
        model = Customer
