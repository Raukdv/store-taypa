from django.contrib import admin
# Register your models here.
from core.models import BillingProfile

@admin.register(BillingProfile)
class BillingProfileAdmin(admin.ModelAdmin):
	list_display = ('type_payment', 'brand', 'created_at',)