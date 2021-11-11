from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class VendorProfile(models.Model):
  
  # VendorProfile model extends the built-in Django User Model
  
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  company_name = models.CharField(max_length=255)
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  
  address = models.CharField(verbose_name="Address", max_length=100, null=True, blank=True)
  city = models.CharField(verbose_name="City", max_length=100, null=True, blank=True)
  state = models.CharField(verbose_name="State", max_length=100, null=True, blank=True)
  zip_code = models.CharField(verbose_name="Zip Code", max_length=9, null=True, blank=True)
  country = models.CharField(verbose_name="Country", max_length=50, null=True, blank=True)
  longitude = models.CharField(verbose_name="Longitude", max_length=50, null=True, blank=True)
  latitude = models.CharField(verbose_name="Latitude", max_length=50, null=True, blank=True)
  
  captcha_score = models.FloatField(default = 0.0)
  has_profile = models.BooleanField(default = False)
  
  is_active = models.BooleanField(default = True)
  
  def __str__(self):
      return f"{self.name}"
    
  