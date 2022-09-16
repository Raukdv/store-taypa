from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView, DeleteView, DetailView, UpdateView
)
from django_filters.views import FilterView

from core.models import Category

from core.views import (
    CompanyCreateMixin,
    CompanyQuerySetMixin
)
from ..filters.category import CategoryFilterSet
from ..forms.category import get_category_form

class CategoryCreateView(CompanyCreateMixin, CreateView):
    model = Category
    template_name = 'panel/category/form.html'

    def get_form_class(self):
        return get_category_form(self.company)

    def get_success_url(self):
        return reverse_lazy(
            'panel:category_detail',
            args=[self.company.slug, self.object.id]
        )

class CategoryDeleteView(CompanyQuerySetMixin, DeleteView):
    model = Category
    template_name = 'panel/category/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('panel:category_list', args=[self.company.slug])

class CategoryDetailView(CompanyQuerySetMixin, DetailView):
    model = Category
    template_name = 'panel/category/detail.html'

class CategoryListView(CompanyQuerySetMixin, FilterView):
    template_name = 'panel/category/list.html'
    filterset_class = CategoryFilterSet
    model = Category
    paginate_by = 30
    ordering = ['-id']  
class CategoryUpdateView(CompanyQuerySetMixin, UpdateView):
    model = Category
    template_name = 'panel/category/form.html'

    def get_form_class(self):
        return get_category_form(self.company)

    def get_success_url(self):
        return reverse_lazy(
            'panel:category_detail',
            args=[self.company.slug, self.object.id]
        )
