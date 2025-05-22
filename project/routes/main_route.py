from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# Import dummy database db.py
from project.db import *
from project.session import *
# Create blueprints for different sections of the application
main_bp = Blueprint('main', __name__)

###################
# Main Routes
###################

@main_bp.route('/',methods=('POST', 'GET'))
def index():
    """Homepage route."""
    cart_data = session.get('shopping_cart')
    print(cart_data)
    # Get featured products and restaurants
    featured_products = get_all_products()[:4]  # Get first 4 products
    featured_restaurants = get_all_restaurants()[:3]  # Get first 3 restaurants

    return render_template('index.html',
                          products=featured_products,
                          restaurants=featured_restaurants)

@main_bp.route('/cart/<int:product_id>/')
def adding_to_cart(product_id):
    add_to_cart(product_id)
    #return redirect(url_for('main.index'))

@main_bp.route('/about')
def about():
    return render_template('about.html')  # Assuming you have an about.html template

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')  # Assuming you have a contact.html template


############################ DO NOT GO BEYOND THIS POINT #########################
############################ FOR TESTING ONLY ####################################
@main_bp.route('/test')
def order_list():
    ###session check####
    add_to_cart(int(2),1)


    """Display all orders."""
    driver_status = get_driver_status_by_driver_id(1)
    orderered_products = get_all_orders_and_products()
    order = get_all_orders()
    order_item = get_all_orders_by_id(2)
    order_item_by_user = get_all_orders_by_user_id(10)
    order_by_status = get_all_orders_by_status("Completed")
    cart_items = get_all_cart_items()
    user_items = get_all_cart_items_by_user_id(9)
    driver_orders = get_all_orders_by_driver_id_status(1, "Ready")
    completed_orders = get_all_orders_by_status("Completed")
    set_driver_status(1, "Unavailable")
    return render_template('/test.html', 
                           driver_status=driver_status,
                           orderered_products=orderered_products,
                           orders_users = order,
                           order_item=order_item,
                           order_item_by_user=order_item_by_user,
                           order_by_status=order_by_status,
                           cart_items=cart_items,
                           user_items=user_items,
                            driver_orders = driver_orders,
                            completed_orders=completed_orders
                           )