from .main_route import main_bp
from .cart_route import cart_bp
from .product_route import product_bp
from .user_route import user_bp
from .driver_route import driver_bp

all_blueprints = [
    main_bp,
    cart_bp,
    product_bp,
    user_bp,
    driver_bp
]