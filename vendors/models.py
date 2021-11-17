from django.db import models
from django.contrib.auth.models import User
import time

# Create your models here.

class Vendor(models.Model):
   
  # Vendor model extends the built-in Django User Model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True, upload_to='vendor_profile/')
    created_at = models.DateTimeField(auto_now_add=True)
  
    address = models.CharField(verbose_name="Address", max_length=100, null=True, blank=True)
    locality = models.CharField(verbose_name="Locality", max_length=100, null=True, blank=True)
    state = models.CharField(verbose_name="State", max_length=100, null=True, blank=True)
    postal_code = models.CharField(verbose_name="Postal Code", max_length=9, null=True, blank=True)
    country = models.CharField(verbose_name="Country", max_length=50, null=True, blank=True)
    longitude = models.CharField(verbose_name="Longitude", max_length=50, null=True, blank=True)
    latitude = models.CharField(verbose_name="Latitude", max_length=50, null=True, blank=True)
  
    has_profile = models.BooleanField(default = False)
  
    is_active = models.BooleanField(default = True)
  
    def __str__(self):
        return self.user    
    
    class Meta:
        ordering = ['company_name', '-created_at']
        
    def get_balance(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)
    
    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=True, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)