from django.contrib import admin
# Register your models here.
from core.models import ShippingAddress

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
	list_display = ('__str__',)