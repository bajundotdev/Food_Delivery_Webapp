#app/models
from .user import User
from .cart_order_product import Cart, CartItem, Order, OrderItem, Product


"""
User creates cart
User adds items to Cart
Cart Total calculation
Checkout and Create Order
Order Total calculation
Confirmed Order is allocated to available driver

User: Stores user data and authenticates users
Cart: Manages the items Customer plans to buy including adding/removing products
Order: Represents a completed transaction including the items bought and the order total.
Confirmed order locates available driver for delivery to CustomerOrder
Product: Represents a product available in the store, including its price and description

Key Features:

Complete Shop Flow:
User registration → Cart → Checkout → Delivery
Full product management
Price viewing
User Roles:
Customers (make orders)
Drivers (fulfill deliveries)
Admins (manage products)
Transaction Safety:
    Stock validation before checkout
    Operations
Clean Relationships:
    One-to-one: User ↔ Cart
    One-to-many: User ↔ Orders
    Many-to-many via join tables

"""

__all__ = ['User', 'Cart', 'CartItem', 'Order', 'OrderItem', 'Product']