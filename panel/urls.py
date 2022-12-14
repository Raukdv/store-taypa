from panel.views.phone import PhoneConnectView
from django.urls import include, path

from . import views


app_name = 'panel'

urlpatterns = [
    path(
        '',
        views.IndexView.as_view(),
        name='index'
    ),
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
    path(
        'company/',
        views.CompanyCreateView.as_view(),
        name='company_add'
    ),
    path(
        'phones/',
        include([
            path(
                '',
                views.PhoneListView.as_view(),
                name='phone_list'
            ),
            path(
                '<int:pk>/',
                include([
                    path(
                        'change/',
                        views.PhoneChangeView.as_view(),
                        name='phone_change'
                    ),
                    path(
                        'connect/',
                        views.PhoneConnectView.as_view(),
                        name='phone_connect'
                    ),
                    path(
                        'delete/',
                        views.PhoneDeleteView.as_view(),
                        name='phone_delete'
                    )
                ])
            ),
            path(
                'purchase/',
                views.PhonePurchaseView.as_view(),
                name='phone_purchase'
            ),
            path(
                'search/',
                views.PhoneSearchView.as_view(),
                name='phone_search'
            ),
            path(
                'sync/',
                views.PhoneSyncView.as_view(),
                name='phone_sync'
            )
        ])
    ),
    path(
        'services/',
        include([
            path(
                '',
                views.ServiceListView.as_view(),
                name='service_list'
            ),
            path(
                'add/',
                views.ServiceCreateView.as_view(),
                name='service_add'
            ),
            path(
                '<int:pk>/',
                include([
                    path(
                        'change/',
                        views.ServiceUpdateView.as_view(),
                        name='service_change'
                    ),
                    path(
                        'delete/',
                        views.ServiceDeleteView.as_view(),
                        name='service_delete'
                    )
                ])
            )
        ])
    ),
    path(
        '<company>/',
        include([
            path(
                '',
                views.IndexView.as_view(),
                name='index'
            ),
            path(
                'add/',
                views.CompanyChildCreateView.as_view(),
                name='company_add'
            ),
            path(
                'change/',
                include([
                    path(
                        '',
                        views.CompanyUpdateView.as_view(),
                        name='company_change'
                    ),
                    path(
                        'messages/',
                        views.CompanyUpdateMessagesView.as_view(),
                        name='company_change_messages'
                    ),
                    path(
                        'links/',
                        views.CompanyUpdateLinksView.as_view(),
                        name='company_change_links'
                    )
                ])
            ),
            path(
                'customers/',
                include([
                    path(
                        '',
                        views.CustomerListView.as_view(),
                        name='customer_list'
                    ),
                    path(
                        'add/',
                        views.CustomerCreateView.as_view(),
                        name='customer_add'
                    ),
                    path(
                        '<int:pk>/',
                        include([
                            path(
                                '',
                                views.CustomerDetailView.as_view(),
                                name='customer_detail'
                            ),
                            path(
                                'change/',
                                views.CustomerUpdateView.as_view(),
                                name='customer_change'
                            ),
                            path(
                                'delete/',
                                views.CustomerDeleteView.as_view(),
                                name='customer_delete'
                            ),
                            path(
                                'send-sms/',
                                views.CustomerSendSMSView.as_view(),
                                name='customer_send_sms'
                            )
                        ])
                    ),

                ])
            ),
            path(
                'products/',
                include([
                    path(
                        '',
                        views.ProductListView.as_view(),
                        name='product_list'
                    ),
                    path(
                        'add/',
                        views.ProductCreateView.as_view(),
                        name='product_add'
                    ),
                    path(
                        '<int:pk>/',
                        include([
                            path(
                                '',
                                views.ProductDetailView.as_view(),
                                name='product_detail'
                            ),
                            path(
                                'change/',
                                views.ProductUpdateView.as_view(),
                                name='product_change'
                            ),
                            path(
                                'delete/',
                                views.ProductDeleteView.as_view(),
                                name='product_delete'
                            ),
                        ])
                    ),
                ])
            ),
            path(
                'category/',
                include([
                    path(
                        '',
                        views.CategoryListView.as_view(),
                        name='category_list'
                    ),
                    path(
                        'add/',
                        views.CategoryCreateView.as_view(),
                        name='category_add'
                    ),
                    path(
                        '<int:pk>/',
                        include([
                            path(
                                '',
                                views.CategoryDetailView.as_view(),
                                name='category_detail'
                            ),
                            path(
                                'change/',
                                views.CategoryUpdateView.as_view(),
                                name='category_change'
                            ),
                            path(
                                'delete/',
                                views.CategoryDeleteView.as_view(),
                                name='category_delete'
                            ),
                        ])
                    ),
                ])
            ),
            path(
                'ordenes/',
                include([
                    path(
                        '',
                        views.OrderListView.as_view(),
                        name='order_list'
                    ),
                        ])
            ),
            path(
                'feedbacks/',
                include([
                    path(
                        '',
                        views.FeedbackListView.as_view(),
                        name='feedback_list'
                    ),
                    path(
                        '<int:pk>/',
                        views.FeedbackDetailView.as_view(),
                        name='feedback_detail'
                    )
                ])
            ),
            path(
                'messages/',
                include([
                    path(
                        '',
                        views.MessageListView.as_view(),
                        name='message_list'
                    ),
                    path(
                        '<int:pk>/',
                        views.MessageDetailView.as_view(),
                        name='message_detail'
                    )
                ])
            ),
            path(
                'users/',
                include([
                    path(
                        '',
                        views.UserListView.as_view(),
                        name='user_list'
                    ),
                    path(
                        'add/',
                        views.UserCreateView.as_view(),
                        name='user_add'
                    ),
                    path(
                        '<int:pk>/',
                        include([
                            path(
                                'change/',
                                views.UserUpdateView.as_view(),
                                name='user_change'
                            ),
                            path(
                                'delete/',
                                views.UserDeleteView.as_view(),
                                name='user_delete'
                            ),
                            path(
                                'password/',
                                views.UserPasswordView.as_view(),
                                name='user_password'
                            )
                        ])
                    )
                ])
            ),
        ])
    )
]
