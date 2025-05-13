# Import all blueprints from modules
from .main_views import main_bp
from .user_views import user_bp
from .auth_views import auth_bp
from .cart_views import cart_bp
from .product_views import product_bp
from .order_views import order_bp
from .admin_views import admin_bp
from .driver_views import driver_bp
from .restaurant_views import restaurant_bp


# Import session management utilities
from .utils import (
    is_logged_in, get_user_id, get_user_role, 
    set_user_role, clear_user_session, get_user_cart
)

# Export all blueprints
__all__ = [
    'main_bp', 'user_bp', 'auth_bp', 'cart_bp', 'product_bp',
    'order_bp', 'admin_bp', 'driver_bp', 'restaurant_bp'
]
