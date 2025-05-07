from flask import current_app, g
from flask_mysqldb import MySQL
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class Database:
    @staticmethod
    def get_connection():
        """Get database connection."""
        if 'db' not in g:
            g.db = current_app.extensions['mysql'].connection
            g.cursor = g.db.cursor()
        return g.db, g.cursor

@dataclass
class UserInfo:
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    
    @staticmethod
    def get_by_id(user_id):
        # Implementation needed
        pass
        
    @staticmethod
    def get_by_email(email):
        # Implementation needed
        pass
        
    def save(self):
        # Implementation needed
        pass
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

@dataclass
class ProductInfo:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None

@dataclass
class BasketInfo:
    id: Optional[int] = None
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: int = 1

    @staticmethod
    def add_item(user_id, product_id, quantity=1):
        pass

    @staticmethod
    def remove_item(basket_id):
        pass

    @staticmethod
    def clear(user_id):
        pass
        
    @staticmethod
    def get_by_user(user_id):
        # Implementation needed
        pass

    def save(self):
        pass

@dataclass
class OrderInfo:
    id: Optional[int] = None
    user_id: Optional[int] = None
    status: Optional[str] = None
    address: Optional[str] = None
    payment_method: Optional[str] = None
    created_at: Optional[datetime] = None
    driver_id: Optional[int] = None

    @staticmethod
    def create_from_cart(user_id, address, payment_method):
        pass
        
    @staticmethod
    def get_by_user(user_id):
        # Implementation needed
        pass

    def get_items(self):
        pass

    def update_status(self, status):
        pass

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'address': self.address,
            'payment_method': self.payment_method,
            'created_at': self.created_at,
            'driver_id': self.driver_id
        }

@dataclass
class DriverInfo:
    id: Optional[int] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = None

    @staticmethod
    def get_all(): 
        pass

    def assign_to_order(self, order_id):
        pass
    
    def save(self):
        pass

@dataclass
class Menu:
    id: Optional[int] = None
    product_id: Optional[int] = None
    category: Optional[str] = None
    
    @staticmethod
    def get_categories():
        # Implementation needed
        pass
        
    @staticmethod
    def get_by_category(category):
        # Implementation needed
        pass

@dataclass
class StoreInfo:
    id: Optional[int] = None
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None