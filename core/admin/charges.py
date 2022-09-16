from django.contrib import admin
# Register your models here.
from core.models import Charge

@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
	list_display = ('__str__',)