from django.contrib import admin

from core.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = (
        'company', 'first_name', 'last_name', 'email', 'phone'
    )
    list_display = (
        '__str__', 'company', 'email', 'phone'
    )
    list_filter = (
        'company',
    )
    readonly_fields = (
        'company',
    )
    search_fields = (
        'first_name', 'last_name', 'email', 'phone'
    )

    def has_add_permission(self, request):
        return False
