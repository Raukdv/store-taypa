import django_filters as filters
from django.utils.translation import gettext_lazy as _
from core.models import Order


class OrderFilterSet(filters.FilterSet):
    class Meta:
        fields = {
            'status','user'
        }
        model = Order