from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm
from models import UserRole, User
from utils import is_logged_in

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        existing_user = User.get_by_email(form.email.data)
        if existing_user:
            print('Email already registered', 'danger')
            return render_template('register.html', form=form)
        
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            role=UserRole(form.role.data)
        )
        new_user.save()
        print('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.get_by_email(email)
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_role'] = user.role.value
            print('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            print('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    session.clear()
    print('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
