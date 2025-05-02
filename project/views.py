# views.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import User, Order, Cart, Product, Menu, Driver, Store
from forms import UserForm, LoginForm, CartForm, OrderForm, ProductForm, ReviewForm, SearchForm, ContactForm, DriverForm
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'username'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'database_name'

# Initialize MySQL
mysql = MySQL(app)

###################
# Main Routes
###################

@app.route('/')
def index():
    """Homepage route."""
    return render_template('index.html')

###################
# User Routes
###################

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """View and edit user profile on the same page."""
    if 'user_id' not in session:
        flash('Please log in to view your profile')
        return redirect(url_for('login'))
        
    user_id = session.get('user_id')
    user = User.get_by_id(user_id)
    
    if not user:
        flash('User not found')
        return redirect(url_for('login'))
    
    # Get user's recent orders
    orders = Order.get_by_user(user_id)
    
    form = UserForm()
    
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.save()
        
        flash('Profile updated successfully!')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        # Populate form with user data
        form.name.data = user.name
        form.email.data = user.email
    
    return render_template('profile.html', 
                          user=user.to_dict(),
                          orders=[order.to_dict() for order in orders], 
                          form=form)

###################
# Authentication Routes
###################

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    form = LoginForm()
    
    if form.validate_on_submit():
        # Example login logic
        username = form.username.data
        password = form.password.data
        
        user = User.get_by_email(username)
        if user and user.password == password:  # In production, use proper password hashing!
            session['user_id'] = user.id
            flash('Login successful!')
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """User logout route."""
    session.pop('user_id', None)
    flash('You have been logged out')
    return redirect(url_for('index'))

###################
# Cart Routes
###################

@app.route('/cart')
def view_cart():
    """View cart contents."""
    if 'user_id' not in session:
        flash('Please log in to view your cart')
        return redirect(url_for('login'))
        
    user_id = session.get('user_id')
    cart_items = Cart.get_by_user(user_id)
    
    return render_template('cart.html', cart_items=cart_items)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add item to cart."""
    if 'user_id' not in session:
        flash('Please log in to add items to your cart')
        return redirect(url_for('login'))
        
    user_id = session.get('user_id')
    quantity = int(request.form.get('quantity', 1))
    
    Cart.add_item(user_id, product_id, quantity)
    flash('Item added to cart')
    
    return redirect(url_for('view_cart'))

###################
# Menu Routes
###################

@app.route('/menu')
def view_menu():
    """Display menu categories."""
    categories = Menu.get_categories()
    return render_template('menu.html', categories=categories)

@app.route('/menu/<category>')
def menu_category(category):
    """Display menu items for a category."""
    items = Menu.get_by_category(category)
    return render_template('menu_category.html', items=items, category=category)

###################
# Order Routes
###################

@app.route('/orders')
def view_orders():
    """View user's orders."""
    if 'user_id' not in session:
        flash('Please log in to view your orders')
        return redirect(url_for('login'))
        
    user_id = session.get('user_id')
    orders = Order.get_by_user(user_id)
    
    return render_template('orders.html', orders=orders)

@app.route('/orders/create', methods=['GET', 'POST'])
def create_order():
    """Create a new order."""
    if 'user_id' not in session:
        flash('Please log in to place an order')
        return redirect(url_for('login'))
        
    user_id = session.get('user_id')
    form = OrderForm()
    
    if form.validate_on_submit():
        address = form.address.data
        payment_method = form.payment_method.data if hasattr(form, 'payment_method') else 'cash'
        
        order = Order.create_from_cart(user_id, address, payment_method)
        if order:
            flash('Order placed successfully!')
            return redirect(url_for('view_orders'))
        else:
            flash('Error placing order')
    
    cart_items = Cart.get_by_user(user_id)
    return render_template('create_order.html', form=form, cart_items=cart_items)

###################
# Admin Routes
###################

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard."""
    # Add admin authentication check here
    return render_template('admin/dashboard.html')

###################
# Driver Routes
###################

@app.route('/drivers')
def view_drivers():
    """View all drivers."""
    drivers = Driver.get_all()
    return render_template('drivers.html', drivers=drivers)