from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy


class PasswordResetView(PasswordResetView):
    email_template_name = 'panel/account/password_reset_email.html'
    subject_template_name = 'panel/account/password_reset_subject.txt'
    success_url = reverse_lazy('panel:account_password_reset_done')
    template_name = 'panel/account/password_reset_form.html'


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'panel/account/password_reset_done.html'


class PasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('panel:account_password_reset_complete')
    template_name = 'panel/account/password_reset_confirm.html'


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'panel/account/password_reset_complete.html'
