from flask import Blueprint, render_template, redirect, session, url_for, flash, request
from project.decorators import login_required, admin_required
from project.forms.admin_form import ProductForm
from project.models import Product, Order
from flask_mysqldb import MySQL

from project.db import *

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

mysql = MySQL()

#############################
#   Manage Dashboard        #
#############################

@admin_bp.route('/')
@login_required
@admin_required
def admin_dashboard():
    user_id = session['user']['user_id']
    admin_details = get_user_info_with_address_by_user_id(user_id)
    all_users = get_all_users()
    all_orders = get_all_orders()
    all_products = get_all_products()
    orders_with_products = get_all_orders_and_products()[:10]
    orders_by_status = get_all_orders_by_status('Pending')[:10]
    drivers = get_all_driver()

    return render_template('admin/dashboard.html', admin_details=admin_details,
                                                all_users=all_users,
                                                all_orders=all_orders, 
                                                all_products=all_products, 
                                                orders_with_products=orders_with_products,
                                                orders_by_status=orders_by_status,
                                                drivers=drivers)

@admin_bp.route('/admins')
@login_required
@admin_required
def manage_admins():
    return render_template('admin/manage_admins.html')

#############################
#   Manage CRUD Categories  #
#############################

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

###########################
#   Manage CRUD Orders    #
###########################

@admin_bp.route('/orders')
@login_required
@admin_required
def manage_orders():
    status_filter = request.args.get('status', '')

    orders_with_products = get_all_orders_and_products()[:10]
    pending_orders = get_all_orders_by_status('Pending')
    in_progress_orders = get_all_orders_by_status('In Progress')
    ready_orders = get_all_orders_by_status('Ready')
    drivers = get_all_driver()
    
    if status_filter:
        orders = Order.get_orders_by_status(status_filter)
    else:
        # orders = Order.get_all()
        orders = []
    return render_template('admin/orders/manage_orders.html', orders_with_products=orders_with_products,
                                                pending_orders=pending_orders,
                                                in_progress_orders=in_progress_orders,
                                                ready_orders=ready_orders,
                                                drivers=drivers)

@admin_bp.route('/order/<string:order_id>')
@login_required
@admin_required
def view_order(order_id):
    all_orders = get_all_orders()

    return render_template('admin/orders/view_order.html', all_orders=all_orders)
    # return redirect(url_for('admin.manage_orders'))

@admin_bp.route('/orders/report')
@login_required
@admin_required
def manage_order_report():
    status_filter = request.args.get('status', '')
    all_orders = get_all_orders()
    
    if status_filter:
        orders = Order.get_orders_by_status(status_filter)
    else:
        # orders = Order.get_all()
        orders = []
    return render_template('admin/orders/manage_order_report.html', all_orders=all_orders)

###########################
#   Manage CRUD Products  #
###########################

@admin_bp.route('/menu')
@login_required
@admin_required
def manage_product():

    status_filter = request.args.get('status', '')
    
    if status_filter:
        menus = Product.get_orders_by_status(status_filter)
    else:
        menus = get_all_products()

    return render_template('admin/menu/manage_products_and_category.html', menus=menus)

@admin_bp.route('/menu/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    form_product = ProductForm()
    if request.method == 'POST':
        add_product_to_db(form_product)
        return redirect(url_for('admin.manage_product'))
    
    return render_template('admin/menu/product_add_form.html', form_product=form_product, categories=ProductCategory)

@admin_bp.route('/menu/update/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_product(product_id):
    form_product = ProductForm()
    form_product = get_product_by_id(product_id)

    if not form_product:
        flash('Product not found.', 'danger')
        return redirect(url_for('admin.manage_product'))
    
    if request.method == "GET":
        return render_template('admin/menu/product_update_form.html', form_product=form_product, categories=ProductCategory)
    
    if request.method == 'POST':
        form_product.name = request.form['name']
        form_product.price = float(request.form['price'])
        form_product.stock = int(request.form['stock'])
        form_product.description = request.form['description']
        
        if form_product.save():
            flash('Product updated successfully.', 'success')
            return redirect(url_for('admin.products'))
        else:
            flash('Failed to update product.', 'danger')
            
    return redirect(url_for('admin.manage_product'))

@admin_bp.route('/products', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.get_by_id(product_id)
    
    if not product:
        flash('Product not found.', 'danger')
        return redirect(url_for('admin.manage_product'))
    
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

@admin_bp.route('/menu/save/', methods=('POST', 'GET'))
@login_required
@admin_required
def save_product():
    update_form = ProductForm()
    #form_product = get_product_by_id(product_id)
    #update_product_table(form_product)
    if request.method == "POST":
        update_product_table(update_form)
        for info in update_form:
            print(info.data)
        flash('Product successfully updated!')
        return redirect(url_for('admin.manage_product'))
        # return render_template('admin/product_update_form.html', form_product=form_product, categories=ProductCategory)

    return redirect(url_for('admin.manage_product'))

@admin_bp.route('/menu/delete', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product_id = request.args.get('')
    delete_product_from_list(product_id)
    return redirect(url_for('admin.manage_product'))


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
    return render_template('admin/users/manage_customers.html', orders=orders)

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
    return render_template('admin/restaurants/manage_restaurant.html', orders=orders)

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
    return render_template('admin/drivers/manage_drivers.html', orders=orders)