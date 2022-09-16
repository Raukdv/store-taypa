from django.db import models
from django.db.models.signals import pre_save, m2m_changed, post_save
from core.models import Product, User

from django.utils.translation import ugettext_lazy as _
import uuid
import decimal

#Cart Product Manager
class CartProductsManager(models.Manager):
    def create_or_update_quantity(self, cart, product, quantity=1):
        object, created = self.get_or_create(cart=cart, product=product)
        
        if not created:
            quantity = object.quantity + quantity

        object.update_quantity(quantity)
        return object

class Cart(models.Model):

    cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)

    company = models.ForeignKey('core.Company', 
        null=True, blank=True, on_delete=models.CASCADE, verbose_name=_("Company")
    )

    user = models.ForeignKey(User, 
        null=True, blank=True, on_delete=models.CASCADE
    ) #Uno a mucho
    
    products = models.ManyToManyField(Product, through='CartProducts') #Muchos a Muchos
    
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)

    #Comision del total
    #IVA = 16% = 0.16
    IVA = 0.16

    def __str__(self):
        return self.cart_id

    #Para actualizar los subtotales y totales

    def update_totals(self): #Callback entero
        self.update_subtotal()
        self.update_total()
        
        if self.order:
            self.order.update_total()


    def update_subtotal(self):
        self.subtotal = sum([
        product.quantity * product.product.price for product in self.products_related()
            ]
        )
        self.save()

    def update_total(self): #Accion para totales
        self.total = self.subtotal + (self.subtotal * decimal.Decimal(Cart.IVA))
        self.save()
    
    #Para solucionar el problema n+1 query
    def products_related(self):
        return self.cartproducts_set.select_related('product')

    def has_products(self):
        return self.products.exists()

    @property 
    def order(self):
        return self.order_set.filter(status='inprogress').first()
 
class CartProducts(models.Model):
        cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        quantity = models.IntegerField(default=1)
        created_at = models.DateTimeField(auto_now_add=True)

        objects = CartProductsManager()

        def update_quantity(self, quantity=1):
            self.quantity = quantity
            self.save()

#Callbacks functions
def set_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())

def totals(sender, instance, action, *args, **kwargs):
    if action in ['post_add',  'post_remove',  'post_clear']:
        instance.update_totals()

def post_save_update_totals(sender, instance, *args, **kwargs):
    instance.cart.update_totals()

#Callbacks caller
pre_save.connect(set_cart_id, sender=Cart)
post_save.connect(post_save_update_totals, sender=CartProducts)
m2m_changed.connect(totals, sender=Cart.products.through)