from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class Service(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name=_("Name")
    )
    slug = models.SlugField(
        editable=False, unique=True, verbose_name=_("Slug")
    )
    icon = models.ImageField(
        blank=True, null=True, upload_to='services/',
        verbose_name=_("Icon")
    )
    is_active = models.BooleanField(
        default=True, verbose_name=_("Active")
    )

    class Meta:
        ordering = ['name']
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self):
        return str(self.name)

    def clean(self):
        super().clean()
        self.slug = slugify(self.name)
