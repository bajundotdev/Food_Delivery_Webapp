# views.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import UserInfo, OrderInfo, BasketInfo, ProductInfo, Menu, DriverInfo, StoreInfo
from forms import UserForm, LoginForm, CartForm, OrderForm, ProductForm, ReviewForm, SearchForm, ContactForm, DriverForm

bp = Blueprint('main', __name__)

# Create blueprints for different sections of the application
main_bp = Blueprint('main', __name__)
user_bp = Blueprint('user', __name__, url_prefix='/user')
auth_bp = Blueprint('auth', __name__)
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')
menu_bp = Blueprint('menu', __name__, url_prefix='/menu')
order_bp = Blueprint('order', __name__, url_prefix='/orders')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
driver_bp = Blueprint('driver', __name__, url_prefix='/drivers')

###################
# Main Routes
###################

@main_bp.route('/')
def index():
    """Homepage route."""
    return render_template('index.html')

###################
# User Routes
###################

@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    """View and edit user profile on the same page."""
    if 'user_id' not in session:
        flash('Please log in to view your profile')
        return redirect(url_for('auth.login'))
        
    user_id = session.get('user_id')
    user = UserInfo.get_by_id(user_id)
    
    if not user:
        flash('User not found')
        return redirect(url_for('auth.login'))
    
    # Get user's recent orders
    orders = OrderInfo.get_by_user(user_id)
    
    form = UserForm()
    
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.save()
        
        flash('Profile updated successfully!')
        return redirect(url_for('user.profile'))
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

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    form = LoginForm()
    
    if form.validate_on_submit():
        # Example login logic
        username = form.username.data
        password = form.password.data
        
        user = UserInfo.get_by_email(username)
        if user and user.password == password:  # In production, use proper password hashing!
            session['user_id'] = user.id
            flash('Login successful!')
            return redirect(url_for('user.profile'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    """User logout route."""
    session.pop('user_id', None)
    flash('You have been logged out')
    return redirect(url_for('main.index'))

###################
# Cart Routes
###################

@cart_bp.route('/')
def view_cart():
    """View cart contents."""
    if 'user_id' not in session:
        flash('Please log in to view your cart')
        return redirect(url_for('auth.login'))
        
    user_id = session.get('user_id')
    cart_items = BasketInfo.get_by_user(user_id)
    
    return render_template('cart.html', cart_items=cart_items)

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add item to cart."""
    if 'user_id' not in session:
        flash('Please log in to add items to your cart')
        return redirect(url_for('auth.login'))
        
    user_id = session.get('user_id')
    quantity = int(request.form.get('quantity', 1))
    
    BasketInfo.add_item(user_id, product_id, quantity)
    flash('Item added to cart')
    
    return redirect(url_for('cart.view_cart'))

###################
# Menu Routes
###################

@menu_bp.route('/')
def view_menu():
    """Display menu categories."""
    categories = Menu.get_categories()
    return render_template('menu.html', categories=categories)

@menu_bp.route('/<category>')
def menu_category(category):
    """Display menu items for a category."""
    items = Menu.get_by_category(category)
    return render_template('menu_category.html', items=items, category=category)