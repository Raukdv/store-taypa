from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from core.models import Collaborator, User


class CollaboratorInline(admin.TabularInline):
    autocomplete_fields = ('company',)
    extra = 0
    model = Collaborator


@admin.register(User)
class UserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_customer', 'is_merchant', 'is_staff', 'is_superuser', 'groups',
                'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Payment Info'), {'fields': ('customer_id',)}),
    )
    inlines = (
        CollaboratorInline,
    )
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    readonly_fields = ('last_login', 'date_joined')
    search_fields = ('first_name', 'last_name', 'email')
