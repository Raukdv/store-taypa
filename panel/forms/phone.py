from django import forms
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from core.models import Phone


class PhoneForm(forms.ModelForm):
    class Meta:
        fields = ('company',)
        model = Phone


class PhoneSearchForm(forms.Form):
    TYPE_CHOICES = (
        ('local', _('Local')),
        ('toll_free', _('Toll free')),
        ('mobile', _('Mobile')),
    )
    contains = forms.CharField(
        label=_('Contains'), required=False
    )
    type = forms.ChoiceField(
        label=_('Type'), choices=TYPE_CHOICES, required=False
    )
    country = CountryField().formfield(
        label=_('Country'), initial='US'
    )

    def save(self):
        return Phone.objects.search(**self.cleaned_data)
