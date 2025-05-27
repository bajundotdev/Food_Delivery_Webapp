from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from project.db import *
from project.session import *
from project.forms import CartForm, LoginForm
# Create blueprints for different sections of the application
main_bp = Blueprint('main', __name__)

###################
# Main Routes
###################

@main_bp.route('/',methods=['GET'])
def index():
    """Homepage route."""
    cart_form = CartForm()
    categories = get_all_category()

    if request.method == 'GET':        
        query = request.args.get('search_food', '').strip()

        if query:
            featured_products = search_product(query)
        else:
            featured_products = get_all_products()  

    return render_template('index.html', 
                           categories=categories,
                           query=query,
                           products=featured_products,
                           cart_form=cart_form)

@main_bp.post('/cart/<int:product_id>/')
def adding_to_cart(product_id):
    add_to_cart(product_id)
    return redirect(url_for('main.index'))

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
    #add_order_to_db(10,2,OrderStatus.PENDING, 20.99, "Success" ,"Debit Card")
    
    session_cart = session.get('shopping_cart')

    """Display all orders."""
    driver_id = 1
    driver_status = get_driver_status_by_driver_id(1)
    orderered_products = get_all_orders_and_products()
    order = get_all_orders()
    order_item = get_all_orders_by_id(3)
    order_item_by_user = get_all_orders_by_user_id(10)
    order_by_status = get_all_orders_by_status("Completed")
    cart_items = get_uncheckedout_cart_items_by_user_id(5)
    user_items = get_all_cart_items_by_user_id(9)
    driver_orders = get_all_orders_by_driver_id_status(driver_id, "Ready")
    completed_orders = get_all_orders_by_status("Ready")
    set_driver_status(driver_id, "Unavailable")
    delete_cart_item_from_db(6,9)
    return render_template('/test.html',
                           session_cart = session_cart, 
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