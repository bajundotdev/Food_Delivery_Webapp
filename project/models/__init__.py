from .admin_model import AdminLog
from .cart_model import Cart, CartItem
from .driver_model import Driver, DriverStatus
from .order_model import Order, OrderStatus
from .product_model import Product, ProductCategory
from .restaurant_model import Restaurant
from .user_model import User, UserRole, UserAddress

model_list = [AdminLog, Cart, CartItem, Driver, DriverStatus, Order, OrderStatus, Product, ProductCategory, Restaurant, User, UserRole, UserAddress]