from flask import render_template, request, redirect, url_for, Blueprint
from models import Order 
from forms import CreateOrderForm
from flask_mysqldb import MySQL  

order_bp = Blueprint('order', __name__, url_prefix='/orders')

@order_bp.route('/create/<int:user_id>', methods=['GET', 'POST'])
def create_order(user_id):
    form = CreateOrderForm()

    if request.method == 'POST' and form.validate_on_submit():
        product_name = form.product_name.data
        quantity = form.quantity.data

        try:
            cursor = MySQL.connection.cursor()
            order_id = Order.create_order(cursor, user_id, product_name, quantity)
            MySQL.connection.commit()
            cursor.close()

            print('Order successfully created!', 'success')
            return redirect(url_for('order.order_success'))
        except Exception as e:
            print(f'Error creating order: {str(e)}', 'danger')
            return redirect(url_for('order.create_order', user_id=user_id))

    return render_template('orders/create_order.html', form=form)

@order_bp.route('/success')
def order_success():
    return "Order has been successfully created!"
