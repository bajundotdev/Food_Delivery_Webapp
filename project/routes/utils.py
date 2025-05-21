from flask import session

# Shared functions across the application
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

def get_user_cart(user_id):
    """Get the current user's cart from the session."""
    # Check if the cart exists in the session
    if 'cart' not in session:
        # If not, initialize a new cart with user_id and empty items
        session['cart'] = {
            'user_id': user_id,
            'items': []
        }
    return session['cart']

def save_cart(cart):
    """Save the cart to the session."""
    session['cart'] = cart

def clear_user_session():
    """Clear user session data."""
    session.clear()
