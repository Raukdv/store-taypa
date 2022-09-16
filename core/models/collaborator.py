from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _


class CollaboratorManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(is_active=True)

    def parent(self):
        return self.get_queryset().filter(
            is_active=True,
            company__parent_company__isnull=True
        )


class Collaborator(models.Model):
    COMPANY_FIELD = 'company'

    user = models.ForeignKey(
        'core.User', on_delete=models.CASCADE,
        verbose_name=_("user")
    )
    company = models.ForeignKey(
        'core.Company', on_delete=models.CASCADE,
        verbose_name=_("company")
    )
    is_active = models.BooleanField(
        default=True, verbose_name=_("active")
    )
    date_joined = models.DateTimeField(
        auto_now=True, verbose_name=_("date join")
    )

    objects = CollaboratorManager()

    class Meta:
        ordering = ['user', ]
        unique_together = ('user', 'company')
        verbose_name = _("collaborator")
        verbose_name_plural = _("collaborators")

    def __str__(self):
        return str(self.user)

    @property
    def parent(self):
        return self.user


def pre_delete(sender, instance, **kwargs):
    if instance.user == instance.company.user:
        raise PermissionDenied("Cannot remove a user from it's own company.")


signals.pre_delete.connect(pre_delete, sender=Collaborator)
