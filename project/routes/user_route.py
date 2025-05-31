from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from project.decorators import login_required
from project.forms import LoginForm, PasswordChangeForm
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
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER']+'/profile_photos', filename))

            update_user_profile(name,request.form.get('phone'), filename.request.form.get('email'))
            flash('Profile saved!', 'success')
            
        return redirect(url_for('user.profile'))

    return redirect(url_for('user.profile'), photo = session.get('photo'))

@user_bp.route('/profile/change_password/', methods=['GET', 'POST'])
@login_required
def update_password():
    form = PasswordChangeForm()
    return render_template('user/profile/change_password.html', form=form)

@user_bp.route('/user/save_password/', methods=('POST', 'GET'))
@login_required
def save_password():
    if request.method == "POST":
        form = PasswordChangeForm()
        current_password = form.current_password.data
        new_password = form.confirm_password.data
        user = get_user()
        if form.validate_on_submit():
            if check_user(user.email, current_password):
                update_password_db(user.id, generate_password_hash(new_password))
                flash('Password changed!', 'success')
                return redirect(url_for('user.profile'))
            else:
                flash('Invalid password!', 'danger')
                return redirect(url_for('user.update_password'))
        else:
            for error in form.errors.values():
                for item in error:
                    flash(item, 'danger')

            return redirect(url_for('user.update_password'))
        
    return redirect(url_for('user.profile', form=form))