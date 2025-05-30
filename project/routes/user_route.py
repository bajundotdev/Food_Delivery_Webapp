from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from project.decorators import login_required
from project.forms import LoginForm
from project.forms.customer_form import UserForm
from project.session import *
from werkzeug.utils import secure_filename
import os

# Import dummy database db.py
from project.db import *

from project.models import Order, User, UserAddress

# Create blueprints for different sections of the application
user_bp = Blueprint('user', __name__, url_prefix='/user')

###################### FILE UPLOAD #####################

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ###################
# # User Routes     #
# ###################

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_session = session.get('user')
    user_details = get_user_info_with_address_by_email(user_session['email'])

    # print(user_details)
    if request.method == 'POST':
        return redirect(url_for('user.profile'))

    if user_details:
        user_info = user_details[0]
        address = user_details[1]
        photo = user_details[0].profile_picture_url
        session['photo'] = photo
    else:
        user_info = ""
        address = ""
        photo = ""

    user_id = session.get('user').get('user_id')
    my_orders = get_all_orders_by_user_id(user_id)
    return render_template('user/profile/my_profile.html', user_details=user_details, 
                           my_orders = my_orders, 
                           user_info=user_info, 
                           address = address, 
                           photo = photo)

@user_bp.route('/profile/update/<string:email>', methods=['GET', 'POST'])
@login_required
def update_profile(email):
    user_details = get_user_info_with_address_by_email(email)
    return render_template('user/profile/update_profile.html', user_details=user_details)

@user_bp.route('/view_order', methods=['GET', 'POST'])
@login_required
def view_order():
    order_id = request.args.get('order_id')

    order_details = get_all_orders_by_id(order_id)
    driver_id = order_details.driver_id
    driver_details = get_driver_by_id(driver_id)
    if driver_details:
        driver = driver_details[0]
    else:
        driver = ""
    items_in_order = get_all_order_items_by_order_id(order_id)

    return render_template('user/view_order.html', order_details=order_details,
                                                driver_details=driver,
                                                items_in_order=items_in_order)

@user_bp.route('/user/save/', methods=('POST', 'GET'))
@login_required
def save_profile():
    if request.method == "POST":
        name = request.form.get('fullname')
        
        file = request.files.get('profile_image')

        if file and allowed_file(file.filename):
            print(file)
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER']+'/profile_photos', filename))

            update_user_profile(name,request.form.get('phone'), filename.request.form.get('email'))
            flash('Profile saved!', 'success')
            
        return redirect(url_for('user.profile'))

    return redirect(url_for('user.profile'), photo = session.get('photo'))

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
