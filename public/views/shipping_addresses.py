from django.shortcuts import redirect, get_object_or_404, reverse
from django.contrib import messages
from django.views.generic import ListView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.mixins import LoginRequiredMixin

from core.models import ShippingAddress

from core.views import (
    CompanyMixin,
)

from panel.forms.shipping_addresses import  ShippingAddressForm
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy

from public.tools.order import get_or_create_order
from public.tools.cart import get_or_create_cart
class CompanyShippingAddressListView(CompanyMixin, LoginRequiredMixin, ListView):
    model = ShippingAddress
    template_name = 'public/shipping_adressess/shipping_addresses.html'

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')

    def default(request,pk,slug):
        shipping_address = get_object_or_404(ShippingAddress, pk=pk)

        if request.user.id != shipping_address.user_id:
            return ()

        if request.user.has_shipping_address():
            request.user.shipping_address.update_default()
        
        shipping_address.update_default(True)

        return redirect('public:shippingaddress_view', slug=slug)

class CompanyShippingAddressCreateView(CompanyMixin, LoginRequiredMixin, CreateView):
    model = ShippingAddress
    template_name = 'public/shipping_adressess/create.html'
    form_class = ShippingAddressForm

    def post(self, request, slug):
        form = self.form_class(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = self.request.user
            shipping_address.default = not request.user.has_shipping_address()

            messages.success(request, 'Dirección creada exitosamente')
            shipping_address.save()

            if request.GET.get('next'):
                if request.GET['next'] == reverse_lazy('public:orderaddress_view', args=[slug]):
                    company = self.company
                    cart = get_or_create_cart(request, company)
                    order = get_or_create_order(request, cart, company)

                    order.update_shipping_address(shipping_address)

                    return HttpResponseRedirect(request.GET['next'])

            return redirect('public:shippingaddress_view', slug=slug)

        return HttpResponseRedirect(reverse_lazy('public:shippingaddress_add', args=[slug]))

class CompanyShippingAddressUpdateView(CompanyMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = 'public/shipping_adressess/update.html'
    success_message = 'Dirección actualizada exitosamente'
    
    def get_success_url(self, **kwargs):         
       return reverse_lazy('public:shippingaddress_view', args=[self.company.slug])

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().user_id:
            return HttpResponseRedirect(reverse_lazy('public:shippingaddress_view', args=[kwargs['slug']]))
        return super(CompanyShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)

class CompanyShippingAddressDeleteView(CompanyMixin, LoginRequiredMixin, DeleteView):
    model = ShippingAddress
    template_name = 'public/shipping_adressess/delete.html'

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Dirección eliminada exitosamente')
        return reverse_lazy('public:shippingaddress_view', args=[self.company.slug])

    def dispatch(self, request, *args, **kwargs):

        if self.get_object().default:
            return HttpResponseRedirect(reverse_lazy('public:shippingaddress_view', args=[kwargs['slug']]))

        if request.user.id != self.get_object().user_id:
           return HttpResponseRedirect(reverse_lazy('public:merchant_cart', args=[kwargs['slug']]))

        if self.get_object().has_orders():
            print("Tiene ordenes")
            return HttpResponseRedirect(reverse_lazy('public:shippingaddress_view', args=[kwargs['slug']]))

        return super(CompanyShippingAddressDeleteView, self).dispatch(request, *args, **kwargs)


