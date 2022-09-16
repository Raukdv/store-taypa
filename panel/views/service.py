from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.models import Service
from ..forms.service import ServiceForm

class ServiceCreateView(PermissionRequiredMixin, CreateView):
    form_class = ServiceForm
    model = Service
    template_name = 'panel/service/form.html'
    permission_required = 'core:add_service'
    success_url = reverse_lazy('panel:service_list')


class ServiceDeleteView(PermissionRequiredMixin, DeleteView):
    model = Service
    permission_required = 'core:delete_service'
    success_url = reverse_lazy('panel:service_list')
    template_name = 'panel/service/confirm_delete.html'


class ServiceListView(PermissionRequiredMixin, ListView):
    model = Service
    paginate_by = 30
    permission_required = 'core:change_service'
    template_name = 'panel/service/list.html'


class ServiceUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = ServiceForm
    model = Service
    permission_required = 'core:change_service'
    template_name = 'panel/service/form.html'
    success_url = reverse_lazy('panel:service_list')
