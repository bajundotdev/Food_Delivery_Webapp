from flask import current_app, g
from flask_mysqldb import MYSQL

class Database:
    @staticmethod
    """Get database connection."""
    if 'db' not in g:
        g.db = current_app.extensions['mysql'].connection
        g.cursor = g.db.cursor()
    return g.db, g.cursor

class UserInfo:
    def __init__(self, id=None, email=None, password=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

class ProductInfo:
    def __init__(self, id=None, description=None, price=None, image_url=None):
        self.id = id
        self.name = name
        self.description = description
        self.image_url = image_url

class BasketInfo:
    def __init__(self, id=None, product_id=None, quantity=None):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

    def add_item():
    def remove_item(basket_id):
    def clear(user_id):
    def save(self):


class OrderInfo:
    def __init__(self, id=None, product_id=None, quantity=None):
        self.id = id
        self.user_id = user_id
        self.status = status
        self.address = address
        self.payment_method = payment_method
        self.created_at = created_at
        self.driver_id = driver_id

    def create_from_cart(user_id, address, payment_method):
    def get_items(self):
    def update_status(self, status):
    def to_dict(self): #Convert order to dictionary
        return {
            'id': self.user_id
        }
    
class DriverInfo:
    def __init__(self, id=None, phone=None, status=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.status = status
    def get_all(): 
    
    def assign_to_order(self, order_id): #Assign this driver to an order
    
    def save(self)

class Menu:
    def __init__(self, id=None, product_id=None, category=None):
        self.id = id
        self.product_id = product_id
        self.category = category

class StoreInfo:
    def __init__(self, id=None, name=None, address=None, phone=None):
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone