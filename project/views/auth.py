from flask import Blueprint, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm
from project import MySQL

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (form.email.data,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Email already registered.', 'danger')
            cursor.close()
            return render_template('auth/register.html', form=form)

        hashed_password = generate_password_hash(form.password.data)
        cursor.execute(
            """
            INSERT INTO users (name, email, phone, address, password, role) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                form.name.data,
                form.email.data,
                form.phone.data,
                form.address.data,
                hashed_password,
                form.role.data
            )
        )
        mysql.connection.commit()
        cursor.close()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (form.email.data,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password'], form.password.data):
            session['user_id'] = user['id']
            session['user_role'] = user['role']
            flash('Logged in successfully.', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
