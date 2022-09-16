from django.contrib import admin
from django.contrib.auth.models import Group

from .company import CompanyAdmin
from .customer import CustomerAdmin
from .feedback import FeedbackAdmin
from .message import MessageAdmin
from .phone import PhoneAdmin
from .service import ServiceAdmin
from .user import UserAdmin
from .logs import LogEntryMonitor
from .product import ProductAdmin
from .cart import CartAdmin
from .order import OrderAdmin
from .shipping_addresses import ShippingAddress
from .promocodes import PromoCodesAdmin
from .billing_profiles import BillingProfileAdmin
from .charges import Charge

admin.site.unregister(Group)

__all__ = [
    'CompanyAdmin',
    'CustomerAdmin',
    'FeedbackAdmin',
    'MessageAdmin',
    'PhoneAdmin',
    'ServiceAdmin',
    'UserAdmin',
    'LogEntryMonitor',
    'ProductAdmin',
    'CartAdmin',
    'OrderAdmin',
    'ShippingAddress',
    'PromoCodesAdmin'
    'PromoCodesAdmin',
    'BillingProfileAdmin',
    'Charge'
]

