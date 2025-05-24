from functools import wraps
from flask import session, redirect, url_for, flash, request
from project.routes.utils import is_logged_in, get_user_role

"""
Decorators wrap other functions to provide authenticiation and authorisation
"""
def login_required(f):
    """Require login access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('/login/'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Require admin access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # First check if logged in
        if not is_logged_in():
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('/login/'))
        
        # Check admin role
        if get_user_role() != 'Admin':
            flash('You must be an admin to access this page.', 'danger')
            return redirect(url_for('/'))  # Redirect non-admin users
        return f(*args, **kwargs)
    return decorated_function

def driver_required(f):
    """Require delivery driver access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # First check idf logged in
        if not is_logged_in():
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('/login/'))
        
        # Then check driver role
        if get_user_role() != 'Driver':
            flash('You must be a delivery driver to access this page.', 'danger')
            return redirect(url_for('/'))
        
        return f(*args, **kwargs)
    return decorated_function