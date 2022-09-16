from core.models import Cart

def get_or_create_cart(request, company):
    user = request.user if request.user.is_authenticated else None #/Obtener informacion del usuario en cuestion 
    
    cart_id = request.session.get('cart_id') #None si no se encuentra /obtener el id del carrito
    
    cart = Cart.objects.filter(company=company, cart_id=cart_id).first() #[] -> first devuelve None si no cumple con la condicion 
    
    #/Consultar y traer carrito existente

    if cart is None: #Para cuando no exista un carrito para un ususario anonimo o autenticado
        cart = Cart.objects.create(user=user, company=company)
        
        if user and cart.user is None: #Para cuando exista un usuario autenticado pero no posea carrito
            cart.user = user
            cart.company = company
            cart.save()
            
    request.session['cart_id'] = cart.cart_id #se puede usar pk o cart_id #/Creacion de sesion
        
    return cart

def destroy_cart(request):
    request.session['cart_id'] = None