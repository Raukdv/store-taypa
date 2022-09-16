from django.db import models
from django.utils.translation import ugettext_lazy as _

from .mixins import AuditableMixin


class Feedback(AuditableMixin):
    company = models.ForeignKey(
        'core.Company', on_delete=models.CASCADE, verbose_name=_("Company")
    )
    customer = models.ForeignKey(
        'core.Customer', blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name=_("Customer")
    )
    service = models.ForeignKey(
        'core.Service', blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name=_("Service")
    )
    detail = models.TextField(
        blank=True, null=True, verbose_name=_("Detail")
    )

    class Meta:
        ordering = ['-date_creation']
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")

    def __str__(self):
        return str(self.service)

    def is_positive(self):
        return False if self.detail else True
    is_positive.boolean = True
