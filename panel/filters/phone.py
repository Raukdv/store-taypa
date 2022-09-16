import django_filters as filters

from core.models import Phone


class PhoneFilterSet(filters.FilterSet):
    company = filters.CharFilter(
        field_name='company__name', lookup_expr='icontains'
    )

    class Meta:
        fields = {
            'phone': ['icontains'],
            'company': []
        }
        model = Phone
