from django.shortcuts import render

from django.http import JsonResponse

from core.models import PromoCode, Company

from public.tools.order import get_or_create_order
from public.tools.cart import get_or_create_cart

def validate(request, slug):

    company = Company.objects.get(slug=slug)
    cart = get_or_create_cart(request, company)
    order = get_or_create_order(request, cart, company)

    code = request.GET.get('code')
    promo_code = PromoCode.objects.get_valid(code)

    if promo_code is None:
        return JsonResponse(
            {
            'status': False
            }, 
            status=404
        )

    order.apply_promo_code(promo_code)
    # order.promo_code = promo_code
    # order.save()
    
    return JsonResponse({
        'status': True,
        'code': promo_code.code,
        'discount': promo_code.discount,
        'total': order.total
    })
