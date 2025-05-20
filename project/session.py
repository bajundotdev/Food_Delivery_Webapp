from project.db import get_product_by_id
from project.models.cart_model import Cart, CartItem
#from project.models import UserInfo, Order, OrderStatus

from flask import session

# def get_user():
#     user_dict = session.get('user')
#     if user_dict:
#         return UserInfo(
#             id=str(user_dict['user_id']),
#             firstname=user_dict['firstname'],
#             surname=user_dict['surname'],
#             email=user_dict['email'],
#             phone=user_dict['phone']
#         )
#     return None

def get_cart():
    cart_data = session.get('shopping_cart')
    cart = Cart()
    print(cart_data)
    if isinstance(cart_data, dict):
        for item in cart_data.get('items'):
            product = get_product_by_id(item['id'])
            if product:
                cart.add_item(CartItem(
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
                'prodcuct': item.product
            } for item in basket.items
        ]
    }

def add_to_cart(product_id, quantity=1):
    cart = get_cart()
    cart.add_item(CartItem(product=get_product_by_id(product_id), quantity=quantity))
    _save_basket_to_session(cart)

def remove_from_cart(product_id):
    cart = get_cart()
    cart.remove_item(product_id)
    _save_basket_to_session(cart)

def empty_basket():
    session['shopping_cart'] = {
        'items': []
    }

# def convert_basket_to_order(basket):
#     return Order(
#         id=None,
#         status=OrderStatus.PENDING,
#         user=get_user(),
#         total_cost=basket.total_cost(),
#         items=basket.items
#     )
