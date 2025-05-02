from flask import Blueprint, render_template

# Shopping Cart Management
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/', methods=['GET'])
def view_cart():
    return render_template ('/view_cart.html')