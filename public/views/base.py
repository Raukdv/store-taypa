import json
import requests as rq
from formtools.wizard.views import SessionWizardView
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from core.models import Company, User, ShippingAddress
from panel.filters.company import CompanyFilterSet
from django_filters.views import FilterView

from panel.forms.user import UserAddressForm, UserCreateForm
from public.tools.base import get_or_set_geolocation

class IndexView(FilterView):
    filterset_class = CompanyFilterSet
    model = Company
    paginate_by = 30
    ordering = ['-id']
    template_name = 'public/index.html'

    def get_queryset(self):

        get_or_set_geolocation(self.request)

        if self.request.session.get('country') and self.request.session.get('city') and self.request.session.get('state'):
            company = self.model.objects.filter(
            Q(country__icontains=self.request.session.get('country')) | #Requerido en el modelo
            Q(city__icontains=self.request.session.get('city')) | #Requerido en el modelo
            Q(state__icontains=self.request.session.get('state')) | #Requerido en el modelo
            Q(address__icontains=self.request.session.get('country')) | #Todo address requerido en el modelo
            Q(address__icontains=self.request.session.get('state')) |
            Q(address__icontains=self.request.session.get('city'))
            )

            return company
        else:
            return Company.objects.all()
            
class SignUpAsMerchant(SessionWizardView):
    template_name = 'public/users/register.html'
    form_list = [UserCreateForm, UserAddressForm]
    
    def done(self, form_list, **kwargs):
        general_form = form_list[0]
        address_form = form_list[1]
        # get all data
        first_name = general_form.cleaned_data['first_name']
        last_name = general_form.cleaned_data['last_name']
        email = general_form.cleaned_data['email']
        pwd = general_form.cleaned_data['password1']
        # create and modify user
        user = User.objects._create_user(email=email, password=pwd)
        user.first_name = first_name
        user.last_name = last_name
        user.is_merchant = True
        user.save()

        #create and modify shipping address
        shipping_address = ShippingAddress.objects.create(
            user=user,
            address_1=address_form.cleaned_data['address_1'],
            address_2=address_form.cleaned_data['address_2'],
            city=address_form.cleaned_data['city'],
            state=address_form.cleaned_data['state'],
            country=address_form.cleaned_data['country'],
            reference=address_form.cleaned_data['reference'],
            postal_code=address_form.cleaned_data['postal_code'],
            default=address_form.cleaned_data['default']
        )
        shipping_address.save()
        return HttpResponseRedirect(reverse_lazy('panel:index'))

class SignUpAsCustomer(SessionWizardView):
    template_name = 'public/users/register.html'
    form_list = [UserCreateForm, UserAddressForm]
    def done(self, form_list, **kwargs):
        general_form = form_list[0]
        address_form = form_list[1]
        # get all data
        first_name = general_form.cleaned_data['first_name']
        last_name = general_form.cleaned_data['last_name']
        email = general_form.cleaned_data['email']
        pwd = general_form.cleaned_data['password1']
        # create and modify user
        user = User.objects._create_user(email=email, password=pwd)
        user.first_name = first_name
        user.last_name = last_name
        user.is_customer = True
        user.save()

        #create and modify shipping address
        shipping_address = ShippingAddress.objects.create(
            user=user,
            address_1=address_form.cleaned_data['address_1'],
            address_2=address_form.cleaned_data['address_2'],
            city=address_form.cleaned_data['city'],
            state=address_form.cleaned_data['state'],
            country=address_form.cleaned_data['country'],
            reference=address_form.cleaned_data['reference'],
            postal_code=address_form.cleaned_data['postal_code'],
            default=address_form.cleaned_data['default']
        )
        shipping_address.save()
        return HttpResponseRedirect(reverse_lazy('panel:index'))