from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'Admin':
            flash('You must be an admin to access this page.', 'danger')
            return redirect(url_for('main.index'))  # Redirect non-admin users
        return f(*args, **kwargs)
    return decorated_function

def driver_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'Delivery Driver':
            flash('You must be a delivery driver to access this page.', 'danger')
            return redirect(url_for('main.index'))  # Redirect non-admin users
        return f(*args, **kwargs)
    return decorated_function