from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum

#####################
# Enums             #
#####################

class OrderStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class PaymentMethod(Enum):
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"

#####################
# Order Models      #
#####################

@dataclass
class OrderItem:
    id: str
    product_id: str
    products: list = field(default_factory=list)  # Use plain list to avoid needing Product at import time
    quantity: int = 1
    price: float = 0.0  # Store the price at the time of order
    
    def get_subtotal(self):
        """Calculate subtotal for this item."""
        return self.price * self.quantity

@dataclass
class Order:
    id: str
    user_id: str
    status: OrderStatus = OrderStatus.PENDING
    address: str = ""
    payment_method: PaymentMethod = PaymentMethod.CASH
    driver_id: str = ""
    total: float = 0.0
    items: List[OrderItem] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def get_url(self):
        """Return URL to order detail page."""
        return f"/order/{self.id}"
    
    @staticmethod
    def create_from_cart(user_id: str, cart, address: str, payment_method: PaymentMethod):
        """Create a new order from a cart."""
        from models import Product, Cart
        # Implementation needed
        pass
    
    def calculate_total(self):
        """Calculate the total price of the order."""
        self.total = sum(item.get_subtotal() for item in self.items)
        return self.total
    
    def update_status(self, status: OrderStatus):
        """Update order status."""
        self.status = status