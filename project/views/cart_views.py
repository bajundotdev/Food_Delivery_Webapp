from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models import Product
from forms.cart_forms import AddToCartForm
from utils import is_logged_in, get_user_cart, save_cart_to_session

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    form = AddToCartForm()
    
    # Check if user is logged in
    if not is_logged_in():
        flash('Please log in to add items to your cart', 'warning')
        return redirect(url_for('auth.login'))

    # Validate form submission
    if not form.validate_on_submit():
        flash('Invalid quantity', 'danger')
        return redirect(url_for('products.view_product', product_id=product_id))

    # Fetch the product from the database
    product = Product.get_by_id(product_id)
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('products.list_products'))

    # Get the user's cart
    cart = get_user_cart(session['user_id'])

    # Add the product to the cart
    cart.add_item(product, form.quantity.data)

    # Save the updated cart in the session
    save_cart_to_session(cart)

    # Notify the user
    flash(f'Added {form.quantity.data} of {product.name} to your cart.', 'success')
    return redirect(url_for('cart.view_cart'))

# Cart view to display the user's cart
@cart_bp.route('/view')
def view_cart():
    cart = get_user_cart(session.get('user_id'))
    return render_template('cart/view_cart.html', cart=cart)
