from project.db import *
from project.models.cart_model import Cart, CartItem
#from project.models import UserInfo, Order, OrderStatus

from flask import session

def get_user():
    user_dict = session.get('user')
    if user_dict:
        return User(
            id=str(user_dict['user_id']),
            name=user_dict['firstname'],
            email=user_dict['email'],
            phone=user_dict['phone']
        )
    return None

def get_cart():
    cart_data = session.get('shopping_cart')
    cart = Cart()
    if isinstance(cart_data, dict):
        for item in cart_data.get('items', []):
            if not item:
                return cart
            else:
                product = get_product_by_id(item['product']['id'])
                if product:
                    cart.add_item(CartItem(
                        id=str(item['id']),
                        product = product,
                        quantity=item['quantity']
                    ))
    return cart

def _save_basket_to_session(basket):
    session['shopping_cart'] = {
        'items': [
            {
                'id': item.id,
                'quantity': item.quantity,
                'product': {
                    'id': item.product.id
                }
            } for item in basket.items
        ]
    }

def add_to_cart(product_id, quantity=1):
    cart = get_cart()
    cart.add_item(CartItem(product=get_product_by_id(product_id), quantity=int(quantity)))
    _save_basket_to_session(cart)

def add_cart_item_from_db(cart_item):
    cart = get_cart()
    cart.add_item(cart_item)
    _save_basket_to_session(cart)


def remove_from_cart(item_id):
    cart = get_cart()
    print("removing from session")
    cart.remove_item(item_id)
    user_dict = session.get('user')
    if user_dict:
        user_id = session['user']['user_id']
    _save_basket_to_session(cart)

def empty_basket():
    session['shopping_cart'] = {
        'items': []
    }
    #call db to delete items

def convert_basket_to_order(cart):
    return Order(
        id=None,
        status=OrderStatus.PENDING,
        user_id=get_user().id,
        total=cart.total_cost(),
        items=cart.items
    )
