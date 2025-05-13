from flask import Blueprint, request, render_template, redirect, url_for, flash
from forms import RegistrationForm
from models import User
from utils import get_user_id
from flask_mysqldb import MySQL

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # Assuming this is your form for user registration

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        user = User(username=username, email=email)
        user.set_password(password)  # Ensure that `set_password` hashes the password
        
        cur = MySQL.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO users (username, email, password_hash, role)
                VALUES (%s, %s, %s, %s)
            """, (user.username, user.email, user.password_hash, user.role))  # Adjust field names if needed.
            MySQL.connection.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('auth.login'))  # Assuming your login route is set up
        except Exception as e:
            MySQL.connection.rollback()
            flash(f'Error registering user: {e}', 'danger')
        finally:
            cur.close()

    return render_template('register.html', form=form)

@user_bp.route('/user/<int:user_id>')
def user_profile(user_id):
    # Retrieve the user profile and associated orders
    cursor = MySQL.connection.cursor()
    user = User.get_user_by_id(cursor, user_id)
    
    if user:
        # Assuming the `User` class has an attribute or method `orders`
        return render_template('profile.html', user=user, orders=user.orders)
    
    return "User not found", 404
