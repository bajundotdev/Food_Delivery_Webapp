# Imports all models from each .py file

from .cart import Cart
from .driver import Driver
from .menu import Menu
from .order import Order
from .product import Product
from .store import Store
from .user import User

model_classes = [Cart, Driver, Menu, Order, Product, Store, User]
# Needs to be saved into a SQL database
# Then defined in the app > __init__.py