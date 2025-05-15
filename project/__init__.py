from flask import Flask, render_template, request, redirect, url_for, flash, session, current_app
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import timedelta

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'BetterSecretNeeded123'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'your_mysql_user'
    app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
    app.config['MYSQL_DB'] = 'your_database'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

    mysql.init_app(app)
    
    # Decorators
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in first.', 'warning')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function

    def admin_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session or session['user_role'] != 'admin':
                flash('Admin access required.', 'danger')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function

    # Register routes here or import blueprints and register
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            role = request.form.get('role', 'user')

            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash('Email already registered.', 'danger')
                cursor.close()
                return render_template('register.html')

            hashed_password = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                (name, email, hashed_password, role)
            )
            mysql.connection.commit()
            cursor.close()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()

            if user and check_password_hash(user[3], password):  # password is 4th column index
                session['user_id'] = user[0]
                session['user_role'] = user[4]
                flash('Logged in successfully.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password.', 'danger')

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/admin')
    @login_required
    @admin_required
    def admin_panel():
        return render_template('admin_panel.html')

    return app
