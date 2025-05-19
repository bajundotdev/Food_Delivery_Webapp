from flask import Blueprint, render_template, request, redirect, url_for, session, flash

# Import dummy database db.py
from project.db import get_all_products, get_all_restaurants, check_user, add_user
from project.models import Cart, CartItem, Product

# Create blueprints for different sections of the application
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

##########################
# Session Management     #
##########################

def is_logged_in():
    """Check if user is logged in."""
    return 'user_id' in session

def get_user_id():
    """Get the logged-in user's ID."""
    return session.get('user_id')

def get_user_role():
    """Get the logged-in user's role."""
    return session.get('user_role')

def set_user_role(role):
    """Set the logged-in user's role."""
    session['user_role'] = role

def clear_user_session():
    """Clear user session data."""
    session.pop('user_id', None)
    session.pop('user_role', None)

def get_user_cart():
    """Get or create cart for current user."""
    user_id = get_user_id()
    if not user_id:
        return None
    
    # Create a new cart if not in session
    if 'cart' not in session:
        session['cart'] = Cart(user_id=user_id)
    
    return session['cart']

###################
# Cart Routes     #
###################

# Dummy data for cart items
dummy_cart_items = []

@cart_bp.route('/')
def view_cart():
    return render_template('users/user_cart.html')
    # """View cart contents."""
    # if not is_logged_in():
    #     flash('Please log in to view your cart')
    #     return redirect(url_for('auth.login'))
        
    # cart = get_user_cart()
    # if not cart:
    #     flash('Unable to retrieve your cart')
    #     return redirect(url_for('main.index'))
    
    # return render_template('cart.html', 
    #                       cart=cart,
    #                       total=cart.total_cost())

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add item to cart."""
    if not is_logged_in():
        flash('Please log in to add items to your cart')
        return redirect(url_for('auth.login'))
        
    product = Product.get_by_id(product_id)
    if not product:
        flash('Product not found')
        return redirect(url_for('product.list_products'))
        
    quantity = int(request.form.get('quantity', 1))
    
    cart = get_user_cart()
    
    # Create a new CartItem
    cart_item = CartItem(
        id=f"temp_{product_id}",  # Will be replaced when saved
        product_id=product_id,
        product=product,
        quantity=quantity
    )
    
    # Add to cart
    cart.add_item(cart_item)
    
    # Save to session
    session['cart'] = cart
    
    flash('Item added to cart')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/remove/<product_id>')
def remove_from_cart(product_id):
    """Remove item from cart."""
    if not is_logged_in():
        flash('Please log in to modify your cart')
        return redirect(url_for('auth.login'))
        
    cart = get_user_cart()
    cart.remove_item(product_id)
    
    # Save to session
    session['cart'] = cart
    
    flash('Item removed from cart')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/checkout')
def checkout_cart():
    return render_template('users/checkout.html')