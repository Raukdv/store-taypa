from django.db.models import Q
from django.utils.translation import gettext_lazy as _
import django_filters as filters

from core.models import Message
from .filters import DateTimeFromToRangeFilter


class MesageFilterSet(filters.FilterSet):
    date_creation = DateTimeFromToRangeFilter()
    from_ = filters.CharFilter(
        label=_("From"), method='filter_from'
    )
    to = filters.CharFilter(
        label=_("To"), method='filter_to'
    )

    class Meta:
        fields = ('date_creation', 'from_', 'to', 'type', 'direction')
        model = Message

    def filter_from(self, queryset, name, value):
        queryset = queryset.filter(
            Q(from_number__icontains=value)
            | Q(from_email__icontains=value)
        )
        return queryset

    def filter_to(self, queryset, name, value):
        queryset = queryset.filter(
            Q(to_number__icontains=value)
            | Q(to_email__icontains=value)
        )
        return queryset
