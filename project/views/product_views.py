from flask import Blueprint, render_template, flash, redirect, url_for, request
from forms import AddToCartForm  
from models import Product  
from utils import is_logged_in  

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/<int:product_id>', methods=['GET'])
def view_product(product_id):
    product = Product.get_by_id(product_id)  # Get the product by its ID (implement this method)
    if not product:
        print('Product not found', 'danger')
        return redirect(url_for('main.index'))  # Redirect to home or products listing

    form = AddToCartForm()  # Create the form object inside the route
    return render_template('product_detail.html', product=product, form=form)
