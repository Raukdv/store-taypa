from django.db import models
from django.utils.translation import ugettext_lazy as _


class Link(models.Model):
    company = models.ForeignKey(
        'core.Company', on_delete=models.CASCADE, verbose_name=_("Company")
    )
    service = models.ForeignKey(
        'core.Service', on_delete=models.PROTECT, verbose_name=_("Service")
    )
    icon = models.ImageField(
        blank=True, null=True, upload_to='icon/', verbose_name=_("Icon")
    )
    name = models.CharField(
        blank=True, max_length=100, null=True, verbose_name=_("Name")
    )
    url = models.URLField(
        verbose_name=_("URL")
    )
    order = models.PositiveIntegerField(
        default=0, verbose_name=_("Order")
    )

    class Meta:
        ordering = ['order', 'service']
        unique_together = ('company', 'service')
        verbose_name = _("Link")
        verbose_name_plural = _("Links")

    def __str__(self):
        return str(self.name) if self.name else str(self.service)
