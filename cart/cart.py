from django.conf import settings

from inventory.models import BrewProduct

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['inventory'] = BrewProduct.objects.get(pk=p)
        
        for item in self.cart.values():
            item['total_price'] = item['inventory'].price * item['quantity']

            yield item
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def add(self, inventory_id, quantity=1, update_quantity=False):
        inventory_id = str(inventory_id)
        
        if inventory_id not in self.cart:
            self.cart[inventory_id] = {'quantity': 1, 'id': inventory_id}
        
        if update_quantity:
            self.cart[inventory_id]['quantity'] += int(quantity)

            if self.cart[inventory_id]['quantity'] == 0:
                self.remove(inventory_id)
                        
        self.save()
    
    def remove(self, inventory_id):
        if inventory_id in self.cart:
            del self.cart[inventory_id]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
    
    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['inventory'] = BrewProduct.objects.get(pk=p)

        return sum(item['quantity'] * item['inventory'].price for item in self.cart.values())