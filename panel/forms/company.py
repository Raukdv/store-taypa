from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from core.models import Company, Link


class LinkForm(forms.ModelForm):
    class Meta:
        exclude = ('company',)


class CompanyForm(forms.ModelForm):
    field_order = [
        'user', 'name', 'email', 'phone'
    ]

    class Meta:
        exclude = (
            'parent_company', 'sender', 'users', 'sms_template',
            'widget_welcome_text', 'widget_positive_text',
            'widget_negative_text', 'widget_submitted_title',
            'widget_submitted_text',
        )
        model = Company
        widgets = {
            'address': forms.TextInput,
            'address_2': forms.TextInput,
        }


class CompanyChildForm(forms.ModelForm):
    field_order = [
        'name', 'email', 'phone'
    ]

    class Meta:
        exclude = (
            'parent_company', 'user', 'sender', 'users', 'sms_template',
            'widget_welcome_text', 'widget_positive_text',
            'widget_negative_text', 'widget_submitted_title',
            'widget_submitted_text'
        )
        model = Company
        widgets = {
            'address': forms.TextInput,
            'address_2': forms.TextInput,
        }


class CompanyEmptyForm(forms.ModelForm):
    name = forms.CharField(disabled=True, label=_("Company"))

    class Meta:
        fields = ('name',)
        model = Company


class CompanyMessagesForm(forms.ModelForm):
    class Meta:
        fields = (
            'sms_template', 'widget_welcome_text', 'widget_positive_text',
            'widget_negative_text', 'widget_submitted_title',
            'widget_submitted_text',
        )
        model = Company


CompanyLinkFormSet = inlineformset_factory(
    Company,
    Link,
    can_delete=True,
    extra=1,
    form=LinkForm
)
