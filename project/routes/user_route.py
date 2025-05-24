from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from project.decorators import login_required
from project.forms import LoginForm
from project.session import *

# Import dummy database db.py
from project.db import *

from project.models import Order, User, UserAddress

# Create blueprints for different sections of the application
user_bp = Blueprint('user', __name__, url_prefix='/user')

# ###################
# # User Routes     #
# ###################

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_session = session.get('user')
    user_details = get_user_info_with_address_by_email(user_session['email'])
    if user_details:
        user_info = user_details[0]
        address = user_details[1]
    else:
        user_info = ""
        address = ""
    user_id = session.get('user').get('user_id')
    inordermo = get_all_orders_by_user_id(user_id)
    return render_template('user/profile.html', user_details=user_details, inordermo = inordermo, user_info=user_info, address = address)

@user_bp.route('/profile/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_profile(user_id):
    user_details = get_user_info_with_address_by_email(user_id)
    return render_template('user/profile/update_profile.html', user_details=user_details)

@user_bp.route('/view_order', methods=['GET', 'POST'])
@login_required
def view_order():
    order_id = request.args.get('order_id')
    laman = get_products_from_order_id(order_id)
    return render_template('user/view_order.html', laman = laman,)

# def profile():
#     """View and edit user profile on the same page."""
#     if not is_logged_in():
#         flash('Please log in to view your profile')
#         return redirect(url_for('auth.login'))
        
#     user_id = get_user_id()
#     user = User.get_by_id(user_id)
    
#     if not user:
#         flash('User not found')
#         return redirect(url_for('auth.login'))
    
#     # Get user's recent orders and addresses
#     orders = Order.get_by_user(user_id)
#     addresses = UserAddress.get_by_user(user_id)
    
#     form = UserForm()
    
#     if form.validate_on_submit():
#         user.name = form.name.data
#         user.email = form.email.data
#         # Other fields as needed
#         user.save()
        
#         flash('Profile updated successfully!')
#         return redirect(url_for('user.profile'))
#     elif request.method == 'GET':
#         # Populate form with user data
#         form.name.data = user.name
#         form.email.data = user.email
    
#     return render_template('profile.html', 
#                           user=user,
#                           orders=orders, 
#                           addresses=addresses,
#                           form=form)


# # Admin creation route
# @app.route('/admin/create', methods=['GET', 'POST'])
# def create_admin():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         admin = Admin(name=form.name.data, email=form.email.data, password=form.password.data, is_super_admin=form.is_super_admin.data)
#         admin.save()
#         flash('Admin created successfully!', 'success')
#         return redirect(url_for('admin_dashboard'))
#     return render_template('create_admin.html', form=form)

# # Driver creation route
# @app.route('/driver/create', methods=['GET', 'POST'])
# def create_driver():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         driver = Driver(name=form.name.data, email=form.email.data, password=form.password.data, phone=form.phone.data, address=form.address.data)
#         driver.save()
#         flash('Driver created successfully!', 'success')
#         return redirect(url_for('driver_dashboard'))
#     return render_template('create_driver.html', form=form)

# # Customer creation route
# @app.route('/customer/create', methods=['GET', 'POST'])
# def create_customer():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         customer = Customer(name=form.name.data, email=form.email.data, password=form.password.data, phone=form.phone.data, address=form.address.data)
#         customer.save()
#         flash('Customer created successfully!', 'success')
#         return redirect(url_for('customer_dashboard'))
#     return render_template('create_customer.html', form=form)
