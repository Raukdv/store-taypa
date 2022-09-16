from re import template
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from core.views import CompanyRequiredMixin
from ..forms.user import UserCreateForm, UserPasswordForm, UserUpdateForm

UserModel = get_user_model()

class UserCreateView(CompanyRequiredMixin, CreateView):
    form_class = UserCreateForm
    model = UserModel
    template_name = 'panel/user/form.html'

    def form_valid(self, form):
        self.object = form.save()
        self.object.collaborator_set.create(company=self.company)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('panel:user_list', args=[self.company.slug])

class UserDeleteView(CompanyRequiredMixin, DeleteView):
    model = UserModel
    template_name = 'panel/user/confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        collaborator = self.company.collaborator_set.get(user=self.object)
        collaborator.delete()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def get_queryset(self):
        queryset = self.company.users.all()
        queryset = queryset.exclude(pk=self.company.user.pk)
        queryset = queryset.exclude(is_staff=True)
        queryset = queryset.exclude(is_superuser=True)
        return queryset

    def get_success_url(self):
        return reverse_lazy('panel:user_list', args=[self.company.slug])

class UserListView(CompanyRequiredMixin, ListView):
    model = UserModel
    paginate_by = 30
    template_name = 'panel/user/list.html'

    def get_queryset(self):
        queryset = self.company.users.all()
        queryset = queryset.exclude(is_staff=True)
        queryset = queryset.exclude(is_superuser=True)
        return queryset

class UserPasswordView(CompanyRequiredMixin, UpdateView):
    form_class = UserPasswordForm
    model = UserModel
    template_name = 'panel/user/form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance')
        kwargs['user'] = self.get_object()
        return kwargs

    def get_queryset(self):
        queryset = self.company.users.all()
        queryset = queryset.exclude(is_staff=True)
        queryset = queryset.exclude(is_superuser=True)
        return queryset

    def get_success_url(self):
        return reverse_lazy('panel:user_list', args=[self.company.slug])

class UserUpdateView(CompanyRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    model = UserModel
    template_name = 'panel/user/form.html'

    def get_queryset(self):
        queryset = self.company.users.all()
        queryset = queryset.exclude(is_staff=True)
        queryset = queryset.exclude(is_superuser=True)
        return queryset

    def get_success_url(self):
        return reverse_lazy('panel:user_list', args=[self.company.slug])