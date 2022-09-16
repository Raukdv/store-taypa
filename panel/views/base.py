from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView

from core.models import Company
from core.views import CompanyMixin

class IndexView(CompanyMixin, LoginRequiredMixin, ListView):
    model = Company
    template_name = 'panel/index.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            parent_company__isnull=True
        )

        if not self.request.user.is_staff:
            queryset = queryset.none()
        
        return queryset

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff and not self.company:
            queryset = request.user.collaborator_set.filter(
                company__parent_company__isnull=True
            )

            if queryset.count() == 1:
                collaborator = queryset.get()
                company = collaborator.company
                return HttpResponseRedirect(company.get_absolute_url())
                   
        return super().get(request, *args, **kwargs)
