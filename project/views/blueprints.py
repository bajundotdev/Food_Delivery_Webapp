from flask import Blueprint, render_template

# MAIN Blueprint
main_bp = Blueprint('main', __name__)
@main_bp.route('/')
def home():
    return render_template('home.html')

# USER Blueprint
user_bp = Blueprint('user', __name__, url_prefix='/user')
@user_bp.route('/dashboard')
def user_dashboard():
    return render_template('user/dashboard.html')

# AUTH Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')
@auth_bp.route('/logout')
def logout():
    return render_template('auth/logout.html')


# CART Blueprint
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')
@cart_bp.route('/')
def view_cart():
    return render_template('cart/view.html')


# PRODUCT Blueprint
product_bp = Blueprint('product', __name__, url_prefix='/products')
@product_bp.route('/')
def product_list():
    return render_template('products/list.html')

@product_bp.route('/<int:product_id>')
def product_detail(product_id):
    return render_template('products/detail.html', product_id=product_id)


# ORDER Blueprint
order_bp = Blueprint('order', __name__, url_prefix='/orders')
@order_bp.route('/')
def order_history():
    return render_template('orders/history.html')

# ADMIN Blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
@admin_bp.route('/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')

# CHECKOUT Blueprint
checkout_bp = Blueprint('checkout', __name__, url_prefix='/checkout')

# Register all blueprints in one place
blueprints = [
    main_bp,
    user_bp,
    auth_bp,
    cart_bp,
    product_bp,
    order_bp,
    admin_bp
]
