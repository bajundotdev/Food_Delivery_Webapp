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
# ENUMS
################## 
class ProductCategory(Enum):
    MAIN_COURSE = "Main Course"


def check_user(email, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_table WHERE email = \"%s\";" % email)
    row = cur.fetchone()
    cur.close()
    if row:
        if check_password_hash(row[4], password):
            if row[6] == "admin":
                role = UserRole.ADMIN
            elif row[6] == "user":
                role = UserRole.CUSTOMER
            elif row[6] == "driver":
                role = UserRole.DRIVER
            elif row[6] == "ownder":
                role = UserRole.RESTAURANTOWNER
            return User(row[0], row[1], row[2], row[3], row[4], row[5], role)
                           
    return None

def add_user(form):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO users (email, password_hash, fullname, phone_number, user_type, is_active, is_verified, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %d, %d, %s,%s)"""
        , (form.email.data, form.password_hash.data, form.fullname.data, form.phone_number.data, form.user_type.data, 1, 1, curent_timestamp, curent_timestamp))
    mysql.connection.commit()
    cur.close()

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