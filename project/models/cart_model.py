from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum
from uuid import uuid4

# Import models
from .product_model import Product

#####################
# Cart Models       #
#####################

@dataclass
class CartItem:
    product: Product
    cart_id: str = ""
    quantity: int = 1
    id: str = field(default_factory=lambda: str(uuid4()))
    
    def get_subtotal(self):
        """Calculate subtotal for this item."""
        subtotal = float(self.product.price * self.quantity)
        return subtotal
    
    def increment_quantity(self):
        """Increment the quantity of this cart item."""
        self.quantity += 1
        
    def decrement_quantity(self):
        """Decrement the quantity of this cart item."""
        if self.quantity > 1:
            self.quantity -= 1
        
@dataclass
class Cart:
    items: List[CartItem] = field(default_factory=lambda: [])
    
    def add_item(self, item: CartItem):
        """Add an item to the cart."""
        existing_item = self.check_item(item.product.id)
        if existing_item:
            existing_item.increment_quantity()
        else:
            self.items.append(item)
   
    def remove_item(self, item_id: str):
        """Remove an item from the cart by its product ID."""
        self.items = [item for item in self.items if item.id != item_id]
    
    def check_item(self, product_id: str):
        """Get an item from the cart by its product ID."""
        for item in self.items:
            if item.product.id == product_id:
                return item
        return None
    
    def get_item(self, product_id: str):
        """Get an item from the cart by its product ID."""
        for item in self.items:
            if item.id == product_id:
                return item
        return None
    
    def clear(self):
        """Empty the cart."""
        self.items = []
    
    def total_cost(self):
        """Calculate the total cost of the cart."""
        total_cost = sum(item.get_subtotal() for item in self.items)
        return f"%.2f" % (total_cost)