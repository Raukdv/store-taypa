
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    DetailView
)

from core.models import Product
from core.views import (
    CompanyMixin,
)
class CompanyProductDetailView(CompanyMixin, DetailView):
    model = Product
    template_name = 'public/product/product_detail.html'
    slug_url_kwarg = 'product_slug'
    slug_field = 'slug'

