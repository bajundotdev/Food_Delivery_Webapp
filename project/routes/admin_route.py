from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from project.forms import ProductForm
from project.decorators import login_required, admin_required, driver_required
from project.models import Product, Order
from flask_mysqldb import MySQL

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

mysql = MySQL()

@admin_bp.route('/')
@login_required
@admin_required
def manage_admins():
    return render_template('admin/manage_admins.html')

@admin_bp.route('/dashboard')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/products', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.get_by_id(product_id)
    
    if not product:
        flash('Product not found.', 'danger')
        return redirect(url_for('admin.products'))
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        product.description = request.form['description']
        
        if product.save():
            flash('Product updated successfully.', 'success')
            return redirect(url_for('admin.products'))
        else:
            flash('Failed to update product.', 'danger')
    
    return render_template('admin/edit_product.html', product=product)

@admin_bp.route('/categories', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_categories():
    form = ProductForm()
    if form.validate_on_submit():
        try:
            with mysql.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO categories (name) VALUES (%s)",
                    (form.name.data,)
                )
                mysql.connection.commit()
            flash('Category added successfully.', 'success')
            return redirect(url_for('admin.manage_categories'))
        except Exception as e:
            flash(f'Error adding category: {e}', 'danger')

    with mysql.connection.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()

    return render_template('admin/categories.html', form=form, categories=categories)

@admin_bp.route('/orders')
@login_required
@admin_required
def manage_orders():
    status_filter = request.args.get('status', '')
    
    if status_filter:
        orders = Order.get_orders_by_status(status_filter)
    else:
        # orders = Order.get_all()
        orders = []
    return render_template('admin/manage_orders.html', orders=orders)

@admin_bp.route('/order/<string:order_id>')
@login_required
@admin_required
def view_order(order_id):
    return render_template('admin/manage_orders.html', orders=order_id)

@admin_bp.route('/orders/report')
@login_required
@admin_required
def manage_order_report():
    status_filter = request.args.get('status', '')
    
    if status_filter:
        orders = Order.get_orders_by_status(status_filter)
    else:
        # orders = Order.get_all()
        orders = []
    return render_template('admin/manage_order_report.html', orders=orders)

@admin_bp.route('/menu')
@login_required
@admin_required
def manage_product():
    status_filter = request.args.get('status', '')
    
    if status_filter:
        orders = Order.get_orders_by_status(status_filter)
    else:
        # orders = Order.get_all()
        orders = []
    return render_template('admin/manage_products_and_category.html', orders=orders)

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    status_filter = request.args.get('status', '')
    
    if status_filter:
        orders = Order.get_orders_by_status(status_filter)
    else:
        # orders = Order.get_all()
        orders = []
    return render_template('admin/manage_customers.html', orders=orders)

@admin_bp.route('/restaurant')
@login_required
@admin_required
def manage_restaurant():
    status_filter = request.args.get('status', '')
    
    if status_filter:
        orders = Order.get_orders_by_status(status_filter)
    else:
        # orders = Order.get_all()
        orders = []
    return render_template('admin/manage_restaurant.html', orders=orders)

@admin_bp.route('/drivers')
@login_required
@admin_required
def manage_drivers():
    status_filter = request.args.get('status', '')
    
    if status_filter:
        orders = Order.get_orders_by_status(status_filter)
    else:
        # orders = Order.get_all()
        orders = []
    return render_template('admin/manage_drivers.html', orders=orders)