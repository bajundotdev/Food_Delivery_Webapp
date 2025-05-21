from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from project.forms.authentication_form import LoginForm, RegistrationForm
from project.db import check_user, add_user, get_user_by_email
from project.routes.utils import clear_user_session

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
                # Store full user info in session
                session['user'] = {
                    'user_id': user.id,
                    'firstname': user.name,
                    'phone': user.phone,
                    'email': user.email,
                }
                session['logged_in'] = True
                session['role'] = user.role
                flash('Login successful!', 'primary')
                if session['role'] == "Admin":
                    return redirect(url_for('admin.admin_dashboard'))
                elif session['role'] == "Delivery Driver":
                    return redirect(url_for('driver.driver_dashboard'))
                elif session['role'] == "Customer":
                    return redirect(url_for('user.profile'))
        
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    """User logout route."""
    clear_user_session()
    flash('You have been logged out', 'primary')
    return redirect(url_for('main.index'))