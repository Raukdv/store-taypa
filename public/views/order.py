from django.views.generic import (TemplateView, ListView
)

from django.contrib.auth.mixins import LoginRequiredMixin


from core.views import (
    CompanyMixin,
)

from .decorators import validate_cart_and_order
from mails.mails import Mail
from public.tools.order import get_or_create_order, breadcrumb, destroy_order
from public.tools.cart import get_or_create_cart, destroy_cart
from django.shortcuts import redirect, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages


from core.models import Company, ShippingAddress, Charge
import threading

class CompanyOrderListView(CompanyMixin, LoginRequiredMixin, ListView):
    template_name = 'public/order/orders.html'

    def get_queryset(self):
        return self.request.user.orders_completed()


class CompanyOrderView(CompanyMixin, LoginRequiredMixin, TemplateView):
    template_name = 'public/order/order.html'

    @validate_cart_and_order
    def get(self, request, cart, order, *args, **kwargs):
        company = self.company
        
        if not cart.has_products():
            return redirect('public:merchant_cart', slug=company.slug)

        
        return self.render_to_response(
            self.get_context_data(company=company,
                order=order,
                cart=cart, 
                breadcrumb=breadcrumb(company)
                )
            )
class CompanyAddressOrderView(CompanyMixin, LoginRequiredMixin, TemplateView):
    template_name = 'public/order/address.html'
    
    @validate_cart_and_order
    def get(self, request, cart, order, *args, **kwargs):
  
        company = self.company

        if not cart.has_products():
            return redirect('public:merchant_cart', slug=company.slug)

        shipping_address = order.get_or_set_shipping_address()
        
        can_choose_address = request.user.has_shipping_addresses()

        return self.render_to_response(
            self.get_context_data(
                company=company,
                order=order,
                cart=cart,
                can_choose_address=can_choose_address,
                shipping_address=shipping_address,
                breadcrumb=breadcrumb(company, address=True)
                )
            )
class CompanySelectAddressOrderView(CompanyMixin, LoginRequiredMixin, TemplateView):
    template_name = 'public/order/select_address.html'

    def get(self, request, slug):
        company = self.company

        shipping_addresses = request.user.addresses
        
        return self.render_to_response(
            self.get_context_data(
                company=company,
                shipping_addresses=shipping_addresses,
                breadcrumb=breadcrumb(company, address=True)
                )
            )

class CompanyCheckAddressOrderView(CompanyMixin, LoginRequiredMixin, TemplateView):
    template_name = 'public/order/select_address.html'
    @validate_cart_and_order
    def get(self, request, slug, pk):

        shipping_address = get_object_or_404(ShippingAddress, pk=pk)

        company = self.company

        if request.user.id != shipping_address.user_id:
            return redirect('public:merchant_cart', slug=slug)
        
        order.update_shipping_address(shipping_address)

        return HttpResponseRedirect(reverse_lazy('public:orderaddress_view', args=[slug]))
  
class CompanyConfirmOrderView(CompanyMixin, LoginRequiredMixin, TemplateView):
    template_name = 'public/order/confirm.html'
    
    @validate_cart_and_order
    def get(self, request, cart, order, *args, **kwargs):
        company = self.company
        shipping_address = order.shipping_address

        
        if not cart.has_products() or order.shipping_address is None or order.billing_profile is None:
            return HttpResponseRedirect(reverse_lazy('public:order_view', args=[company.slug]))

        if shipping_address is None:
            return HttpResponseRedirect(reverse_lazy('public:orderaddress_view', args=[company.slug]))

        return self.render_to_response(
            self.get_context_data(
                company=company,
                order=order,
                cart=cart,
                shipping_address=shipping_address,
                breadcrumb=breadcrumb(company, confirmation=True)
                )
            )
class CompanyCancelOrderView(CompanyMixin, LoginRequiredMixin, TemplateView):
    template_name = 'public/order/confirm.html'  

    @validate_cart_and_order
    def get(self, request, cart, order, *args, **kwargs):
        company = self.company

        if request.user.id != order.user_id:
            return HttpResponseRedirect(reverse_lazy('public:orderaddress_view', args=[company.slug]))
        
        order.cancel() 
        destroy_cart(request)
        destroy_order(request)

        messages.error(request, 'Orden cancelada')
        return HttpResponseRedirect(reverse_lazy('public:merchant_detail', args=[company.slug]))    

class CompanyCompleteOrderView(CompanyMixin, LoginRequiredMixin, TemplateView):
    template_name = 'public/order/confirm.html'  

    @validate_cart_and_order
    def get(self, request, cart, order, *args, **kwargs):
        company = self.company

        if request.user.id != order.user_id:
            return HttpResponseRedirect(reverse_lazy('public:orderaddress_view', args=[company.slug]))
        
        #DESCOMENTAR ESTO PARA HACER EL COBRO AUTOMATICO DESDE LA APP    
        #charge = Charge.objects.create_charge(order)
        #if charge:
        
        order.complete()
        
        thread = threading.Thread(target=Mail.send_complete_order, args=(company, order, request.user))
        thread.start()

        destroy_cart(request)
        destroy_order(request)

        messages.success(request, 'Orden completada exitosamente')
        return HttpResponseRedirect(reverse_lazy('public:merchant_detail', args=[company.slug]))

class CompanyPaymentOrderView(CompanyMixin, LoginRequiredMixin, TemplateView):
    template_name = 'public/order/payment.html'  

    @validate_cart_and_order
    def get(self, request, cart, order, *args, **kwargs):
        company = self.company

        if not cart.has_products() or order.shipping_address is None:
            messages.error(request, 'No posee productos ni direccion de envio.')
            return HttpResponseRedirect(reverse_lazy('public:order_view', args=[company.slug]))
        
        billing_profile = order.get_or_set_billing_profile()

        return self.render_to_response(
            self.get_context_data(
                company=company,
                order=order,
                cart=cart,
                billing_profile=billing_profile,
                breadcrumb=breadcrumb(company, address=True, payment=True),
                )
            )
