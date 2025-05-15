from .main import main_bp
from .user import user_bp
from .auth import auth_bp
from .cart import cart_bp
from .order import order_bp
from .admin import admin_bp
from .checkout import checkout_bp

blueprints = [
    main_bp,
    user_bp,
    auth_bp,
    cart_bp,
    product_bp,
    order_bp,
    admin_bp
    checkout_bp
]
