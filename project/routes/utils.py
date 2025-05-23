# filepath: project/utils.py
from flask import session, request, current_app
from functools import wraps
from datetime import datetime
from project.models import *

###################
# Session Management Functions
###################

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

def get_username():
    """Get the logged-in user's username."""
    return session.get('username')

def login_user(user_id, username, role='Customer'):
    """Log in a user by storing their info in session."""
    session['user_id'] = user_id
    session['username'] = username
    session['user_role'] = role
    session['logged_in'] = True
    session['login_time'] = datetime.now().isoformat()
    session.permanent = True

def logout_user():
    """Log out user by clearing session."""
    clear_user_session()

def clear_user_session():
    """Clear user session data."""
    session.clear()

###################
# Role Check Functions
###################

def is_admin():
    """Check if current user is admin."""
    return get_user_role() == 'Admin'

def is_driver():
    """Check if current user is driver."""
    return get_user_role() == 'Delivery Driver'

def is_customer():
    """Check if current user is customer."""
    return get_user_role() == 'Customer'

def is_restaurant_owner():
    """Check if current user is restaurant owner."""
    return get_user_role() == 'Restaurant Manager'

def can_access_admin():
    """Check if user can access admin panel."""
    return is_admin() or is_restaurant_owner()