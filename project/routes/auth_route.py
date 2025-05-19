from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from project.forms import LoginForm
from project.db import check_user
from project.routes.utils import clear_user_session

auth_bp = Blueprint('auth', __name__, url_prefix='/')

###################
# Authentication Routes
###################

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    # form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Example login logic
            user = check_user(form.username.data, form.password.data)

            if not user:
                flash('Invalid username or password', 'error')
                return redirect(url_for('main.login'))

            # Store full user info in session
            session['user'] = {
                'user_id': user.info.id,
                'firstname': user.info.name,
                'phone': user.info.phone,
                'email': user.info.email,
                'role': user.info.role,

            }
            session['logged_in'] = True
            flash('Login successful!')
            return redirect(url_for('main.profile'))
        
        # return render_template('login.html', form=form)
        return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """User logout route."""
    clear_user_session()
    flash('You have been logged out')
    return redirect(url_for('main.index'))