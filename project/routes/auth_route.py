from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from project.forms.authentication_form import LoginForm
from project.db import check_user
from project.routes.utils import clear_user_session

auth_bp = Blueprint('auth', __name__, url_prefix='/')

###################
# Authentication Routes
###################
# Registration route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')
    # form = RegistrationForm()
    # if form.validate_on_submit():
    #     # Depending on the role, create the appropriate user instance
    #     if form.role.data == 'Admin':
    #         user = Admin(name=form.name.data, email=form.email.data, password=form.password.data)
    #     elif form.role.data == 'Driver':
    #         user = Driver(name=form.name.data, email=form.email.data, password=form.password.data, phone=form.phone.data, address=form.address.data)
    #     else:
    #         user = Customer(name=form.name.data, email=form.email.data, password=form.password.data, phone=form.phone.data, address=form.address.data)
        
    #     user.save()
    #     flash('Registration successful!', 'success')
    #     return redirect(url_for('login'))
    
    # return render_template('register.html', form=form)

@auth_bp.route('/login/', methods=('POST', 'GET'))
def login():
    form = LoginForm()
    if request.method == 'POST':
        
        #if form.validate_on_submit():
            user = check_user(form.username.data, form.password.data)
            if not user:
                flash('Invalid username or password', 'error')
                return redirect(url_for('auth.login'))

            # Store full user info in session
            session['user'] = {
                'user_id': user.id,
                'firstname': user.name,
                'phone': user.phone,
                'email': user.email,
            }
            session['logged_in'] = True
            session['role'] = user.role
            flash('Login successful!')
            if session['role'] == "Admin":
                return redirect(url_for('admin.admin_dashboard'))
            elif session['role'] == "Customer":
                return redirect(url_for('user.profile'))
            elif session['role'] == "Delivery Driver":
                return redirect(url_for('driver.profile'))
            elif session['role'] == "Restaurant Owner":
                return redirect(url_for('user.profile'))
            #return redirect(url_for('main.profile'))
        
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    """User logout route."""
    clear_user_session()
    flash('You have been logged out')
    return redirect(url_for('main.index'))