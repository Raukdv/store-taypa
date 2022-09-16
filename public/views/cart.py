from django.views.generic import (TemplateView
)

from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.urls import reverse_lazy

from core.views import (
    CompanyMixin,
)

from public.tools.cart import get_or_create_cart
from core.models import Product, Company, CartProducts

class CompanyMerchantCartView(CompanyMixin, TemplateView):
    template_name = 'public/cart/cart.html'

    def get(self, request, *args, **kwargs):
        
        company = self.company
        cart = get_or_create_cart(request, company)

        return self.render_to_response(self.get_context_data(company=company, cart=cart))

def add(request, slug):
    company = get_object_or_404(Company, slug=slug)
    cart = get_or_create_cart(request, company)
        
    if request.method == 'POST':
        id_product = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=id_product)
        quantity = int(request.POST.get('quantity', 1))
        
        #cart.products.add(product, through_defaults={'quantity':quantity})

        cart_procut = CartProducts.objects.create_or_update_quantity(cart=cart, product=product, quantity=quantity)
        messages.success(request, 'El Producto fue agregado.')
        return render(request, 'public/cart/cart_added.html', {
            'quantity':quantity,
            'product':product,
            'company':company
        })
    else:
        messages.warning(request, 'El Producto no pudo ser agregado.')
        return HttpResponseRedirect(reverse_lazy('public:merchant_detail', args=[slug]))

def remove(request, slug):

    company = get_object_or_404(Company, slug=slug)
    cart = get_or_create_cart(request, company)

    if request.method == 'POST':
        id_product = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=id_product)
        cart.products.remove(product)
        messages.success(request, 'El Producto: {}, fue eliminado.'.format(product.title))
        return HttpResponseRedirect(reverse_lazy('public:merchant_cart', args=[slug]))
    else:
        messages.warning(request, 'El Producto no pudo ser eliminado.')
        return HttpResponseRedirect(reverse_lazy('public:merchant_detail', args=[slug]))
