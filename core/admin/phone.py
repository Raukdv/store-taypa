from django.contrib import admin

from core.models import Phone


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    fields = (
        'phone', 'api_id'
    )
    readonly_fields = (
        'api_id',
    )
    search_fields = (
        'phone', 'api_id'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
