from functools import wraps
from flask import session, redirect, url_for, flash
"""
Decorator to protect routes requiring login and specific roles.
This module provides decorators to enforce user authentication and role-based access control in Flask applications.
These decorators can be applied to Flask route functions to ensure that only authenticated users with the appropriate roles can access certain views.

WHAT HAPPENS (example for Admin Required):
1. User goes to /admin
2. login_required checks session['user'] exists
3. admin_required checks session['user']['role'] == 'Admin'
4. If fails: flash message + redirect to login/home
5. If passes: admin_dashboard() runs with correct name preserved

"""
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
        if 'user' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        role = session['user'].get('role')
        if role != 'Admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function

def driver_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        role = session['user'].get('role')
        if role != 'Delivery Driver':
            flash('Driver access required.', 'danger')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function