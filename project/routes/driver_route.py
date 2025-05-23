from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from project.models import Driver, DriverStatus
from project.decorators import login_required, admin_required, driver_required

# Import dummy database db.py
from project.db import *

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

@driver_bp.route('/dashboard')
@login_required
@driver_required
def driver_dashboard():
    """Display all drivers."""

    #get all orders na ready
    # for this order in orders
        #get the products
    #get all products orders from above order_id
    user = session.get('user')
    user_id = user['user_id']
    driver = get_driver_details_by_user_id(user_id)
    driver_id = driver[0].id
    # orderReady = get_all_orders_by_status(status="Ready")
    orderReady = get_all_orders_and_products()


    orderCompleted = get_all_orders_by_status(status="Completed") 
    return render_template('driver/dashboard.html', driver=driver, orderCompleted=orderCompleted, orderReady=orderReady)

@driver_bp.route('/profile')
@login_required
@driver_required
def profile():
    """Display all drivers."""
    user = session.get('user')
    user_id = user['user_id']
    driver = get_driver_details_by_user_id(user_id)
    driver_id = driver[0].id
    orderCompleted = get_all_orders_by_driver_id_status(driver_id, status="Completed")

    return render_template('driver/profile.html', driver=driver, orderCompleted=orderCompleted)

