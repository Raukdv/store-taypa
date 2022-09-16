from boilerplate.mixins import ExtraFormsAndFormsetsMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView

from core.models import Company
from core.views import (
    CompanyCreateMixin,
    CollaboratorRequiredMixin,
    UserCreateMixin
)
from ..forms.company import (
    CompanyForm,
    CompanyChildForm,
    CompanyEmptyForm,
    CompanyLinkFormSet,
    CompanyMessagesForm
)

class CompanyCreateView(PermissionRequiredMixin, CreateView):
    form_class = CompanyForm
    model = Company
    permission_required = 'core:add_company'
    template_name = 'panel/company/form.html'

class CompanyChildCreateView(
    CompanyCreateMixin, UserCreateMixin, CreateView
):
    company_field = 'parent_company'
    form_class = CompanyChildForm
    model = Company
    template_name = 'panel/company/form.html'

class CompanyUpdateView(
    CollaboratorRequiredMixin, UpdateView
):
    form_class = CompanyChildForm
    model = Company
    template_name = 'panel/company/form.html'
    slug_url_kwarg = 'company'

class CompanyUpdateLinksView(
    ExtraFormsAndFormsetsMixin, CollaboratorRequiredMixin, UpdateView
):
    form_class = CompanyEmptyForm
    formset_list = (
        CompanyLinkFormSet,
    )
    model = Company
    template_name = 'panel/company/form.html'
    slug_url_kwarg = 'company'

class CompanyUpdateMessagesView(
    CollaboratorRequiredMixin, UpdateView
):
    form_class = CompanyMessagesForm
    model = Company
    template_name = 'panel/company/form.html'
    slug_url_kwarg = 'company'
