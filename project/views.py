# views.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import User, UserAddress, Order, OrderItem, Cart, CartItem, Product, Driver, Restaurant, Search, ProductCategory
from .forms import LoginForm, RegistrationForm, UserForm, UserAddressForm, ContactForm, ReviewForm, SearchForm, CartForm, OrderForm, AdminUserForm, AdminSearchForm, ProductForm, RestaurantForm, DriverForm
from dataclasses import dataclass


# Import dummy database db.py
from db import get_all_products, get_all_restaurants


# Create blueprints for different sections of the application
main_bp = Blueprint('main', __name__)
user_bp = Blueprint('user', __name__, url_prefix='/user')
auth_bp = Blueprint('auth', __name__)
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')
product_bp = Blueprint('product', __name__, url_prefix='/products') 
order_bp = Blueprint('order', __name__, url_prefix='/orders')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
driver_bp = Blueprint('driver', __name__, url_prefix='/drivers')
restaurant_bp = Blueprint('restaurant', __name__, url_prefix='/restaurants')

###################
# Session Management
###################

def is_logged_in():
    """Check if user is logged in."""
    return 'user_id' in session

def get_user_id():
    """Get the logged-in user's ID."""
    return session.get('user_id')

def get_user_role():
    """Get the logged-in user's role."""
    return session.get('user_role')

def set_user_role(role):
    """Set the logged-in user's role."""
    session['user_role'] = role

def clear_user_session():
    """Clear user session data."""
    session.pop('user_id', None)
    session.pop('user_role', None)

def get_user_cart():
    """Get or create cart for current user."""
    user_id = get_user_id()
    if not user_id:
        return None
    
    # Create a new cart if not in session
    if 'cart' not in session:
        session['cart'] = Cart(user_id=user_id)
    
    return session['cart']

###################
# Main Routes
###################

@main_bp.route('/')
def index():
    """Homepage route."""
    # Get featured products and restaurants
    # featured_products = Product.get_all()[:4]  # Get first 4 products
    featured_products = get_all_products()[:4]  # Get first 4 products
    # featured_restaurants = Restaurant.get_all()[:3]  # Get first 3 restaurants
    featured_restaurants = get_all_restaurants()[:3]  # Get first 3 restaurants
    
    return render_template('landing_page.html', 
                          products=featured_products,
                          restaurants=featured_restaurants)

###################
# User Routes
###################

@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    """View and edit user profile on the same page."""
    # if not is_logged_in():
    #     flash('Please log in to view your profile')
    #     return redirect(url_for('auth.login'))
        
    user_id = get_user_id()
    user = User.get_by_id(user_id)
    
    if not user:
        flash('User not found')
        return redirect(url_for('auth.login'))
    
    # Get user's recent orders and addresses
    orders = Order.get_by_user(user_id)
    addresses = UserAddress.get_by_user(user_id)
    
    form = UserForm()
    
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        # Other fields as needed
        user.save()
        
        flash('Profile updated successfully!')
        return redirect(url_for('user.profile'))
    elif request.method == 'GET':
        # Populate form with user data
        form.name.data = user.name
        form.email.data = user.email
    
    return render_template('profile.html', 
                          user=user,
                          orders=orders, 
                          addresses=addresses,
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
        
        user = User.get_by_email(username)
        if user and user.password == password:  
            session['user_id'] = user.id
            session['user_role'] = user.role.value 
            flash('Login successful!')
            return redirect(url_for('user.profile'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    """User logout route."""
    clear_user_session()
    flash('You have been logged out')
    return redirect(url_for('main.index'))

###################
# Cart Routes
###################

@cart_bp.route('/')
def view_cart():
    """View cart contents."""
    if not is_logged_in():
        flash('Please log in to view your cart')
        return redirect(url_for('auth.login'))
        
    cart = get_user_cart()
    if not cart:
        flash('Unable to retrieve your cart')
        return redirect(url_for('main.index'))
    
    return render_template('cart.html', 
                          cart=cart,
                          total=cart.total_cost())

@cart_bp.route('/add/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add item to cart."""
    if not is_logged_in():
        flash('Please log in to add items to your cart')
        return redirect(url_for('auth.login'))
        
    product = Product.get_by_id(product_id)
    if not product:
        flash('Product not found')
        return redirect(url_for('product.list_products'))
        
    quantity = int(request.form.get('quantity', 1))
    
    cart = get_user_cart()
    
    # Create a new CartItem
    cart_item = CartItem(
        id=f"temp_{product_id}",  # Will be replaced when saved
        product_id=product_id,
        product=product,
        quantity=quantity
    )
    
    # Add to cart
    cart.add_item(cart_item)
    
    # Save to session
    session['cart'] = cart
    
    flash('Item added to cart')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/remove/<product_id>')
def remove_from_cart(product_id):
    """Remove item from cart."""
    if not is_logged_in():
        flash('Please log in to modify your cart')
        return redirect(url_for('auth.login'))
        
    cart = get_user_cart()
    cart.remove_item(product_id)
    
    # Save to session
    session['cart'] = cart
    
    flash('Item removed from cart')
    return redirect(url_for('cart.view_cart'))

###################
# Product Routes
###################

@product_bp.route('/')
def list_products():
    """Display all products."""
    products = Product.get_all()
    return render_template('products/list.html', products=products)

@product_bp.route('/category/<category>')
def list_by_category(category):
    """Display products by category."""
    try:
        # Convert string to enum
        category_enum = ProductCategory[category.upper()]
        products = Product.get_by_category(category_enum)
        return render_template('products/category.html', 
                              products=products, 
                              category=category_enum)
    except KeyError:
        flash(f'Category {category} not found')
        return redirect(url_for('product.list_products'))

@product_bp.route('/<product_id>')
def product_detail(product_id):
    """Display product details."""
    product = Product.get_by_id(product_id)
    if not product:
        flash('Product not found')
        return redirect(url_for('product.list_products'))
        
    return render_template('products/detail.html', product=product)

###################
# Restaurant Routes
###################

@restaurant_bp.route('/')
def list_restaurants():
    """Display all restaurants."""
    restaurants = Restaurant.get_all()
    return render_template('restaurants/list.html', restaurants=restaurants)

@restaurant_bp.route('/<restaurant_id>')
def restaurant_detail(restaurant_id):
    """Display restaurant details and menu."""
    restaurant = Restaurant.get_by_id(restaurant_id)
    if not restaurant:
        flash('Restaurant not found')
        return redirect(url_for('restaurant.list_restaurants'))
        
    # Get restaurant's menu items
    menu_items = restaurant.get_menu_items()
    
    return render_template('restaurants/detail.html', 
                          restaurant=restaurant,
                          menu_items=menu_items)

###################
# Driver Routes
###################

@driver_bp.route('/')
def list_drivers():
    """Display all drivers."""
    drivers = Driver.get_all()
    return render_template('drivers/list.html', drivers=drivers)

###################
# Order Routes
###################

@order_bp.route('/')
def list_orders():
    """Display user's orders."""
    if not is_logged_in():
        flash('Please log in to view your orders')
        return redirect(url_for('auth.login'))
        
    user_id = get_user_id()
    orders = Order.get_by_user(user_id)
    
    return render_template('orders/list.html', orders=orders)

@order_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout process."""
    if not is_logged_in():
        flash('Please log in to checkout')
        return redirect(url_for('auth.login'))
        
    user_id = get_user_id()
    cart = get_user_cart()
    
    if not cart or not cart.items:
        flash('Your cart is empty')
        return redirect(url_for('product.list_products'))
    
    form = OrderForm()
    
    # Get user addresses for dropdown
    addresses = UserAddress.get_by_user(user_id)
    form.address.choices = [(a.id, a.full_address()) for a in addresses]
    
    if form.validate_on_submit():
        # Create the order
        address_id = form.address.data
        payment_method = form.payment_method.data
        
        # Create order from cart
        order = Order.create_from_cart(user_id, cart, address_id, payment_method)
        
        # Clear cart
        cart.clear()
        session['cart'] = cart
        
        flash('Order placed successfully!')
        return redirect(url_for('order.order_detail', order_id=order.id))
    
    return render_template('orders/checkout.html', 
                          form=form,
                          cart=cart,
                          total=cart.total_cost())

@order_bp.route('/<order_id>')
def order_detail(order_id):
    """Display order details."""
    if not is_logged_in():
        flash('Please log in to view order details')
        return redirect(url_for('auth.login'))
        
    user_id = get_user_id()
    order = Order.get_by_id(order_id)
    
    # Verify this is the user's order
    if not order or order.user_id != user_id:
        flash('Order not found')
        return redirect(url_for('order.list_orders'))
    
    # Get order items
    items = order.items
    
    return render_template('orders/detail.html', 
                          order=order,
                          items=items)

###################
# Search Routes
###################

@main_bp.route('/search')
def search():
    """Search for products and restaurants."""
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('main.index'))
    
    # Search across all entities
    results = Search.search_all(query)
    
    return render_template('search_results.html', 
                          query=query,
                          results=results)