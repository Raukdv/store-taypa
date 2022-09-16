from django import forms

from core.models import Service


class ServiceForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Service
