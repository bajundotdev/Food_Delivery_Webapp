from .admin_route import admin_bp
from .auth_route import auth_bp
from .main_route import main_bp
from .cart_route import cart_bp
from .product_route import product_bp
from .user_route import user_bp
from .driver_route import driver_bp
from .error_handlers_route import error_bp

all_blueprints = [
    admin_bp,
    auth_bp,
    main_bp,
    cart_bp,
    product_bp,
    user_bp,
    error_bp,
    driver_bp
]