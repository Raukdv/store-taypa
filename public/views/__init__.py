from .base import IndexView, SignUpAsMerchant, SignUpAsCustomer
from .company import CompanyDetailView, CompanyLinkView, CompanyMerchantDetailView
from .message import MessageRedirectView, MessageSMSView
from .cart import CompanyMerchantCartView, add, remove

from .order import (
    CompanyOrderView, 
    CompanyAddressOrderView, 
    CompanySelectAddressOrderView, 
    CompanyCheckAddressOrderView,
    CompanyConfirmOrderView,
    CompanyCancelOrderView,
    CompanyCompleteOrderView,
    CompanyOrderListView,
    CompanyPaymentOrderView
    )

from .shipping_addresses import (
    CompanyShippingAddressListView, 
    CompanyShippingAddressCreateView, 
    CompanyShippingAddressUpdateView,
    CompanyShippingAddressDeleteView
    )

from .product import CompanyProductDetailView
from .category import CompanyCategoryDetailView
from .promocodes import validate

__all__ = [
    'IndexView',
    'CompanyDetailView',
    'CompanyLinkView',
    'CompanyMerchantDetailView',
    'MessageRedirectView',
    'MessageSMSView',
    'CompanyMerchantCartView',
    'add',
    'SignUpAsMerchant',
    'SignUpAsCustomer',
    'remove',
    'CompanyOrderView',
    'CompanyShippingAddressListView',
    'CompanyShippingAddressCreateView',
    'CompanyShippingAddressUpdateView',
    'CompanyShippingAddressDeleteView',
    'CompanyProductDetailView',
    'CompanyAddressOrderView',
    'CompanySelectAddressOrderView',
    'CompanyCheckAddressOrderView',
    'CompanyConfirmOrderView',
    'CompanyCancelOrderView',
    'CompanyCompleteOrderView',
    'CompanyOrderListView',
    'validate',
    'CompanyPaymentOrderView'
    'CompanyCategoryDetailView'
]
