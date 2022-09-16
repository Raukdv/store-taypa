from public.tools.order import get_or_create_order
from public.tools.cart import get_or_create_cart

def validate_cart_and_order(function):
    def wrap(self, request, *args, **kwarg):
        cart = get_or_create_cart(request, self.company)
        order = get_or_create_order(request, cart, self.company)
        return function(self, request, cart, order, *args, **kwarg)
    return wrap   



