from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView, DeleteView, DetailView, UpdateView
)
from django_filters.views import FilterView

from core.models import Customer
from core.views import (
    CompanyCreateMixin,
    CompanyQuerySetMixin
)
from ..filters.customer import CustomerFilterSet
from ..forms.customer import CustomerForm

class CustomerCreateView(CompanyCreateMixin, CreateView):
    form_class = CustomerForm
    model = Customer
    template_name = 'panel/customer/form.html'

    def get_success_url(self):
        return reverse_lazy(
            'panel:customer_detail',
            args=[self.company.slug, self.object.id]
        )


class CustomerDeleteView(CompanyQuerySetMixin, DeleteView):
    model = Customer
    template_name = 'panel/customer/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('panel:customer_list', args=[self.company.slug])


class CustomerDetailView(CompanyQuerySetMixin, DetailView):
    model = Customer
    template_name = 'panel/customer/detail.html'


class CustomerListView(CompanyQuerySetMixin, FilterView):
    filterset_class = CustomerFilterSet
    model = Customer
    paginate_by = 30
    template_name = 'panel/customer/list.html'


class CustomerUpdateView(CompanyQuerySetMixin, UpdateView):
    form_class = CustomerForm
    model = Customer
    template_name = 'panel/customer/form.html'

    def get_success_url(self):
        return reverse_lazy(
            'panel:customer_detail',
            args=[self.company.slug, self.object.id]
        )


class CustomerSendSMSView(CompanyQuerySetMixin, DetailView):
    model = Customer

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            response = self.object._send_sms(
                scheme=request.scheme,
                host=request.get_host()
            )
            if response:
                messages.error(request, response)
            else:
                messages.success(
                    request, _("SMS message was send successfully.")
                )
        except ValidationError as err:
            messages.error(request, str(err))

        url = reverse_lazy(
            'panel:customer_detail',
            args=[self.company.slug, self.object.id]
        )

        return HttpResponseRedirect(url)
