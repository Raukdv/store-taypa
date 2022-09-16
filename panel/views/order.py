from django.views.generic import (ListView, DetailView, CreateView
)

from django.contrib.auth.mixins import LoginRequiredMixin

from core.views import (
    CompanyMixin, CompanyCreateMixin
)

from core.models import Company, ShippingAddress, Charge, User, Order

from ..filters.order import OrderFilterSet
from ..forms.order import OrderForm

class OrderListView(CompanyMixin, LoginRequiredMixin, ListView):
    filterset_class = OrderFilterSet
    model = Order
    paginate_by = 30
    ordering = ['-create_at']
    template_name = 'panel/order/list.html'

    def get_queryset(self):
        qs = Order.objects.filter(company=self.company)
        return qs






