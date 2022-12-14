from django.urls import include, path

from panel.forms.user import UserAddressForm, UserCreateForm
from . import views

app_name = 'public'

urlpatterns = [
    path(
        '',
        views.IndexView.as_view(),
        name='index'
    ),
    path(
        'merchant_signup/',
        views.SignUpAsMerchant.as_view(),
        name='merchant_signup'
    ),
    path(
        'customer_signup/',
        views.SignUpAsCustomer.as_view(),
        name='customer_signup'
    ),
    path(
        'rest/<slug>/',
        include([
            path(
                '',
                views.CompanyMerchantDetailView.as_view(),
                name='merchant_detail'
            ),
            path(
                'carrito/',
                views.CompanyMerchantCartView.as_view(),
                name='merchant_cart'
            ),
            path(
                'carrito/agregar/',
                views.add,
                name='cart_add'
            ),
            path(
                'carrito/eliminar/',
                views.remove,
                name='cart_remove'
            ),
            path(
                'orden/',
                views.CompanyOrderView.as_view(),
                name='order_view'
            ),
            path(
                'confirmar-orden/',
                views.CompanyConfirmOrderView.as_view(),
                name='order_confirm'
            ),
            path(
                'cancelar-orden/',
                views.CompanyCancelOrderView.as_view(),
                name='order_cancel'
            ),
            path(
                'completar-orden/',
                views.CompanyCompleteOrderView.as_view(),
                name='order_complete'
            ),
            path(
                'pago-orden/',
                views.CompanyPaymentOrderView.as_view(),
                name='order_payment'
            ),

            path(
                'mis-ordenes/',
                views.CompanyOrderListView.as_view(),
                name='orders_list'
            ),
            path(
                'direccion-de-envio/',
                views.CompanyShippingAddressListView.as_view(),
                name='shippingaddress_view'
            ),
            path(
                'direccion-de-envio/agregar/',
                views.CompanyShippingAddressCreateView.as_view(),
                name='shippingaddress_add'
            ),
            path(
                'direccion-de-orden/',
                views.CompanyAddressOrderView.as_view(),
                name='orderaddress_view'
            ),
            path(
                'seleccionar/direccion',
                views.CompanySelectAddressOrderView.as_view(),
                name='select_address'
            ),
            path(
                'promo/validar',
                views.validate,
                name='promocode_validate'
            ),
            path(
                '<int:pk>/',
                include([
                    path(
                        'direccion-de-envio/actualizar/',
                        views.CompanyShippingAddressUpdateView.as_view(),
                        name='shippingaddress_update'
                    ),
                    path(
                        'establecer-direccion/',
                        views.CompanyCheckAddressOrderView.as_view(),
                        name='selected_address'
                    ),
                    path(
                        'direccion-de-envio/eliminar/',
                        views.CompanyShippingAddressDeleteView.as_view(),
                        name='shippingaddress_delete'
                    ),
                    path(
                        'direccion-de-envio/predeterminada/',
                        views.CompanyShippingAddressListView.default,
                        name='shippingaddress_default'
                    ),
                ])
            ),
            path('producto/<product_slug>/',
            include([
                    path(
                    '',
                    views.CompanyProductDetailView.as_view(),
                    name='merchant_product_detail'
                ),
            ]),
            ),
            path('categoria/<category_slug>/',
            include([
                    path(
                    '',
                    views.CompanyCategoryDetailView.as_view(),
                    name='merchant_category_detail'
                ),
            ]),
            ),
        ])
    ),
    path(
        'o/<uidb64>/',
        views.MessageRedirectView.as_view(),
        name='message_redirect'
    ),
    path(
        'messages/',
        include([
            path(
                'sms/',
                views.MessageSMSView.as_view(),
                name='message_sms'
            )
        ])
    ),
    path(
        '<slug>/',
        include([
            path(
                '',
                views.CompanyDetailView.as_view(),
                name='company_detail'
            ),
            path(
                'review/<service>/',
                views.CompanyLinkView.as_view(),
                name='company_link'
            )
        ])
    )
]

#
