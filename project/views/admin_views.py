from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from decorators import login_required, admin_required
from flask_mysqldb import MySQL

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@admin_required
def admin_dashboard():
    # Only authenticated admins can access this
    return render_template('admin/dashboard.html')

@admin_bp.route('/restaurants')
@login_required
@admin_required
def list_restaurants():
    """Display all restaurants for admin."""
    cursor = MySQL.connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE role = 'restaurant_manager'")
    restaurants = cursor.fetchall()
    cursor.close()
    
    return render_template('admin/restaurants.html', restaurants=restaurants)

@admin_bp.route('/restaurants/<int:restaurant_id>')
@login_required
@admin_required
def restaurant_detail(restaurant_id):
    """Display restaurant details and menu for admin."""
    # Get restaurant details
    cursor = MySQL.connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s AND role = 'restaurant_manager'", 
                  (restaurant_id,))
    restaurant = cursor.fetchone()
    
    if not restaurant:
        print('Restaurant not found', 'danger')
        return redirect(url_for('admin.list_restaurants'))
    
    # Get restaurant's menu items
    cursor.execute("SELECT * FROM products WHERE restaurant_id = %s", (restaurant_id,))
    product_items = cursor.fetchall()
    cursor.close()
    
    return render_template('admin/restaurant_detail.html', 
                          restaurant=restaurant,
                          product_items=product_items)