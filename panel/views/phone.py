from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    DeleteView, DetailView, FormView, View, UpdateView
)
from django_filters.views import FilterView

from core.models import Phone
from ..filters.phone import PhoneFilterSet
from ..forms.phone import PhoneForm, PhoneSearchForm

class PhoneChangeView(PermissionRequiredMixin, UpdateView):
    form_class = PhoneForm
    model = Phone
    permission_required = 'core:change_phone'
    success_url = reverse_lazy('panel:phone_list')
    template_name = 'panel/phone/form.html'


class PhoneConnectView(PermissionRequiredMixin, DetailView):
    model = Phone
    permission_required = 'core:change_phone'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.object.connect(request=request)
        if response:
            messages.error(request, response)
        else:
            messages.success(request, _("Phone connected successfully."))
        return HttpResponseRedirect(reverse_lazy('panel:phone_list'))


class PhoneDeleteView(PermissionRequiredMixin, DeleteView):
    model = Phone
    permission_required = 'core:delete_phone'
    success_url = reverse_lazy('panel:phone_list')
    template_name = 'panel/phone/confirm_delete.html'


class PhoneListView(PermissionRequiredMixin, FilterView):
    filterset_class = PhoneFilterSet
    model = Phone
    paginate_by = 30
    permission_required = 'core:change_phone'
    template_name = 'panel/phone/list.html'


class PhoneSearchView(PermissionRequiredMixin, FormView):
    form_class = PhoneSearchForm
    permission_required = 'core:add_phone'
    template_name = 'panel/phone/search.html'

    def form_valid(self, form):
        object_list = form.save()
        if isinstance(object_list, list):
            return self.render_to_response(
                self.get_context_data(object_list=object_list)
            )

        messages.error(self.request, object_list)
        return self.render_to_response(self.get_context_data())


class PhonePurchaseView(PermissionRequiredMixin, View):
    model = Phone
    permission_required = 'core:add_phone'

    def get_phone(self):
        try:
            return self.request.GET['phone']
        except KeyError:
            return

    def get(self, request, *args, **kwargs):
        phone = self.get_phone()
        if not phone:
            return PermissionDenied

        response = self.model.objects.purchase(request=request, phone=phone)

        if isinstance(response, self.model):
            messages.success(
                request,
                _("Phone %(phone)s has been purchased successfully.") % dict(
                    phone=response
                )
            )
            return HttpResponseRedirect(reverse_lazy('panel:phone_list'))

        messages.error(request, response)
        return HttpResponseRedirect(reverse_lazy('panel:phone_search'))


class PhoneSyncView(PermissionRequiredMixin, View):
    model = Phone
    permission_required = 'core:change_phone'

    def get(self, request, *args, **kwargs):
        response = self.model.objects.sync(request=request)
        if isinstance(response, list):
            messages.success(request, _("Phone list synced successfully."))
        else:
            messages.error(request, response)
        return HttpResponseRedirect(reverse_lazy('panel:phone_list'))
