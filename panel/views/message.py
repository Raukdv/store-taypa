from django.views.generic import DetailView
from django_filters.views import FilterView

from core.models import Message
from core.views import CompanyQuerySetMixin
from ..filters.message import MesageFilterSet
class MessageDetailView(CompanyQuerySetMixin, DetailView):
    model = Message
    template_name = 'panel/message/detail.html'

class MessageListView(CompanyQuerySetMixin, FilterView):
    filterset_class = MesageFilterSet
    model = Message
    paginate_by = 30
    template_name = 'panel/message/list.html'
