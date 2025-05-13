from typing import List
from product import Product
from user import User

###################
# Cart Models
###################
from flask import session
class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def get_subtotal(self):
        """Calculate subtotal for this item."""
        return self.product.price * self.quantity
    
    def increment_quantity(self):
        """Increment the quantity of this cart item."""
        self.quantity += 1
        
    def decrement_quantity(self):
        """Decrement the quantity of this cart item."""
        if self.quantity > 1:
            self.quantity -= 1

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product_id, quantity):
        """Add item to cart."""
        cart_item = next((item for item in self.items if item.product_id == product_id), None)
        if cart_item:
            cart_item.quantity += quantity
        else:
            self.items.append(CartItem(product_id, quantity))

    def remove_item(self, product_id):
        """Remove item from cart."""
        self.items = [item for item in self.items if item.product_id != product_id]
    
    def clear(self):
        """Empty the cart."""
        self.items = []
    
    def total_cost(self, products):
        """Calculate the total cost of the cart."""
        total = 0
        for item in self.items:
            product = next((prod for prod in products if prod.id == item.product_id), None)
            if product:
                total += item.get_subtotal(product.price)
        return total

cart = Cart()

