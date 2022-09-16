from django.contrib import admin

from core.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'date_creation', 'from_', 'to', 'company', 'type', 'direction'
    )
    list_filter = (
        'company',
    )
    readonly_fields = (
        'api_id', 'type', 'direction'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
