from django.contrib import admin
# Register your models here.
from core.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

	fields = ('title', 'description', 'price', 'image', 'available', 'stock')

	list_display = ('__str__', 'slug', 'created_at', 'last_updated')
