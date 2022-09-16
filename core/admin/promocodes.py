from django.contrib import admin
# Register your models here.
from core.models import PromoCode

@admin.register(PromoCode)
class PromoCodesAdmin(admin.ModelAdmin):
    fields = (
        'company', 'code', 'valid_from', 'valid_to', 'discount',
    )

    list_display = (
        '__str__', 'valid_from', 'valid_to', 'discount', 'used'
    )
    list_filter = (
        'company',
    )
    readonly_fields = (
        'company',
    )
    search_fields = (
        'company', '__str__', 'discount', 'used'
    )
