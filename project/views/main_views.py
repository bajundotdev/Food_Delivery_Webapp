from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import User, cart_order_product
from forms import AddToCartForm
from utils import get_user_cart, save_cart, is_logged_in, get_user_id

# Create the blueprint
main_bp = Blueprint('main', __name__)

# Route to the homepage
@main_bp.route('/')
def index():
    """Homepage route."""
    # Get featured products
    featured_products = Product.get_all()[:4]  # Get the first 4 products
    featured_restaurants = Restaurant.get_all()[:3]  # Get the first 3 restaurants
    
    return render_template('index.html', 
                          products=featured_products,
                          restaurants=featured_restaurants)

# Route to add product to the cart
@main_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add a product to the cart."""
    form = AddToCartForm()

    if form.validate_on_submit():
        if not is_logged_in():
            flash("You need to be logged in to add items to your cart", "warning")
            return redirect(url_for('auth.login'))  # Redirect to login if not logged in

        # Fetch the product by ID
        product = Product.query.get(product_id)
        if not product:
            flash("Product not found", "danger")
            return redirect(url_for('main.index'))  # Redirect to homepage if product not found

        # Get the current user's cart
        cart = get_user_cart(get_user_id())

        # Check if the product is already in the cart
        cart_item = next((item for item in cart['items'] if item['product_id'] == product_id), None)

        if cart_item:
            # Update the quantity of the existing product in the cart
            cart_item['quantity'] += form.quantity.data
        else:
            # If product is not in the cart, add it with the specified quantity
            cart['items'].append({
                'product_id': product_id,
                'quantity': form.quantity.data
            })

        # Save the updated cart to the session
        save_cart(cart)

        # Flash success message
        flash(f"Added {product.name} (x{form.quantity.data}) to your cart!", "success")
        return redirect(url_for('main.index'))  # Redirect back to homepage

    return render_template('add_to_cart.html', form=form)

# Route to view the user's cart
@main_bp.route('/cart')
def view_cart():
    """View the current user's cart."""
    cart = get_user_cart(get_user_id())
    if not cart or len(cart['items']) == 0:
        flash("Your cart is empty.", "info")
        return redirect(url_for('main.index'))  # Redirect to homepage if cart is empty

    # Render the existing cart view template, passing the cart to it
    return render_template('cart.html', cart=cart)

# Route to remove an item from the cart
@main_bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    """Remove a product from the cart."""
    cart = get_user_cart(get_user_id())

    # Remove the item by product_id
    cart['items'] = [item for item in cart['items'] if item['product_id'] != product_id]
    
    # Save the updated cart
    save_cart(cart)
    
    flash("Item removed from your cart.", "success")
    return redirect(url_for('main.view_cart'))  # Redirect to view the updated cart

# Route to clear the cart
@main_bp.route('/clear_cart', methods=['POST'])
def clear_cart():
    """Clear all items in the cart."""
    cart = get_user_cart(get_user_id())
    
    # Empty the cart items
    cart['items'] = []
    
    # Save the empty cart
    save_cart(cart)
    
    flash("Your cart has been cleared.", "info")
    return redirect(url_for('main.index'))  # Redirect to homepage
