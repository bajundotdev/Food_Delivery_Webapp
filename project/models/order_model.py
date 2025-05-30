from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum

#####################
# Enums             #
#####################

class DeliveryOption(Enum):
    FOR_DELIVERY = "For Delivery"
    FOR_PICKUP = "For Pickup"

class OrderStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    READY = "Ready"
    DELIVERY_IN_PROGRESS = "Delivery in Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

# Customer view: upon checkout: status order = Pending (admin)
# Admin: once received order status = Pending, change the status = if accept ("In Progress -- Cooking")
# Admin: once order is READY, it will trigger the Driver side, status = "READY" na naay ready for delivery
# Driver: 

class PaymentMethod(Enum):
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"

#####################
# Order Models      #
#####################

@dataclass
class OrderItem:
    order_id: str
    product_id: str
    user_id: str
    #products: list = field(default_factory=list)  # Use plain list to avoid needing Product at import time
    quantity: int = 1
    price: float = 0.0  # Store the price at the time of order

    def get_subtotal(self):
        """Calculate subtotal for this item."""
        return self.price * self.quantity

@dataclass
class Order:
    id: str = ""
    user_id: str = ""
    driver_id: str = ""
    status: OrderStatus = OrderStatus.PENDING
    total: float = 0.0
    payment_status: str = ""
    payment_method: PaymentMethod = PaymentMethod.CASH
    placed_at: datetime = field(default_factory=datetime.now)
    delivered_at: datetime = field(default_factory=datetime.now)
    canceled_at: str = ""
    notes: str = ""
    payment_invoice: str = ""
    delivery_option: DeliveryOption = DeliveryOption.FOR_DELIVERY
    fullname: str = ""
    email: str = ""
    phone_number: str = ""
    address: str = ""
    shipping_fee: float = 0.0
    packaging_fee: float = 0.0
    cancellation_notes: str = ""
    items: List[OrderItem] = field(default_factory=lambda: [])

    def get_url(self):
        """Return URL to order detail page."""
        return f"/order/{self.id}"
    
    @staticmethod
    def create_from_cart(user_id: str, cart, address: str, payment_method: PaymentMethod):
        """Create a new order from a cart."""
        from models import Product, Cart
        # Implementation needed
        pass
    
    def update_status(self, status: OrderStatus):
        """Update order status."""
        self.status = status