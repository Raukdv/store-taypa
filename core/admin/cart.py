from django.contrib import admin
# Register your models here.
from core.models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'created_at',)