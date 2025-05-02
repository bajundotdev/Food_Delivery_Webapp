from flask import Blueprint, render_template

# Blueprint(plural)
orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/orders')
def index():
    return render_template ('auth/login.html')