from flask import session
from datetime import datetime
from project.db import *
from project.models.cart_model import Cart, CartItem
from project.models.user_model import User, UserRole
from project.models.order_model import Order, OrderStatus
from project.db import get_product_by_id

"""
This module handles session management for the application.

1. "session management" - Controls user sessions
2. "initialises session variables" - Sets up session structure  
3. "retrieves user and cart information" - Gets data from session
4. "manage the shopping cart" - Add/remove/update cart items
"""

def init_session():
    """Initialize session with default values if they don't exist."""
    if 'created_at' not in session:
        session['created_at'] = datetime.now().isoformat()
    
    if 'last_activity' not in session:
        session['last_activity'] = datetime.now().isoformat()

def get_user():
    """Get user object from session data."""
    user_dict = session.get('user')
    if user_dict:
        return User(
            id=str(user_dict['user_id']),
            name=user_dict['firstname'],
            email=user_dict['email'],
            phone=user_dict['phone']
        )
    return None

def get_cart():
    """Get cart object from session data."""
    cart_data = session.get('shopping_cart')
    cart = Cart()
    
    if isinstance(cart_data, dict):
        for item in cart_data.get('items', []):
            if not item:
                return cart
            else:
                product = get_product_by_id(item['product']['id'])
                if product:
                    cart.add_item(CartItem(
                        id=str(item['id']),
                        product=product,
                        quantity=item['quantity']
                    ))
    return cart

def savebasket_to_session(basket):
    """Save basket/cart to session."""
    session['shopping_cart'] = {
        'items': [
            {
                'id': item.id,
                'quantity': item.quantity,
                'product': {
                    'id': item.product.id
                }
            } for item in basket.items
        ]
    }

def add_to_cart(product_id, quantity=1):
    """Add item to cart."""
    cart = get_cart()
    cart.add_item(CartItem(product=get_product_by_id(product_id), quantity=int(quantity)))
    _save_basket_to_session(cart)

def increment_cart_item(cart_id, quantity=1):
    cart = get_cart()
    for item in cart.items:
        if item.id == cart_id:
            item.increment_quantity()
    _save_basket_to_session(cart)

def minus_cart_item(cart_id, quantity=1):
    cart = get_cart()
    for item in cart.items:
        #print("item: ", item.id)
        if item.id == cart_id:
            print("Bawas")
            item.decrement_quantity()
    _save_basket_to_session(cart)
#     cart = get_cart()
#     cart =
#     cart.add_item(CartItem(product=get_product_by_id(product_id), quantity=int(quantity)))
#     _save_basket_to_session(cart)

def add_cart_item_from_db(cart_item):
    """Add cart item from database to session cart."""
    cart = get_cart()
    cart.add_item(cart_item)
    _save_basket_to_session(cart)


def remove_from_cart(item_id):
    """Remove item from cart."""
    cart = get_cart()
    print("removing from session")
    cart.remove_item(item_id)
    
    user_dict = session.get('user')
    if user_dict:
        user_id = session['user']['user_id']
    _save_basket_to_session(cart)

def empty_basket():
    """Clear all items from cart."""
    session['shopping_cart'] = {
        'items': []
    }
    #call db to delete items

def convert_basket_to_order(cart):
    """Convert cart to order object."""
    return Order(
        id=None,
        status=OrderStatus.PENDING,
        user_id=get_user().id,
        total=cart.total_cost(),
        items=cart.items
    )

# User session helper functions
def is_logged_in():
    """Check if user is logged in."""
    return 'user' in session and session['user'] is not None

def get_user_id():
    """Get current user ID."""
    user = get_user()
    return user.id if user else None

def get_user_role():
    """Get current user's role."""
    user_dict = session.get('user')
    return user_dict.get('role') if user_dict else None

def set_user_role(role):
    """Set the logged-in user's role."""
    if 'user' in session:
        session['user']['role'] = role

def get_user_cart(user_id):
    """Get the current user's cart from the session (dictionary format)."""
    if 'shopping_cart' not in session:
        session['shopping_cart'] = {
            'user_id': user_id,
            'items': []
        }
    return session['shopping_cart']

def save_cart(cart):
    """Save the cart to the session."""
    if hasattr(cart, 'items'):  # If it's a Cart object
        savebasket_to_session(cart)
    else:  # If it's a dictionary
        session['shopping_cart'] = cart

def clear_user_session():
    """Clear user session data."""
    session.clear()

# Role checking functions
def is_admin():
    """Check if current user is an admin."""
    role = get_user_role()
    return role == 'Admin' 

def is_driver():
    """Check if current user is a driver."""
    role = get_user_role()
    return role == 'Delivery Driver' 

def is_customer():
    """Check if current user is a customer."""
    role = get_user_role()
    return role == 'Customer' or role is None

def has_role(required_role):
    """Check if user has specific role."""
    return get_user_role() == required_role

# Cart utility functions
def get_cart_item_count():
    """Get total number of items in cart."""
    cart = get_cart()
    return sum(item.quantity for item in cart.items)

def refresh_session():
    """Update last activity timestamp."""
    session['last_activity'] = datetime.now().isoformat()