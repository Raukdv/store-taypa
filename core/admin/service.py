from django.contrib import admin

from core.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'is_active'
    )
    search_fields = (
        'name',
    )
