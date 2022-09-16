from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView, DeleteView, DetailView, UpdateView
)
from django_filters.views import FilterView

from core.models import Product
from core.views import (
    CompanyCreateMixin,
    CompanyQuerySetMixin
)

from ..filters.product import ProductFilterSet
from ..forms.product import ProductForm
class ProductCreateView(CompanyCreateMixin, CreateView):
    form_class = ProductForm
    model = Product
    template_name = 'panel/product/form.html'

    def get_success_url(self):
        return reverse_lazy(
            'panel:product_detail',
            args=[self.company.slug, self.object.id]
        )

class ProductDeleteView(CompanyQuerySetMixin, DeleteView):
    model = Product
    template_name = 'panel/product/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('panel:product_list', args=[self.company.slug])

class ProductDetailView(CompanyQuerySetMixin, DetailView):
    model = Product
    template_name = 'panel/product/detail.html'

class ProductListView(CompanyQuerySetMixin, FilterView):
    filterset_class = ProductFilterSet
    model = Product
    paginate_by = 30
    ordering = ['-id']
    template_name = 'panel/product/list.html'

class ProductUpdateView(CompanyQuerySetMixin, UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'panel/product/form.html'

    def get_success_url(self):
        return reverse_lazy(
            'panel:product_detail',
            args=[self.company.slug, self.object.id]
        )
