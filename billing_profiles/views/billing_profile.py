
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.views.generic import (
    TemplateView, ListView, CreateView, DeleteView, UpdateView, DetailView
)

from core.models.billing_profiles import BillingProfile
from billing_profiles.forms.billing_profile import BillingProfileForm

from public.tools.order import get_or_create_order, breadcrumb
from public.tools.cart import get_or_create_cart

from django.conf import settings

class BillingProfileListView(LoginRequiredMixin, ListView):
    model = BillingProfile
    paginate_by = 30
    ordering = ['-default']
    template_name = 'panel/billing_profile/list.html'

    def get_queryset(self):
        return self.request.user.billing_profiles

class BillingProfileCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'panel/billing_profile/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        return context

    def post(self, request):

        if request.method == 'POST':

            if request.POST.get('stripeToken'):

                if not request.user.has_customer():
                    request.user.create_customer_id()

            stripe_token = request.POST['stripeToken']
            billing_profile = BillingProfile.objects.create_by_stripe_token(request.user, stripe_token)

            if billing_profile:
                messages.success(request, 'Tarjeta creada exitosamente')
    
            return HttpResponseRedirect(reverse_lazy('billingprofile:billing_profile_list'))

def create_billing_profile(request):
    if request.method == 'POST':
        print("hola desde la vista create")

    return HttpResponseRedirect(reverse_lazy('billingprofile:billing_profile_list'))