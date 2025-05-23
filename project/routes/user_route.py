from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from project.forms import LoginForm

# Import dummy database db.py
from project.db import *

from project.models import Order, User, UserAddress

# Create blueprints for different sections of the application
user_bp = Blueprint('user', __name__, url_prefix='/user')

##########################
# Session Management     #
##########################

def is_logged_in():
    """Check if user is logged in."""
    return 'user_id' in session

def get_user_id():
    """Get the logged-in user's ID."""
    return session.get('user_id')

def get_user_role():
    """Get the logged-in user's role."""
    return session.get('user_role')

def set_user_role(role):
    """Set the logged-in user's role."""
    session['user_role'] = role

def clear_user_session():
    """Clear user session data."""
    session.pop('user_id', None)
    session.pop('user_role', None)


# ###################
# # User Routes     #
# ###################

@user_bp.route('/profile', methods=['GET', 'POST'])
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
    return render_template('user/profile.html', inordermo = inordermo, user_info=user_info, address = address)
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


# from flask import render_template, redirect, url_for, flash
# from project import app
# from project.models.user import Admin, Driver, Customer
# from forms import RegistrationForm, LoginForm
# from models import modelslist

# # Registration route
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         # Depending on the role, create the appropriate user instance
#         if form.role.data == 'Admin':
#             user = Admin(name=form.name.data, email=form.email.data, password=form.password.data)
#         elif form.role.data == 'Driver':
#             user = Driver(name=form.name.data, email=form.email.data, password=form.password.data, phone=form.phone.data, address=form.address.data)
#         else:
#             user = Customer(name=form.name.data, email=form.email.data, password=form.password.data, phone=form.phone.data, address=form.address.data)
        
#         user.save()
#         flash('Registration successful!', 'success')
#         return redirect(url_for('login'))
    
#     return render_template('register.html', form=form)

# # Login route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Login logic here
#         flash('Login successful!', 'success')
#         return redirect(url_for('dashboard'))
#     return render_template('login.html', form=form)

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
