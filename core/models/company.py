from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import signals
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from .mixins import get_address_mixin
from ..fields import PhoneField
from .. import constants


class Company(get_address_mixin(required=True, default_country='US')):
    parent_company = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.CASCADE,
        verbose_name=_("Parent company")
    )
    name = models.CharField(
        max_length=150, unique=True, verbose_name=_("Name")
    )
    logo = models.ImageField(
        blank=True, null=True, upload_to='companies/',
        verbose_name=_("Logo")
    )
    slug = models.SlugField(
        editable=False, verbose_name=_("Slug")
    )
    user = models.ForeignKey(
        'core.User', on_delete=models.PROTECT, verbose_name=_("User")
    )
    email = models.EmailField(
        verbose_name=_("Email")
    )
    phone = PhoneField(
        verbose_name=_("Phone")
    )
    users = models.ManyToManyField(
        'core.User', blank=True,
        through='Collaborator', related_name='+',
        verbose_name=_("users")
    )
    sms_template = models.TextField(
        default=constants.REVIEW_SMS,
        help_text=_(
            "Available variables: {{ customer }}, {{ company }}, {{ url }}."
        ),
        verbose_name=_("SMS template")
    )
    # Widget copy
    widget_welcome_text = models.TextField(
        default=constants.DEFAULT_WIDGET_WELCOME_TEXT,
        verbose_name=_("Widget welcome text")
    )
    widget_positive_text = models.TextField(
        default=constants.DEFAULT_WIDGET_POSITIVE_TEXT,
        verbose_name=_("Widget positive text")
    )
    widget_negative_text = models.TextField(
        default=constants.DEFAULT_WIDGET_NEGATIVE_TEXT,
        verbose_name=_("Widget negative text")
    )
    widget_submitted_title = models.TextField(
        default=constants.DEFAULT_WIDGET_SUBMITTED_TITLE,
        verbose_name=_("Widget submitted title")
    )
    widget_submitted_text = models.TextField(
        default=constants.DEFAULT_WIDGET_SUBMITTED_TEXT,
        verbose_name=_("Widget submitted text")
    )

    class Meta:
        ordering = ['name']
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return str(self.name)

    def clean(self):
        super().clean()
        self.slug = slugify(self.name)

        if self.parent_company == self:
            raise ValidationError({
                'parent_company': _("Cannot have itself as a parent.")
            })

        if self.parent_company and self.parent_company.parent_company:
            raise ValidationError({
                'parent_company': _("Maximum depth reached.")
            })

        if '{{ url }}' not in self.sms_template:
            raise ValidationError({
                'sms_template': _(
                    "{{ url }} must be present in the SMS template."
                )
            })

    def get_absolute_url(self):
        return reverse_lazy('panel:index', args=[self.slug])
    
    def get_absolute_merchant_url(self):
        return reverse_lazy('public:merchant_detail', args=[self.slug])


def post_save_company(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        user.collaborator_set.get_or_create(company=instance)


signals.post_save.connect(post_save_company, sender=Company)
