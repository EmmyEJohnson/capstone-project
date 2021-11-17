from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AddToCartForm
from .models import BrewCategory, BrewProduct
from cart.cart import Cart
import random

# Create your views here.
def search(request):
    query = request.GET.get('query', '')
    brewproduct = BrewProduct.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'inventory/search.html', {'inventory': brewproduct, 'query': query})

def brewproduct(request, brewcategory_slug, brewproduct_slug):
    cart = Cart(request)

    brewproduct = get_object_or_404(BrewProduct, brewcategory__slug=brewcategory_slug, slug=brewproduct_slug)

    imagesstring = '{"thumbnail": "%s", "image": "%s", "id": "mainimage"},' % (brewproduct.get_thumbnail(), brewproduct.image.url)

    for image in brewproduct.images.all():
        imagesstring += ('{"thumbnail": "%s", "image": "%s", "id": "%s"},' % (image.get_thumbnail(), image.image.url, image.id))
    
    print(imagesstring)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            cart.add(brewproduct_id=brewproduct.id, quantity=quantity, update_quantity=False)

            messages.success(request, 'The brew was added to the cart')

            return redirect('inventory', brewcategory_slug=brewcategory_slug, brewproduct_slug=brewproduct_slug)
    else:
        form = AddToCartForm()

    similar_inventory = list(brewproduct.brewcategory.inventory.exclude(id=brewproduct.id))

    if len(similar_inventory) >= 4:
        similar_inventory = random.sample(similar_inventory, 4)

    context = {
        'form': form,
        'brewproduct': brewproduct,
        'similar_inventory': similar_inventory,
        'imagesstring': "[" + imagesstring.rstrip(',') + "]"
    }

    return render(request, 'inventory/brewproduct.html', context)

def brewcategory(request, brewcategory_slug):
    category = get_object_or_404(BrewCategory, slug=brewcategory_slug)

    return render(request, 'inventory/brewcategory.html', {'brewcategory': brewcategory})