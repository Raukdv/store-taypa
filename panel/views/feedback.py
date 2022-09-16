from django.views.generic import DetailView
from django_filters.views import FilterView

from core.views import CompanyQuerySetMixin
from core.models import Feedback
from ..filters.feedback import FeedbackFilterSet


class FeedbackDetailView(CompanyQuerySetMixin, DetailView):
    model = Feedback
    template_name = 'panel/feedback/detail.html'


class FeedbackListView(CompanyQuerySetMixin, FilterView):
    filterset_class = FeedbackFilterSet
    model = Feedback
    paginate_by = 30
    template_name = 'panel/feedback/list.html'
