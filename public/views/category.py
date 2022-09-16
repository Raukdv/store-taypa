
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    DetailView
)

from core.models import Category
from core.views import (
    CompanyMixin,
)


class CompanyCategoryDetailView(CompanyMixin, DetailView):
    model = Category
    template_name = 'public/category/category_detail.html'
    slug_url_kwarg = 'category_slug'
    slug_field = 'title'

