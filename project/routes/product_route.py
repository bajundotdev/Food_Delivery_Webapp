from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from project.models import Product, ProductCategory, OrderStatus

# Import dummy database db.py
from project.db import *

# Create blueprints for different sections of the application
product_bp = Blueprint('product', __name__, url_prefix='/products') 

#####################
# Product Routes    #
#####################

@product_bp.route('/')
def product_list():
    """Display all products."""
    products = get_all_products()
    return render_template('products/product_list.html', products=products)

@product_bp.route('/category/<category>')
def list_by_category(category):
    """Display products by category."""
    try:
        # Convert string to enum
        category_enum = ProductCategory[category.upper()]
        products = Product.get_by_category(category_enum)
        return render_template('products/category.html', 
                              products=products, 
                              category=category_enum)
    except KeyError:
        flash(f'Category {category} not found')
        return redirect(url_for('product.list_products'))

@product_bp.route('/<int:product_id>')
def product_detail(product_id):
    """Display product details."""

    product = get_product_by_id(product_id)

    if not product:
        flash('Product not found')
        return redirect(url_for('product.product_list'))
        
    return render_template('products/product_detail.html', product=product)

@product_bp.route('/status')
def get_order_by_status():
    """Display order by status."""
    status_enum = 'Ready'
    order = get_order_ready(status_enum)
    return render_template('products/product_list.html', 
                              order=order, 
                              status=status_enum)
    # try:
    #     # Convert string to enum
    #     status_enum = "Ready"
    #     order = get_order_ready(status_enum)
    #     return render_template('products/product_list.html', 
    #                           order=order, 
    #                           status=status_enum)
    # except KeyError:
    #     flash(f'Status {status} not found')
    #     return redirect(url_for('product.list_products'))

