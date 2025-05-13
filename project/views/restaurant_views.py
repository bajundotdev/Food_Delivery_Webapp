from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RestaurantForm
from models import Restaurant
from flask_mysqldb import MySQL

restaurant_bp = Blueprint('restaurant', __name__, url_prefix='/restaurants')
@restaurant_bp.route('/register', methods=['GET', 'POST'])
def register_restaurant():
    form = RestaurantForm()

    if form.validate_on_submit():
        # Get the form data
        name = form.name.data
        address = form.address.data
        phone = form.phone.data
        email = form.email.data
        website = form.website.data
        description = form.description.data

        # Automatically set role as 'restaurant_manager'
        role = 'restaurant_manager'

        # Insert the restaurant into the database, including the role
        cursor = MySQL.connection.cursor()
        cursor.execute("""
            INSERT INTO users (name, address, phone, email, website, description, role)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, address, phone, email, website, description, role))
        MySQL.connection.commit()
        cursor.close()

        print('Restaurant registration successful!', 'success')
        return redirect(url_for('main.index'))  # Redirect to the main page after successful registration

    return render_template('register.html', form=form)

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
        print('Restaurant not found')
        return redirect(url_for('restaurant.list_restaurants'))
        
    # Get restaurant's menu items
    menu_items = restaurant.get_menu_items()
    
    return render_template('restaurants/detail.html', 
                          restaurant=restaurant,
                          menu_items=menu_items)


