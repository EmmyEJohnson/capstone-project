from django.shortcuts import render
from inventory.models import BrewProduct

# Create your views here.

def frontpage(request):
    newest_products = BrewProduct.objects.all()[0:8]

    return render(request, 'home/frontpage.html', {'newest_products': newest_products})

def contact(request):
    return render(request, 'home/contact.html')