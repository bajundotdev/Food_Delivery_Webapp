from flask_mysqldb import MySQLdb
from datetime import datetime
from models import Cart, CartItem
from enum import Enum

class OrderStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

    @classmethod
    def get_all_values(cls):
        """Return all possible status values as strings."""
        return [status.value for status in cls]
    
class Order:
    """Model for customer orders using raw SQL queries."""
    def __init__(self, id, user_id, address="", payment_method="", driver_id="", total=0.0, items=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.status = ""
        self.address = address
        self.payment_method = payment_method
        self.driver_id = driver_id
        self.total = total
        self.items = items or []
        self.created_at = created_at or datetime.now()

    def get_url(self):
        return f"/order/{self.id}"

    @staticmethod
    def create_from_cart(user_id, cart, address, payment_method):
        pass

    def calculate_total(self):
        self.total = sum(item.get_subtotal() for item in self.items)
        return self.total

    def update_status(self, status):
        self.status = status

class OrderItem:
    def __init__(self, id, product_id, products=None, quantity=1, price=0.0):
        self.id = id
        self.product_id = product_id
        self.products = products or []
        self.quantity = quantity
        self.price = price

    def get_subtotal(self):
        return self.price * self.quantity
    
@staticmethod
def create_from_cart(cursor, user_id, cart_items, address, payment_method):
    created_at = datetime.now()
    status = OrderStatus.PENDING.value
    total = sum(item['price'] * item['quantity'] for item in cart_items)

    # Insert into orders table
    cursor.execute("""
        INSERT INTO orders (user_id, status, address, payment_method, total, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, status, address, payment_method, total, created_at))

    order_id = cursor.lastrowid  # Get the ID of the newly created order

    # Insert items into order_items table
    for item in cart_items:
        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, item['product_id'], item['quantity'], item['price']))

    return order_id
