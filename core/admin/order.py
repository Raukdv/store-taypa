from django.contrib import admin
# Register your models here.
from core.models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('__str__',)