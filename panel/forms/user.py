from pyexpat import model
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    SetPasswordForm,
    UserCreationForm,
    UserChangeForm
)
from django.utils.translation import gettext_lazy as _

from core.models.shipping_addresses import ShippingAddress


UserModel = get_user_model()


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(
        label=_("First name")
    )
    last_name = forms.CharField(
        label=_("Last name")
    )

    class Meta:
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')
        model = UserModel

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        exclude = ('user', 'created_at')

class UserPasswordForm(SetPasswordForm):
    pass


class UserUpdateForm(UserChangeForm):
    class Meta:
        fields = (
            'password', 'email', 'first_name', 'last_name'
        )
        model = UserModel
