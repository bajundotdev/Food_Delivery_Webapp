#Imports all blueprints from each .py file

from .admin import admin_bp
from .auth import auth_bp
from .cart import cart_bp
from .drivers import drivers_bp
from .main import main_bp
from .menu import menu_bp
from .orders import orders_bp
from .users import users_bp

blueprints = [
    main_bp, 
    admin_bp, 
    auth_bp, 
    cart_bp, 
    drivers_bp, 
    menu_bp, 
    orders_bp, 
    users_bp, 
    ]
