from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import Product

# Create your models here.
class Category(models.Model):
    
    company = models.ForeignKey(
        'core.Company', on_delete=models.CASCADE, verbose_name=_("Company")
    )
    
    title = models.CharField(max_length=50)
    
    description = models.TextField()
    
    products = models.ManyToManyField(Product, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title