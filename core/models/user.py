from django.contrib.auth.models import UserManager, AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _

from paymentsAPI.stripe.customer import create_customer

class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_by_email(self, username):
        return self.get(**{self.model.EMAIL_FIELD: username})


class User(AbstractUser):
    username = None  # noqa

    objects = UserManager()
    
    email = models.EmailField(
        unique=True, verbose_name=_("Email")
    )
    companies = models.ManyToManyField(
        'core.Company', blank=True, through='Collaborator', related_name='+',
        verbose_name=_("Companies")
    )

    is_customer = models.BooleanField(default=False, verbose_name=_("Customer Status"))

    is_merchant = models.BooleanField(default=False, verbose_name=_("Merchant Status"))

    customer_id = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def shipping_address(self):
        return self.shippingaddress_set.filter(default=True).first()
    
    @property
    def addresses(self):
        return self.shippingaddress_set.all()
    
    @property
    def description(self):
        return 'Descripción para el usuario {}'.format(self.first_name)
    
    @property
    def shipping_address(self):
        return self.shippingaddress_set.filter(default=True).first()
    
    @property
    def billing_profile(self):
        return self.billingprofile_set.filter(default=True).first()

    @property
    def billing_profiles(self):
        return self.billingprofile_set.all().order_by('-default')
    
    def has_shipping_address(self):
        return self.shipping_address is not None
    
    def has_shipping_addresses(self):
        return self.shippingaddress_set.exists()

    def orders_completed(self):
        return self.order_set.filter(status='pending')
    
    def has_customer(self):
        return self.customer_id is not None

    def has_billing_profiles(self):
        return self.billingprofile_set.exists()
    
    def create_customer_id(self):
        if not self.has_customer():
            customer = create_customer(self)
            self.customer_id = customer.id
            self.save()

    def as_collaborator(self, company):
        if not company:
            return

        if any([self.is_staff or self.is_superuser]):
            collaborator, created = self.collaborator_set.get_or_create(
                company=company
            )
            return collaborator

        try:
            return self.collaborator_set.get(company=company, is_active=True)
        except ObjectDoesNotExist:
            return

    def has_shipping_address(self):
        return self.shipping_address is not None


    def __str__(self):
        return self.get_full_name()
    
    class Meta:
        ordering = ['email', ]
        permissions = (
            ('remove_user', 'Can remove user'),
        )
        verbose_name = _("user")
        verbose_name_plural = _("user")
