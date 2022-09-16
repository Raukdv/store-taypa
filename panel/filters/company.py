import django_filters as filters

from core.models import Company

class CompanyFilterSet(filters.FilterSet):
    class Meta:
        fields = {
            'name': ['icontains'],
        }
        model = Company