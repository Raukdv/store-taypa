from django import forms

from core.models import BillingProfile

class BillingProfileForm(forms.ModelForm):
    
    class Meta:

        model = BillingProfile

        fields = '__all__'

        exclude = (
            'user', 'created_at', 'default'
        )

        