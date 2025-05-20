from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum

# Import models
from .product_model import Product

#####################
# Cart Models       #
#####################

@dataclass
class CartItem:
    product: Product
    quantity: int = 1
    
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
        
@dataclass
class Cart:
    user_id: str
    items: List[CartItem] = field(default_factory=list)
    
    def add_item(self, item: CartItem):
        """Add an item to the cart."""
        existing_item = self.get_item(item.product_id)
        if existing_item:
            existing_item.increment_quantity()
        else:
            self.items.append(item)
    
    def remove_item(self, product_id: str):
        """Remove an item from the cart by its product ID."""
        self.items = [item for item in self.items if item.product_id != product_id]
    
    def get_item(self, product_id: str):
        """Get an item from the cart by its product ID."""
        for item in self.items:
            if item.product_id == product_id:
                return item
        return None
    
    def clear(self):
        """Empty the cart."""
        self.items = []
    
    def total_cost(self):
        """Calculate the total cost of the cart."""
        return sum(item.get_subtotal() for item in self.items)