
from core.models import Order
from django.urls import reverse_lazy

def get_or_create_order(request, cart, company):
    order = cart.order

    if order is None and request.user.is_authenticated:
        order = Order.objects.create(company=company, cart=cart, user=request.user)

    if order:
        request.session['order_id'] = order.order_id

    return order

def destroy_order(request):
    request.session['order_id'] = None

def breadcrumb(company, products=True, address=False, payment=False, confirmation=False):
    return [
        {'title':'Productos','active':products,'url': reverse_lazy('public:order_view', args=[company.slug])},
        {'title':'Dirección','active':address,'url':reverse_lazy('public:orderaddress_view', args=[company.slug])},
        {'title':'Pago','active':payment,'url':reverse_lazy('public:order_view', args=[company.slug])},
        {'title':'Confirmación','active':confirmation,'url':reverse_lazy('public:order_confirm', args=[company.slug])}
    ]