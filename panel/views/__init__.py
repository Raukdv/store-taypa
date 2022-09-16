from .account import (
    AccountChangeView,
    AccountDetailView,
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from .base import IndexView

from .company import (
    CompanyChildCreateView,
    CompanyCreateView,
    CompanyUpdateView,
    CompanyUpdateLinksView,
    CompanyUpdateMessagesView
)
from .customer import (
    CustomerCreateView,
    CustomerDeleteView,
    CustomerDetailView,
    CustomerListView,
    CustomerUpdateView,
    CustomerSendSMSView
)
from .feedback import (
    FeedbackDetailView,
    FeedbackListView
)
from .message import (
    MessageDetailView,
    MessageListView
)
from .phone import (
    PhoneChangeView,
    PhoneConnectView,
    PhoneDeleteView,
    PhoneListView,
    PhonePurchaseView,
    PhoneSearchView,
    PhoneSyncView
)
from .service import (
    ServiceCreateView,
    ServiceDeleteView,
    ServiceListView,
    ServiceUpdateView
)
from .user import (
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserPasswordView,
    UserUpdateView,
)

from .product import (
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,

)

from .category import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryDetailView,
    CategoryListView,
    CategoryUpdateView,
)

from .order import (
    OrderListView
)

from .error import (
    pag_400_bad_request,
    pag_403_forbidden,
    pag_404_not_found,
    pag_500_error_server
)

__all__ = [
    'AccountChangeView',
    'AccountDetailView',
    'CompanyChildCreateView',
    'CompanyCreateView',
    'CompanyUpdateView',
    'CustomerCreateView',
    'CustomerDeleteView',
    'CustomerDetailView',
    'CustomerListView',
    'CustomerUpdateView',
    'CompanyUpdateLinksView',
    'CompanyUpdateMessagesView',
    'CustomerSendSMSView',
    'FeedbackDetailView',
    'FeedbackListView',
    'IndexView',
    'LoginView',
    'LogoutView',
    'MessageDetailView',
    'MessageListView',
    'PasswordChangeView',
    'PasswordResetView',
    'PasswordResetDoneView',
    'PasswordResetConfirmView',
    'PasswordResetCompleteView',
    'PhoneChangeView',
    'PhoneConnectView',
    'PhoneDeleteView',
    'PhoneListView',
    'PhonePurchaseView',
    'PhoneSearchView',
    'PhoneSyncView',
    'ServiceCreateView',
    'ServiceDeleteView',
    'ServiceListView',
    'ServiceUpdateView',
    'UserCreateView',
    'UserDeleteView',
    'UserListView',
    'UserPasswordView',
    'UserUpdateView',
    'ProductCreateView',
    'ProductDeleteView',
    'ProductDetailView',
    'ProductListView',
    'ProductUpdateView',
    'CategoryCreateView',
    'CategoryDeleteView',
    'CategoryDetailView',
    'CategoryListView',
    'CategoryUpdateView',
    'pag_400_bad_request',
    'pag_403_forbidden',
    'pag_404_not_found',
    'pag_500_error_server',
    'OrderListView'
]
