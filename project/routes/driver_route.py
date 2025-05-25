from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from project.models import Driver, DriverStatus
from project.decorators import login_required, admin_required, driver_required

# Import dummy database db.py
from project.db import *

# Create blueprints for different sections of the application
driver_bp = Blueprint('driver', __name__, url_prefix='/driver')

#####################
# Driver Routes     #
#####################

@driver_bp.route('/')
@login_required
@driver_required
def driver_dashboard():
    """Display all drivers."""

    #get all orders na ready
    # for this order in orders
        #get the products
    #get all products orders from above order_id
    user_session = session.get('user')
    user_id = user_session['user_id']
    user_email = user_session['email']


    user_details = get_user_info_with_address_by_user_id(user_id)
    # print(user_details)

    driver = get_driver_details_by_user_id(user_id)
    driver_id = driver[0].id
    # orderReady = get_all_orders_by_status(status="Ready")
    all_orders = get_all_orders_and_products()

    # order = get_all_order_items_by_order_id(order_id)
    orderReady = get_all_orders_by_status(status="Ready")


    for order in orderReady:
        order.items = get_all_order_items_by_order_id_status(order.id, 'Ready')
        

    orderCompleted = get_all_orders_by_status(status="Completed") 

    return render_template('driver/dashboard.html', user_details=user_details, 
                                                driver=driver, 
                                                orderCompleted=orderCompleted, 
                                                orderReady=orderReady,
                                                all_orders=all_orders)

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

