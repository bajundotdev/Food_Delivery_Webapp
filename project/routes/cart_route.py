from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from project.decorators import login_required, admin_required, driver_required

from project.db import *
from project.models import Cart, CartItem, Product
from project.forms.shopping_form import CheckoutForm

# Create blueprints for different sections of the application
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')
from project.session import *

###################
# Cart Routes     #
###################
@cart_bp.route('/')
def view_cart():
    product_id = request.form.get('product_id')
    order = get_cart()

    if product_id:
        add_to_cart(product_id)

    return render_template('user/user_cart.html', order=order, totalprice=order.total_cost())

@cart_bp.route('/cart/update/<cart_id>', methods=['POST'])
def update_quantity(cart_id):
    
    action = request.form.get('action')
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('cart_quantity', 0))
    if action == 'plus':
        increment_cart_item(cart_id)
    elif action == 'minus':
        minus_cart_item(cart_id)

    return redirect(url_for('cart.view_cart'))

    
@cart_bp.post('/removebasketitem/<string:cart_id>/')
def removing_from_cart(cart_id):
    cart = get_cart()
    item = cart.get_item(cart_id)
    
    if item:
        remove_from_cart(item.id)
    else:
        flash("Item not found in basket.", "warning")

    return redirect(url_for('cart.view_cart'))

# Dummy data for cart items
dummy_cart_items = []

@cart_bp.post('/clearbasket/')
def clear_basket():
    empty_basket()
    if session.get('user'):
        clear_cart_db(get_user().id)
    flash('Basket cleared.', 'primary')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/checkout/', methods=('POST','GET'))
@login_required
def checkout_cart():
    cart = get_cart()
    user_session = session.get('user')
    user_details = get_user_info_with_address_by_email(user_session['email'])

    if user_details:
        user_info = user_details[0]
        address = user_details[1]
    else:
        user_info = ""
        address = ""

    if 'user' not in session or session['user']['user_id'] == 0:
        flash('Please log in before checking out.', 'error')
        return redirect(url_for('main.login'))

    form = CheckoutForm()
    
    if request.method == 'POST':
        shippingFee = 0
        packagingFee = 0

        if form.shippingMethod.data == "express":
            shippingFee = 5.99
        if form.packagingMethod.data == "standard":
            packagingFee = 2.99
        elif form.packagingMethod.data == "discreet_confidential":
            packagingFee = 5.99
        
        total = round(float(cart.total_cost()) + float(shippingFee) + float(packagingFee),2)

        if form.validate_on_submit():
            user_id = session['user']['user_id']
            clear_cart_db(user_id)
            cart_items = session.get('shopping_cart')
            for item in cart_items.get('items', []):
                product_id = item['product']['id']
                quantity = item['quantity']
                item_id = item['id']
                add_cart_item_to_db(product_id ,user_id, quantity, item_id)

            order = convert_basket_to_order(cart)
            order.total = total
            address_id = get_address_id_by_user_id(int(order.user_id))
            order_id = add_order_to_db(order, form, address_id, shippingFee, packagingFee)
            session['order'] = {
                'order_id' : order_id,
                'shippingFee': shippingFee,
                'packagingFee': packagingFee,
                'total': total
            }
            empty_basket()
            return render_template('user/receipt.html', form=form, cart=cart, total=total, packagingFee=packagingFee, shippingFee = shippingFee)
        else:
            flash('The provided information is missing or incorrect', 'error')
    
    return render_template('user/checkout.html', form=form, cart=cart, user_info=user_info, address = address)

@cart_bp.route('/receipt', methods=('POST','GET'))
@login_required
def receipt():
    cart = get_cart()
    user_session = session.get('user')
    #user_details= user_session['email']
    user_details = get_user_info_with_address_by_email(user_session['email'])
    if user_details:
        user_info = user_details[0]
        address = user_details[1]
    else:
        user_info = ""
        address = ""

    if 'user' not in session or session['user']['user_id'] == 0:
        flash('Please log in before checking out.', 'error')
        return redirect(url_for('main.login'))

    
    if request.method == 'POST':
        order = session.get('order')
        order_id = order['order_id']
        shippingFee = order['shippingFee']
        packagingFee = order['packagingFee']
        total = order['total']
        update_order_price_db(order_id, total)
        flash('Your order has been confirmed!', 'success')
        return redirect(url_for('user.profile'))
    
    return render_template('user/receipt.html')