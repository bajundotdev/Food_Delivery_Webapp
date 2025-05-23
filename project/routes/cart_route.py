from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from project.decorators import login_required, admin_required, driver_required

# Import dummy database db.py
from project.db import *
from project.models import Cart, CartItem, Product
from project.forms.shopping_form import CheckoutForm



# Create blueprints for different sections of the application
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')
from project.session import *
##########################
# Session Management     #
##########################

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
# Cart Routes     #
###################
@cart_bp.post('/removebasketitem/<string:cart_id>/')
def removing_from_cart(cart_id):
    cart = get_cart()
    item = cart.get_item(cart_id)
    
    if item:
        #flash(f"Removed '{item.product.name}' from basket.")
        print("item: ", item)
        remove_from_cart(item.id)
        print("removing item")
    else:
        flash("Item not found in basket.", "warning")

    return redirect(url_for('cart.view_cart'))
# Dummy data for cart items
dummy_cart_items = []

@cart_bp.route('/')
def view_cart():
    product_id = request.form.get('product_id')
    order = get_cart()

    if product_id:
        print(f'user requested to add tour id = {product_id}')
        add_to_cart(product_id)

    return render_template('user/user_cart.html', order=order, totalprice=order.total_cost())
    # """View cart contents."""
    # if not is_logged_in():
    #     flash('Please log in to view your cart')
    #     return redirect(url_for('auth.login'))
        
    # cart = get_user_cart()
    # if not cart:
    #     flash('Unable to retrieve your cart')
    #     return redirect(url_for('main.index'))
    
    # return render_template('cart.html', 
    #                       cart=cart,
    #                       total=cart.total_cost())

@cart_bp.route('/add/<string:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add item to cart."""
    
    product_id = request.args.get(product_id)

    if not is_logged_in():
        if 'shopping_cart' not in session:
            session['shopping_cart'] = {}
            cart = session['shopping_cart']

        # Add or update product quantity
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {
                # 'id': product['id'],
                # 'name': product['name'],
                # 'price': product['price'],
                # 'quantity': 1
            }

        session['shopping_cart'] = cart  # Save back to session 
        
    else:
        product = Product.get_by_id(product_id)
        if not product:
            flash('Product not found', 'error')
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
    return redirect(url_for('main.index'))

@cart_bp.post('/clearbasket/')
def clear_basket():
    empty_basket()
    flash('Basket cleared.', 'primary')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/checkout', methods=('POST','GET'))
@login_required
def checkout_cart():
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

    form = CheckoutForm()
    if request.method == 'POST':
        
        if form.validate_on_submit():
            print(form.payment_method.data)
            order = convert_basket_to_order(cart)
            add_order(order)
            empty_basket()
            flash('Your order has been placed!', 'success')
            return redirect(url_for('user.profile'))
        else:
            print(form.validate_on_submit())
            flash('The provided information is missing or incorrect', 'error')
    
    return render_template('user/checkout.html', form=form, cart=cart, user_info=user_info, address = address)