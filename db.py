# dummyDb.py
from project.models import Product, ProductCategory, Restaurant, User, UserRole
from datetime import datetime
from typing import List
from enum import Enum
from flask import Flask, render_template_string, request, session, redirect, url_for
from flask_mysqldb import MySQL
from MySQLdb import _mysql
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
mysql = MySQL(app)  # this is the instantiation

curent_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

##################
#    AUTH   
##################
def check_user(email, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_table WHERE email = \"%s\";" % email)
    row = cur.fetchone()
    cur.close()
    if row:
        if check_password_hash(row[4], password):
            return User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                           
    return None

##################
#    USER QUERIES   
##################

def get_user_by_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT user_id,fullname, email, phone_number,
                password_hash ,profile_picture_url,
                user_type, is_active, last_login
        FROM user_table
        WHERE user_id = %s
    """ % user_id)
    row = cur.fetchone()
    cur.close()
    return [
        User(str(row['user_id']), row['fullname'], row['phone_number'],
             row['password_hash'], row['profile_picture_url'],
             row['user_type'], bool(row['is_active']), row['last_login'])
    ]

def search_user_by_name(fullname):
    search_name = "%" + str(fullname) + "%"
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT user_id,fullname, email, phone_number,
                password_hash ,profile_picture_url,
                user_type, is_active, last_login
        FROM user_table
        WHERE fullname LIKE %s
    """ % search_name)
    row = cur.fetchone()
    cur.close()
    return [
        User(str(row['user_id']), row['fullname'], row['phone_number'],
             row['password_hash'], row['profile_picture_url'],
             row['user_type'], bool(row['is_active']), row['last_login'])
    ]

def add_user(form):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO users (email, password_hash, fullname, phone_number, user_type, is_active, is_verified, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %d, %d, %s,%s)"""
        , (form.email.data, form.password_hash.data, form.fullname.data, form.phone_number.data, form.user_type.data, 1, 1, curent_timestamp, curent_timestamp))
    mysql.connection.commit()
    cur.close()

#update
#delete

##################
#    ADDRESS QUERIES   
##################
def get_address_by_user_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT address_id,user_id, label,
                address_line1, address_line2 ,city,
                state, postal_code, country,
                created_at, updated_at
        FROM user_address
        WHERE user_id = %s
    """ % user_id)
    row = cur.fetchone()
    cur.close()
    return [
        User(str(row['address_id']), row['user_id'], row['label'],
             row['address_line1'], row['address_line2'], row['city'],
             row['state'], row['postal_code'], row['country'],
             row['created_at'], row['updated_at']
            )
    ]
   
def add_address_by_user_id(form):
    # cur = mysql.connection.cursor()
    # cur.execute("""
    #     INSERT INTO user_address (
    #                             )
    #     VALUES (%s, %s, %s, %s,
    #             %s, %s, %d, %d,
    #             curent_timestamp, curent_timestamp
    #             )
    # """, (form.username.data, form.password.data, form.email.data,
    #       form.firstname.data, form.surname.data, form.phone.data))
    # mysql.connection.commit()
    # cur.close()

#update
#delete

##################
#    PRODUCT QUERIES   
##################
def get_all_products():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT *
        FROM product_table
    """)
    results = cur.fetchall()
    cur.close()

    return [
        Product(str(row[0]), row[1], row[2],
             row[3], float(row[4]), float(row[5]), int(row[6]),
             row[7], row[8], str(row[11])) for row in results
    ]

def get_product_by_id(product_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT *
        FROM product_table
        WHERE product_id = %d
    """ % product_id)
    row = cur.fetchone()
    cur.close()
    return [
        Product(str(row[0]), row[1], row[2],
             row[3], float(row[4]), float(row[5]), int(row[6]),
             row[7], row[8], str(row[11]))
    ]

def search_product_by_name(search_str):
    str = "%" + str(search_str) + "%"
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT *
        FROM product_table
        WHERE product_id LIKE %s
    """ % str)
    results = cur.fetchall()
    cur.close()
    return [
        Product(str(row[0]), row[1], row[2],
             row[3], float(row[4]), float(row[5]), int(row[6]),
             row[7], row[8], str(row[11])) for row in results
    ]

def get_product_by_category(categ):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT *
        FROM product_table
        WHERE category = %s
    """ % categ)
    results = cur.fetchall()
    cur.close()

    return [
        Product(str(row[0]), row[1], row[2],
             row[3], float(row[4]), float(row[5]), int(row[6]),
             row[7], row[8], str(row[11])) for row in results
    ]

#add
#update
#delete
##################
#    RESTAURANT QUERIES   
##################
def get_all_restaurants():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT *
        FROM restaurant
    """)
    results = cur.fetchall()
    cur.close()
    return [
        Restaurant(str(row[0]), row[1], row[2],
             bool(row[3]), row[4], bool(row[5]), row[6],
             row[7], row[8], row[9], row[10]) for row in results
    ]

def get_restaurant_by_id(restaurant_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT *
        FROM restaurant
        WHERE restaurant_id = %s
    """)
    row = cur.fetchone()
    cur.close()
    return [
        Restaurant(str(row[0]), row[1], row[2],
             bool(row[3]), row[4], bool(row[5]), row[6],
             row[7], row[8], row[9], row[10])
    ]

def get_restaurant_by_name():
    pass

#add
#update
#delete

##################
#    DRIVER QUERIES   
##################
def get_driver_by_id(driver_id):
    pass

def get_all_drivers():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT *
        FROM delivery_driver, user_table
    """)
    results = cur.fetchall()
    cur.close()
    return [
        Restaurant(str(row[0]), row[1], row[2],
             bool(row[3]), row[4], bool(row[5]), row[6],
             row[7], row[8], row[9], row[10]) for row in results
    ]

def get_available_driver():
    pass

#add driver
#update driver
#delete driver

##################
#    PAYMENT QUERIES   
##################

##################
#    ORDER QUERIES   
##################

##################
#    CART QUERIES   
##################