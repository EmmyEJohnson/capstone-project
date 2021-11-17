from django.contrib import admin

# Register your models here.

from .models import BrewCategory, BrewProduct, BrewProductImage

admin.site.register(BrewCategory)
admin.site.register(BrewProduct)
admin.site.register(BrewProductImage)