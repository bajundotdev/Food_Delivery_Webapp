from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from project.forms.authentication_form import LoginForm, RegistrationForm, DriverRegistrationForm
from project.db import check_user, add_user, get_user_by_email, add_cart_item_to_db, get_uncheckedout_cart_items_by_user_id
from project.routes.utils import clear_user_session
from project.session import *
auth_bp = Blueprint('auth', __name__, url_prefix='/')

###################
# Authentication Routes
###################
# Registration route
@auth_bp.route('/register/', methods=('POST', 'GET'))
def register():
    form = RegistrationForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            # Check if the user already exists
            user = get_user_by_email(form.email.data)
            if user:
                flash('User already exists', 'error')
                return redirect(url_for('auth.register'))

            add_user(form)
            flash('Registration successful!')
            return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth_bp.route('/driver_register/', methods=('POST', 'GET'))
def driver_register():
    form = DriverRegistrationForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            # Check if the user already exists
            user = get_user_by_email(form.email.data)
            if user:
                flash('Email address already exists', 'error')
                return redirect(url_for('auth.driver_register'))

            add_driver(form)
            flash('Registration successful!', 'success')
            return redirect(url_for('auth.login'))

    return render_template('driver_register.html', form=form)

@auth_bp.route('/login/', methods=('POST', 'GET'))
def login():
    
    form = LoginForm()
    if request.method == 'POST':  
        if form.validate_on_submit():
            user = check_user(form.username.data, form.password.data)
            if not user:
                flash('Invalid username or password', 'error')
                return redirect(url_for('auth.login'))
            else:
                if user.is_active:
                    # Store full user info in session
                    session['user'] = {
                        'user_id': user.id,
                        'firstname': user.name,
                        'phone': user.phone,
                        'email': user.email,
                        'address_id': "",
        
                    }
                    session['logged_in'] = True
                    session['role'] = user.role
                    flash('Login successful!', 'success')
                    if session['role'] == "Admin":
                        return redirect(url_for('admin.admin_dashboard'))
                    elif session['role'] == "Delivery Driver":
                        return redirect(url_for('driver.driver_dashboard'))
                    elif session['role'] == "Customer":
                        user_id = session['user']['user_id']
                        cart_from_db = get_uncheckedout_cart_items_by_user_id(user_id)
                        for item in cart_from_db:
                            add_cart_item_from_db(item)  
                        return redirect(url_for('main.index'))
        
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    """User logout route."""
    if session['role'] == "Customer":
        user_id = session['user']['user_id']
        clear_cart_db(user_id)
        cart_items = session.get('shopping_cart')
        if cart_items:
            for item in cart_items.get('items', []):
                product_id = item['product']['id']
                
                quantity = item['quantity']
                item_id = item['id']
                add_cart_item_to_db(product_id ,user_id, quantity, item_id)

    clear_user_session()
    flash('You have been logged out', 'success')
    return redirect(url_for('main.index'))