from flask import Blueprint, render_template, redirect, url_for
from models import Product, Cart, Order 
from forms import ConfirmOrderForm 
from views import Decorators 

product_bp = Blueprint('product', __name__, url_prefix='/product')
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/')
def view_cart():
    return render_template('cart.html')

# Product Listings View
@product_cart_bp.route('/products')
def products():
    products = Product.query.all()  # Fetch all products
    return render_template('products.html', products=products)

# Product Detail View
@product_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)  # Fetch product by ID
    return render_template('product_detail.html', product=product)

# Cart View
@cart_bp.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()  # Get user's cart items
    total_price = sum(item.product.price * item.quantity for item in cart_items)  # Calculate total price
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

# Checkout View
@product_cart_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = ConfirmOrderForm()
    if form.validate_on_submit():
        # Process order (create order, reduce cart items, etc.)
        new_order = Order(user_id=current_user.id, delivery_address=form.delivery_address.data)
        # Add items to order, handle payment, etc.
        return redirect(url_for('product_cart.order_confirmation', order_id=new_order.id))
    return render_template('checkout.html', form=form)

# Order Confirmation View
@product_cart_bp.route('/order/<int:order_id>/confirmation')
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)  # Fetch order by ID
    return render_template('order_confirmation.html', order=order)
