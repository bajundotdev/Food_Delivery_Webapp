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

@admin_bp.route('/products')
@login_required
@admin_required
def products():
    """Admin view to manage all products."""
    cursor = MySQL.connection.cursor(dictionary=True)

    # Get all products
    cursor.execute("SELECT * FROM products")
    product_items = cursor.fetchall()
    cursor.close()

    return render_template('admin/products.html', product_items=product_items)


@admin_bp.route('/orders/assign/<int:order_id>', methods=['GET'])
@login_required
@admin_required
def assign_driver_form(order_id):
    cursor = MySQL.connection.cursor(dictionary=True)

    # Get the order details
    cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    order = cursor.fetchone()

    if not order:
        flash('Order not found.', 'danger')
        return redirect(url_for('admin.dashboard'))

    # Get list of all available drivers
    cursor.execute

@admin_bp.route('/orders/assign/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def assign_driver(order_id):
    driver_id = request.form.get('driver_id')

    if not driver_id:
        flash('Please select a driver.', 'warning')
        return redirect(url_for('admin.assign_driver_form', order_id=order_id))

    cursor = MySQL.connection.cursor()
    cursor.execute("UPDATE orders SET driver_id = %s WHERE id = %s", (driver_id, order_id))
    MySQL.connection.commit()
    cursor.close()

    flash('Driver assigned successfully.', 'success')
    return redirect(url_for('admin.view_order', order_id=order_id))  # Adjust route name if needed
