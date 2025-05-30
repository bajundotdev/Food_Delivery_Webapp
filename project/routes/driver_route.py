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

    user_details = get_user_info_with_address_by_user_id(user_id)
    # print(user_details)

    driver = get_driver_details_by_user_id(user_id)
    driver_id = driver[0].id
    all_orders_by_driver = get_all_orders_by_driver(driver_id)

    orderReady = get_all_orders_by_status(status="Ready")
    for order in orderReady:
        order.items = get_all_order_items_by_order_id_status(order.id, 'Ready')
        

    order_for_delivery = get_all_orders_by_status(status="For Delivery") 
    orderCompleted = get_all_orders_by_status(status="Completed") 

    return render_template('driver/dashboard.html', user_details=user_details, 
                                                driver=driver, 
                                                orderCompleted=orderCompleted, 
                                                order_for_delivery=order_for_delivery,
                                                orderReady=orderReady,
                                                all_orders_by_driver=all_orders_by_driver)

@driver_bp.route('/confirm_delivery', methods=['POST'])
@login_required
@driver_required
def confirm_delivery():
    user_session = session.get('user')
    user_id = user_session['user_id']
    driver = get_driver_details_by_user_id(user_id)
    driver_id = driver[0].id
    order_id = request.form.get('order_id', '')

    try:
        set_order_status_by_driver_id(order_id, driver_id, 'For Delivery')
        flash('Order confirmed for delivery!', 'success')
    except Exception as e:
        print("Error:", e)
        flash('Failed to confirm order for delivery.', 'danger')

    return redirect(url_for('driver.driver_dashboard'))

@driver_bp.route('/ongoing_delivery/<int:order_id>', methods=['GET', 'POST'])
@login_required
@driver_required
def view_ongoing_delivery(order_id):

    user_session = session.get('user')
    user_id = user_session['user_id']
    driver = get_driver_details_by_user_id(user_id)
    driver_id = driver[0].id

    action = request.form.get('order_status')
    status = ""

    if request.method == 'POST':
        try:
            if action == 'order_received':
                driver_complete_delivery(order_id)
            elif action == 'order_cancelled':
                status = str(request.form.get('cancelNote'))
                cancel_order(order_id, status)

            flash('Order status updated successfully!', 'success')
        except Exception as e:
            print("Error:", e)
            flash('Failed to update order status.', 'danger')
   
    if request.method == 'GET':
        order_details = get_all_orders_by_id(order_id)
        items_in_order = get_all_order_items_by_order_id(order_id)

        return render_template('driver/view_order.html', order_details=order_details, items_in_order=items_in_order)

    return redirect(url_for('driver.driver_dashboard'))

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

@driver_bp.route('/profile/update_status/<driver_id>', methods=['POST'])
@login_required
@driver_required
def update_driver_status(driver_id):
    driver_status = request.form.get('is_active', '')
    print(driver_id, driver_status)

    if request.method == 'POST':
        try:
            set_driver_is_active(driver_id, driver_status)
            flash('Status successfully updated!', 'success')
        except Exception as e:
            print("Error:", e)
            flash('Failed to update status.', 'danger')

    return redirect(url_for('driver.driver_dashboard'))
