from flask import render_template, redirect, url_for, flash
from project import app
from project.models.user import Admin, Driver, Customer
from forms import RegistrationForm, LoginForm
from models import modelslist
# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Depending on the role, create the appropriate user instance
        if form.role.data == 'Admin':
            user = Admin(name=form.name.data, email=form.email.data, password=form.password.data)
        elif form.role.data == 'Driver':
            user = Driver(name=form.name.data, email=form.email.data, password=form.password.data, phone=form.phone.data, address=form.address.data)
        else:
            user = Customer(name=form.name.data, email=form.email.data, password=form.password.data, phone=form.phone.data, address=form.address.data)
        
        user.save()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login logic here
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

# Admin creation route
@app.route('/admin/create', methods=['GET', 'POST'])
def create_admin():
    form = RegistrationForm()
    if form.validate_on_submit():
        admin = Admin(name=form.name.data, email=form.email.data, password=form.password.data, is_super_admin=form.is_super_admin.data)
        admin.save()
        flash('Admin created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('create_admin.html', form=form)

# Driver creation route
@app.route('/driver/create', methods=['GET', 'POST'])
def create_driver():
    form = RegistrationForm()
    if form.validate_on_submit():
        driver = Driver(name=form.name.data, email=form.email.data, password=form.password.data, phone=form.phone.data, address=form.address.data)
        driver.save()
        flash('Driver created successfully!', 'success')
        return redirect(url_for('driver_dashboard'))
    return render_template('create_driver.html', form=form)

# Customer creation route
@app.route('/customer/create', methods=['GET', 'POST'])
def create_customer():
    form = RegistrationForm()
    if form.validate_on_submit():
        customer = Customer(name=form.name.data, email=form.email.data, password=form.password.data, phone=form.phone.data, address=form.address.data)
        customer.save()
        flash('Customer created successfully!', 'success')
        return redirect(url_for('customer_dashboard'))
    return render_template('create_customer.html', form=form)
