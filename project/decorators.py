from flask import session, redirect, url_for, flash, request
from functools import wraps

def login_required(f):
    """
    Custom decorator to ensure a user is logged in.
    Redirects to login page if not.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # Store the current URL for redirecting after login
            session['next_url'] = request.url
            flash('Please log in to access this page.', 'info')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Custom decorator to ensure a user is logged in and has admin role.
    Redirects to login page if not logged in, or home page if not admin.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # Store the current URL for redirecting after login
            session['next_url'] = request.url
            flash('Please log in to access this page.', 'info')
            return redirect(url_for('auth.login'))
        
        if session.get('user_role') != 'admin':
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('main.index'))
            
        return f(*args, **kwargs)
    return decorated_function

def restaurant_manager_required(f):
    """
    Custom decorator to ensure a user is logged in and has restaurant_manager role.
    Redirects to login page if not logged in, or home page if not a restaurant manager.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # Store the current URL for redirecting after login
            session['next_url'] = request.url
            flash('Please log in to access this page.', 'info')
            return redirect(url_for('auth.login'))
        
        if session.get('user_role') != 'restaurant_manager':
            flash('Access denied. Restaurant manager privileges required.', 'danger')
            return redirect(url_for('main.index'))
            
        return f(*args, **kwargs)
    return decorated_function