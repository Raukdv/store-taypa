from django.db.models import Q
import django_filters as filters

from core.models import Feedback
from .filters import DateTimeFromToRangeFilter


class FeedbackFilterSet(filters.FilterSet):
    date_creation = DateTimeFromToRangeFilter()
    customer = filters.CharFilter(method='filter_customer')

    class Meta:
        fields = (
            'date_creation', 'customer', 'service'
        )
        model = Feedback

    def filter_customer(self, queryset, name, value):
        queryset = queryset.filter(
            Q(customer__first_name__icontains=value)
            | Q(customer__last_name__icontains=value)
        )
        return queryset
