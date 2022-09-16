from django.core.exceptions import PermissionDenied
from ..models import Company


class CompanyMixin:
    company_field = 'company'

    def dispatch(self, request, *args, **kwargs):
        self.company = self.get_company()
        return super().dispatch(request, *args, **kwargs)

    def get_company(self):
        if hasattr(self, 'company') and self.company:
            return self.company

        #company_slug = self.kwargs.get('company')
        #dinamic comparator.
        #company_slug = ''
        company_slug = self.kwargs.get('company') if 'company' in self.kwargs else self.kwargs.get('slug')

        try:
            return Company.objects.get(slug=company_slug)
        except Company.DoesNotExist:
            return

    def get_company_field(self):
        return self.company_field

    def get_context_data(self, **kwargs):
        kwargs['company'] = self.get_company()
        return super().get_context_data(**kwargs)


class CompanyRequiredMixin(CompanyMixin):
    def dispatch(self, request, *args, **kwargs):
        self.company = self.get_company()

        if not self.company:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class CollaboratorRequiredMixin(CompanyMixin):
    def dispatch(self, request, *args, **kwargs):
        self.company = self.get_company()

        if not self.company:
            raise PermissionDenied

        collaborator = self.get_collaborator()
        if not collaborator:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_collaborator(self):
        if hasattr(self, 'collaborator') and self.collaborator:
            return self.collaborator
        return self.request.user.as_collaborator(self.company)

    def get_context_data(self, **kwargs):
        kwargs['collaborator'] = self.get_collaborator()
        return super().get_context_data(**kwargs)

#Public mixin
class CompanyQuerySetPublicMixin(CompanyMixin):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            **{self.get_company_field(): self.get_company()}
        )
        return queryset

class CompanyQuerySetMixin(CollaboratorRequiredMixin):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            **{self.get_company_field(): self.get_company()}
        )
        return queryset


class CompanyCreateMixin(CollaboratorRequiredMixin):
    def form_valid(self, form):
        setattr(form.instance, self.get_company_field(), self.get_company())
        return super().form_valid(form)


class UserCreateMixin:
    def form_valid(self, form):
        setattr(form.instance, 'user', self.request.user)
        return super().form_valid(form)
