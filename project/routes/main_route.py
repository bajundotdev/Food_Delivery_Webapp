from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# Import dummy database db.py
from project.db import get_all_driver, get_all_products, get_all_restaurants, check_user, add_user

# Create blueprints for different sections of the application
main_bp = Blueprint('main', __name__)

###################
# Main Routes
###################

@main_bp.route('/',methods=('POST', 'GET'))
def index():
    """Homepage route."""
    cart_data = session.get('shopping_cart')
    print(cart_data)
    # Get featured products and restaurants
    featured_products = get_all_products()[:4]  # Get first 4 products
    featured_restaurants = get_all_restaurants()[:3]  # Get first 3 restaurants

    return render_template('index.html',
                          products=featured_products,
                          restaurants=featured_restaurants)

@main_bp.post('/cart/<int:product_id>/')
def adding_to_cart(product_id):
    adding_to_cart(product_id)
    return redirect(url_for('main.index'))

@main_bp.route('/about')
def about():
    return render_template('about.html')  # Assuming you have an about.html template

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')  # Assuming you have a contact.html template