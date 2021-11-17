from inventory.models import BrewCategory

def menu_categories(request):
    categories = BrewCategory.objects.all()

    return {'menu_categories': categories}