from io import BytesIO
from PIL import Image
from django.db import models
from django.core.files import File
from vendors.models import Vendor
import time

# Create your models here.
class BrewCategory(models.Model):
    title = models.CharField(max_length=255)
    brew_origin = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.title
       
    class Meta: 
        ordering = ['brew_origin']
        verbose_name_plural = "Brews"
        
           
class BrewProduct(models.Model):
    brewcategory = models.ForeignKey(BrewCategory, related_name='inventory', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(blank=True, null=True, upload_to='uploads/')
    vendor = models.ForeignKey(Vendor, related_name='inventory', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    slug = models.SlugField(max_length=255)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x180.jpg'
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    
    
class BrewProductImage(models.Model):
    brewproduct = models.ForeignKey(BrewProduct, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.FileField(upload_to='uploads/', blank=True, null=True)   

    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x180.jpg'

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail