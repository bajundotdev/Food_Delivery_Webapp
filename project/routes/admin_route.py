import os
from flask import Blueprint, current_app, render_template, redirect, session, url_for, flash, request
from project.decorators import login_required, admin_required
from project.forms import ProductForm, DriverForm
from project.models import Product, Order
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

from project.db import *
from project.routes.user_route import allowed_file

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

mysql = MySQL()

#############################
#   Manage Dashboard        #
#############################

@admin_bp.route('/')
@login_required
@admin_required
def admin_dashboard():
    user_session = session['user']
    user_id = user_session['user_id']
    user_email = user_session['email']
    user_details = get_user_info_with_address_by_user_id(user_id)
    admin_details = get_user_info_with_address_by_user_id(user_id)


    all_users = get_all_users()
    all_orders = get_all_orders()
    all_products = get_all_products()
    drivers = get_all_driver()

    orders_by_status = get_all_orders_by_status('Pending')

    for order in orders_by_status:
        order.items = get_all_order_items_by_order_id_status(order.id, 'Pending')

    search_order = request.args.get('search_order')
    order_status = request.args.get('order_status')
    search_driver = request.args.get('search_driver')
    driver_status = request.args.get('driver_status')
    clear = request.args.get('clear')

    if request.method == "GET":
        if search_order or order_status:
            all_orders = search_order_name_id_status(search_order, order_status)

        if search_driver or driver_status:
            all_orders = search_order_name_id_status(search_driver, driver_status)

        if clear:
            return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/dashboard.html', user_details=user_details,
                                                admin_details=admin_details,
                                                all_users=all_users,
                                                all_orders=all_orders, 
                                                all_products=all_products, 
                                                orders_by_status=orders_by_status)
                                                #,drivers=drivers)

@admin_bp.route('/profile', methods=['GET'])
@login_required
@admin_required 
def profile():
    user_session = session.get('user')
    user_details = get_user_info_with_address_by_email(user_session['email'])

    if user_details:
        user_info = user_details[0]
        address = user_details[1]
        photo = user_details[0].profile_picture_url
        session['photo'] = photo
    else:
        user_info = ""
        address = ""
        photo = ""
    
    user_id = session.get('user').get('user_id')
    my_orders = get_all_orders_by_user_id(user_id)

    return render_template('admin/profile.html', user_details=user_details, 
                           user_info=user_info, 
                           my_orders=my_orders,
                           address = address, 
                           photo = photo)

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

@admin_bp.route('/categories/update_category/<int:category_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_category(category_id):
    category = get_all_category_by_categ_id(category_id)
    

    return render_template('admin/menu/category_update_form.html', category=category)


@admin_bp.route('/menu/save_category/', methods=('POST', 'GET'))
@login_required
@admin_required
def save_category():
   
    if request.method == "POST":
        try:
            #update_category(category_id, category_name)
            flash('Category successfully updated!', 'success')

        except Exception as e:
            print("Error:", e)
            flash('Failed to update category.', 'danger')

    return redirect(url_for('admin.manage_product'))

@admin_bp.route('/menu/delete_category/<int:category_id>', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    if request.method == "POST":
            pass
            #delete_category(product_id)
     

    return redirect(url_for('admin.manage_product'))
###########################
#   Manage CRUD Orders    #
###########################

# View All Orders
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

# View Order by Order_ID
@admin_bp.route('/order/<string:order_id>', methods=['GET'])
@login_required
@admin_required
def view_order(order_id):
    order_details = get_all_orders_by_id(order_id)
    items_in_order = get_all_order_items_by_order_id(order_id)

    return render_template('admin/orders/view_order.html', order_details=order_details,
                                                        items_in_order=items_in_order)
    # return redirect(url_for('admin.manage_orders'))

# Update Status of Order by ORDER_ID
@admin_bp.route('/orders/update_order', methods=['POST'])
@login_required
@admin_required
def update_order_status():
    order_id = request.form.get('order_id')
    status = request.form.get('order_status')
    result = set_order_status(order_id, status)

    return redirect(url_for('admin.manage_orders'))
    # return redirect(url_for('admin.manage_orders'))


# View All Orders
@admin_bp.route('/orders/report')
@login_required
@admin_required
def manage_order_report():
    all_orders = get_all_orders()
    search_order = request.args.get('search_order')
    order_status = request.args.get('order_status')
    clear = request.args.get('clear')

    if request.method == "GET":
        if search_order or order_status:
            all_orders = search_order_name_id_status(search_order, order_status)
        if clear:
            return redirect(url_for('admin.manage_order_report'))


    return render_template('admin/orders/manage_order_report.html', all_orders=all_orders)


###########################
#   Manage CRUD Products  #
###########################

@admin_bp.route('/menu')
@login_required
@admin_required
def manage_product():
    categories = get_all_category()
    menus = get_all_products()
    search_menu = request.args.get('search_menu', '')
    menu_status = request.args.get('menu_status', '')
    clear = request.args.get('clear', '')

    if request.method == "GET":
        if search_menu or menu_status:
            menus = search_product(search_menu)
            
        if clear:
            return redirect(url_for('admin.manage_product'))

    return render_template('admin/menu/manage_products_and_category.html', categories=categories,menus=menus)

@admin_bp.route('/menu/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    form_product = ProductForm()
    categories = get_all_category()

    if request.method == "POST":
        file = request.files['food_image_url']
    
        try:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER']+'/products', filename))
                add_product_to_db(form_product)

            flash('Menu successfully added!', 'success')
            return redirect(url_for('admin.manage_product'))

        except Exception as e:
            print("Error:", e)
            flash('Failed to add new menu.', 'danger')
    
    return render_template('admin/menu/product_add_form.html', form_product=form_product, categories=categories)

@admin_bp.route('/menu/<int:product_id>', methods=['GET'])
@login_required
@admin_required
def view_product(product_id):
    product_details = get_product_by_id(product_id)
    return render_template('admin/menu/product_details.html', product_details=product_details)

# Update Product/ Menu
@admin_bp.route('/menu/update/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_product(product_id):
    form_product = ProductForm()
    form_product = get_product_by_id(product_id)
    categories = get_all_category()
    if not form_product:
        flash('Product not found.', 'danger')
        return redirect(url_for('admin.manage_product'))
    
    if request.method == "GET":
        return render_template('admin/menu/product_update_form.html', form_product=form_product, categories=categories)
    
    if request.method == 'POST':
        form_product.name = request.form['name']
        form_product.price = float(request.form['price'])
        form_product.stock = int(request.form['stock'])
        form_product.description = request.form['description']
        file = request.files.get('food_image_url')
        
        print("File: ", file)

        try:
            result = update_product_table(form_product)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER']+'/products', filename))

            flash('Product updated successfully.', 'success')
            return redirect(url_for('admin.manage_product'))
        except:
            flash('Failed to update product.', 'danger')
            
    return redirect(url_for('admin.manage_product'))

@admin_bp.route('/menu/save/', methods=('POST', 'GET'))
@login_required
@admin_required
def save_product():
    update_form = ProductForm()

    if request.method == "POST":
        file = request.files['food_image_url']
        try:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER']+'/products', filename))

            update_form.food_image_url
            update_product_table(update_form)
            flash('Menu successfully updated!', 'success')

        except Exception as e:
            print("Error:", e)
            flash('Failed to update menu.', 'danger')

    return redirect(url_for('admin.manage_product'))

@admin_bp.route('/menu/delete/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    if request.method == "POST":
        try:
            result = delete_product_from_list(product_id)
            flash('Product successfully removed!', 'success')
        except:
            flash('Failed to remove product.', 'danger')

    return redirect(url_for('admin.manage_product'))

#########################
#   Manage CRUD Users   #
#########################
 
@admin_bp.route('/users/')
@login_required
@admin_required
def manage_users():
    customers = get_all_users_by_status(1)    

    return render_template('admin/users/manage_customers.html', customers=customers)

@admin_bp.post('/user/<int:user_id>/')
def delete_user(user_id):
    
    print(user_id)
    set_user_is_active(user_id,0)

    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/admins')
@login_required
@admin_required
def manage_admins():
    return render_template('admin/admins/manage_admins.html')

@admin_bp.route('/drivers')
@login_required
@admin_required
def manage_drivers():
    drivers = get_all_driver()
    return render_template('admin/drivers/manage_drivers.html', drivers=drivers)

@admin_bp.route('/drivers/<int:driver_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_driver(driver_id):
    driver_form = DriverForm()
    driver_query = get_driver_by_id(driver_id)
    driver_details = driver_query[0]

    # for driver in driver_query:
    #     print(driver)
    #     #user_address = get_address_by_user_id(driver.user_id)
    #     #driver_details.append(user_address)
    #     print(driver_details)
    #     pass

    return render_template('admin/drivers/update_driver.html', driver_form=driver_form,
                                                        driver_details=driver_details)

##############################
#   Manage CRUD Restaurants  #
##############################

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