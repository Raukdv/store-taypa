from django.db.utils import ProgrammingError
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from core.models import Company, Collaborator, Link, Service


class CollaboratorInline(admin.TabularInline):
    autocomplete_fields = ('user',)
    extra = 0
    model = Collaborator

    def has_delete_permission(self, request, obj=None):
        if not obj:
            return True
        return obj.user != request.user


class LinkInline(admin.TabularInline):
    autocomplete_fields = ('service',)
    extra = 0
    model = Link

    def get_max_num(self, request, obj=None, **kwargs):
        try:
            return Service.objects.count()
        except ProgrammingError:
            return 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    autocomplete_fields = ('parent_company', 'user')
    fieldsets = (
        (None, {'fields': (
            'user', 'parent_company', 'name', 'slug', 'email', 'phone'
        )}),
        (_('Address'), {
            'fields': (
                'address', 'address_2', 'city', 'state', 'country'
            ),
        }),
    )
    inlines = (
        LinkInline, CollaboratorInline
    )
    readonly_fields = ('slug',)
    search_fields = ('name', 'email')
