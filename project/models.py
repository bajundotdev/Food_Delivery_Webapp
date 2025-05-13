from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum

###################
# Enums
###################

class UserRole(Enum):
    CUSTOMER = "Customer"
    ADMIN = "Admin"
    DRIVER = "Delivery Driver"
    RESTAURANTOWNER = "Restaurant Manager"

class OrderStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class PaymentMethod(Enum):
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    
class DriverStatus(Enum):
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"

class ProductCategory(Enum):
    MAIN_COURSE = "Main"

###################
# User Models
###################

@dataclass
class User:
    id: str
    name: str
    phone: str
    email: str
    password: str
    profile_picture_url: str = ""
    role: UserRole = UserRole.CUSTOMER
    
    def get_url(self):
        """Return URL to user profile."""
        return f"/user/profile/{self.id}"
    
    def is_admin(self):
        """Check if user has admin role."""
        return self.role == UserRole.ADMIN

@dataclass
class DriverVehicle:
    id: int
    name: str
    plate_number: str

    def get_url(self):
        """Return URL to driver vehicle."""
        return f"/driver/vehicle"

@dataclass
class UserAddress:
    id: str
    user_id: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def get_url(self):
        """Return URL to edit address page."""
        return f"/user/address/{self.id}"
        
    def full_address(self):
        """Return formatted full address string."""
        parts = [self.street]
        if self.city and self.state:
            parts.append(f"{self.city}, {self.state}")
        elif self.city:
            parts.append(self.city)
        elif self.state:
            parts.append(self.state)
        
        if self.postal_code:
            parts.append(self.postal_code)
        
        if self.country:
            parts.append(self.country)
        
        return ", ".join(parts)

###################
# Driver Models
###################
@dataclass
class Driver:
    id: str
    user_id: str
    phone: str
    status: DriverStatus = DriverStatus.AVAILABLE
    
    def get_url(self):
        """Return URL to driver detail page."""
        return f"/driver/{self.id}"
    
    def assign_to_order(self, order_id: str):
        """Assign driver to an order."""
        # Implementation needed
        pass

###################
# Restaurant Models
###################
@dataclass
class Restaurant:
    id: str
    name: str
    address: str
    phone: str
    email: str
    website: str
    description: str
    image_url: str = ""
    
    def get_url(self):
        """Return URL to restaurant detail page."""
        return f"/restaurant/{self.id}"

###################
# Product Models
###################
@dataclass
class Product:
    id: str
    name: str
    description: str
    category: ProductCategory.MAIN_COURSE
    restaurant_id: str
    price: float = 0.00
    image_url: str = ""
    
    def get_url(self):
        """Return URL to product detail page."""
        return f"/product/{self.id}"


###################
# Cart Models
###################
@dataclass
class CartItem:
    id: str
    product_id: str
    products: List[Product] = field(default_factory=list)
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

###################
# Order Models
###################
@dataclass
class OrderItem:
    id: str
    product_id: str
    products: List[Product] = field(default_factory=list)
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
    def create_from_cart(user_id: str, cart: Cart, address: str, payment_method: PaymentMethod):
        """Create a new order from a cart."""
        # Implementation needed
        pass
    
    def calculate_total(self):
        """Calculate the total price of the order."""
        self.total = sum(item.get_subtotal() for item in self.items)
        return self.total
    
    def update_status(self, status: OrderStatus):
        """Update order status."""
        self.status = status

###################
# Admin Models
###################
@dataclass
class AdminLog:
    id: str
    admin_id: str
    action: str
    entity_type: str
    entity_id: str
    details: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    @staticmethod
    def log_action(admin_id: str, action: str, entity_type: str, entity_id: str, details: str = ""):
        """Log an admin action."""
        # Implementation needed
        pass

###################
# Search Models
###################
@dataclass
class SearchResult:
    type: str  # 'product', 'restaurant', etc.
    item: object  # The actual object (Product, Restaurant, etc.)

@dataclass
class Search:
    query: str
    user_id: str
    results: List[SearchResult] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    @staticmethod
    def search_all(query: str):
        """Search across all relevant entities."""
        # Implementation needed
        pass