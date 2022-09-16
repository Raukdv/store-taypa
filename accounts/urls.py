from django.urls import include, path

from . import views

app_name = 'accounts'

urlpatterns = [
    path(
        'account/',
        include([
            path(
                '',
                views.AccountDetailView.as_view(),
                name='account_detail'
            ),
            path(
                'change/',
                views.AccountChangeView.as_view(),
                name='account_change'
            ),
            path(
                'login/',
                views.LoginView.as_view(),
                name='account_login'
            ),
            path(
                'logout/',
                views.LogoutView.as_view(),
                name='account_logout'
            ),
            path(
                'password/',
                views.PasswordChangeView.as_view(),
                name='account_password_change'
            ),
            path(
                'password-reset/',
                views.PasswordResetView.as_view(),
                name='account_password_reset'
            ),
            path(
                'password-reset/done/',
                views.PasswordResetDoneView.as_view(),
                name='account_password_reset_done'
            ),
            path(
                'password-reset/<uidb64>/<token>/',
                views.PasswordResetConfirmView.as_view(),
                name='account_password_reset_confirm'
            ),
            path(
                'password-reset/complete/',
                views.PasswordResetCompleteView.as_view(),
                name='account_password_reset_complete'
            ),
        ])
    ),
]