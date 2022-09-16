from django.urls import include, path

from . import views


app_name = 'billingprofile'

urlpatterns = [
    path(
        'profile/',
        include([
            path(
                '',
                views.BillingProfileListView.as_view(),
                name='billing_profile_list'
            ),
            path(
                'create',
                views.BillingProfileCreateView.as_view(),
                name='billing_profile_create'
            ),
        ])
    ),
]