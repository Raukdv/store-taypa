from panel.forms.user import UserUpdateForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView


UserModel = get_user_model()

class AccountChangeView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    model = UserModel
    template_name = 'panel/account/form.html'
    success_url = reverse_lazy('panel:account_detail')

    def get_object(self):
        return self.request.user

class AccountDetailView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'panel/account/detail.html'

    def get_object(self):
        return self.request.user

class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'panel/account/password_change.html'
    success_url = reverse_lazy('panel:account_detail')
