from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from project.models import Driver, DriverStatus
from project.decorators import login_required, admin_required, driver_required

# Import dummy database db.py
from project.db import (get_all_products, 
                get_product_by_id,
                get_all_restaurants, 
                check_user, 
                add_user,
                get_all_driver)

# Create blueprints for different sections of the application
driver_bp = Blueprint('driver', __name__, url_prefix='/drivers')

##########################
# Session Management     #
##########################

# def is_logged_in():
#     """Check if user is logged in."""
#     return 'user_id' in session

# def get_user_id():
#     """Get the logged-in user's ID."""
#     return session.get('user_id')s

# def get_user_role():
#     """Get the logged-in user's role."""
#     return session.get('user_role')

# def set_user_role(role):
#     """Set the logged-in user's role."""
#     session['user_role'] = role

# def clear_user_session():
#     """Clear user session data."""
#     session.pop('user_id', None)
#     session.pop('user_role', None)


#####################
# Driver Routes     #
#####################

@driver_bp.route('/profile')
@login_required
@driver_required
def profile():
    """Display all drivers."""
    drivers = get_all_driver()
    return render_template('drivers/profile.html', drivers=drivers)

