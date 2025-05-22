# dummyDb.py
from project.models import Product, ProductCategory, Restaurant, User, Driver, UserRole
from project.models import *
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mysqldb import MySQL

curent_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

mysql = MySQL()

#####################
#    AUTH           #
#####################
def check_user(email, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_table WHERE email = \"%s\";" % email)
    row = cur.fetchone()
    cur.close()
    if row:
        if check_password_hash(row['password_hash'], password):
            return User(row['user_id'], row['fullname'], row['email'], row['phone_number'], row['password_hash'], row['profile_picture_url'], row['user_type'])
                           
    return None

#####################
#    USER QUERIES   #
#####################
def get_user_by_email(email):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT user_id,fullname, email, phone_number,
                password_hash ,profile_picture_url,
                user_type, is_active, last_login
        FROM user_table
        WHERE email = %s
    """, (email,))
    row = cur.fetchone()
    cur.close()
    if row is not None:
        return [
            User(str(row['user_id']), row['fullname'], row['email'],row['phone_number'],
                row['password_hash'], row['profile_picture_url'],
                row['user_type'], bool(row['is_active']), row['last_login'])
        ]
    else:
        return None

def get_user_by_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT user_id,fullname, email, phone_number,
                password_hash ,profile_picture_url,
                user_type, is_active, last_login
        FROM user_table
        WHERE user_id = %s
    """, (user_id,))
    row = cur.fetchone()
    cur.close()
    if row is not None:
        return [
            User(str(row['user_id']), row['fullname'], row['email'],row['phone_number'],
                row['password_hash'], row['profile_picture_url'],
                row['user_type'], bool(row['is_active']), row['last_login'])
        ]
    else:
        return None

def search_user_by_name(fullname):
    search_name = "%" + str(fullname) + "%"
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT user_id,fullname, email, phone_number,
                password_hash ,profile_picture_url,
                user_type, is_active, last_login
        FROM user_table
        WHERE fullname LIKE %s
    """, search_name)
    result = cur.fetchall()
    cur.close()
    if result is not None:
        return [
            User(str(row['user_id']), row['fullname'], row['email'],row['phone_number'],
                row['password_hash'], row['profile_picture_url'],
                row['user_type'], bool(row['is_active']), row['last_login']) for row in result
        ]
    else:
        return None

def add_user(form):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO user_table (email, password_hash, fullname, phone_number, user_type, is_active, is_verified, created_at, updated_at, last_login, profile_picture_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s)"""
        , (form.email.data, str(generate_password_hash(form.password.data)), form.fullname.data, form.phone_number.data, "Customer", int(1), int(1), curent_timestamp, curent_timestamp, curent_timestamp,"user.jpg"))
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
    """, user_id)
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
    pass
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
#add somethin here
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
        Product(str(row['product_id']), row['product_name'], row['description'],
             row['category'], float(row['price']), float(row['food_rating']), int(row['prep_time_est']),
             row['food_image_url'], row['is_active'], str(row['restaurant_id'])) for row in results
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
        Product(str(row['product_id']), row['product_name'], row['description'],
             row['category'], float(row['price']), float(row['food_rating']), int(row['prep_time_est']),
             row['food_image_url'], row['is_active'], str(row['restaurant_id']))
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
        Product(str(row['product_id']), row['product_name'], row['description'],
             row['category'], float(row['price']), float(row['food_rating']), int(row['prep_time_est']),
             row['food_image_url'], row['is_active'], str(row['restaurant_id'])) for row in results
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
        Product(str(row['product_id']), row['product_name'], row['description'],
             row['category'], float(row['price']), float(row['food_rating']), int(row['prep_time_est']),
             row['food_image_url'], row['is_active'], str(row['restaurant_id'])) for row in results
    ]

def add_product(form):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO product_table (product_name,description,category,price,food_rating,
                prep_time_est,food_image_url,is_active,created_at,updated_at,restaurant_id))
        VALUES (%s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s)"""
        , (form.product_name.data, form.description.data, form.category.data, form.price.data, form.food_rating.data,
           form.prep_time_est.data, form.food_image_url.data, form.is_active.data, curent_timestamp, curent_timestamp,form.restaurant_id.data))
    mysql.connection.commit()
    cur.close()
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
        Restaurant(str(row['restaurant_id']), row['owner_id'], row['restaurant_name'],
             bool(row['is_indigenous']), row['address'], bool(row['is_active']), row['phone'],
             row['email'], row['website'], row['description'], row['image_url']) for row in results
    ]

def get_restaurant_by_id(restaurant_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT *
        FROM restaurant
        WHERE restaurant_id = %s
    """, (restaurant_id,))
    row = cur.fetchone()
    cur.close()
    return [
        Restaurant(str(row['restaurant_id']), row['owner_id'], row['restaurant_name'],
             bool(row['is_indigenous']), row['address'], bool(row['is_active']), row['phone'],
             row['email'], row['website'], row['description'], row['image_url'])
    ]

def get_restaurant_by_name(restaurant_name):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT *
        FROM restaurant
        WHERE restaurant_id = %s
    """, (restaurant_name,))
    row = cur.fetchone()
    cur.close()
    return [
        Restaurant(str(row['restaurant_id']), row['owner_id'], row['restaurant_name'],
             bool(row['is_indigenous']), row['address'], bool(row['is_active']), row['phone'],
             row['email'], row['website'], row['description'], row['image_url'])
    ]

#add
#update
#delete

##################
#    DRIVER QUERIES   
##################
def get_driver_details_by_user_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT delivery_driver.driver_id, delivery_driver.user_id, delivery_driver.vehicle_type,
                delivery_driver.license_number, delivery_driver.vehicle_plate, delivery_driver.driver_rating,
                delivery_driver.total_deliveries,
                user_table.user_id, user_table.fullname, user_table.email, user_table.phone_number,
                user_table.profile_picture_url, user_table.is_active, delivery_driver.is_available
                
        FROM delivery_driver, user_table
        WHERE delivery_driver.user_id = user_table.user_id AND user_table.is_active = 1 AND delivery_driver.is_available = 1 AND delivery_driver.user_id = %s
    """, (user_id, ))
    row = cur.fetchone()
    cur.close()
    return [
        Driver(row['driver_id'], row['user_id'], row['vehicle_type'],
             row['license_number'], row['vehicle_plate'], float(row['driver_rating']),
             int(row['total_deliveries']),
             row['fullname'], row['email'], row['phone_number'],
             row['profile_picture_url'], row['is_available']
             )
    ]
def get_driver_by_id(driver_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT delivery_driver.driver_id, delivery_driver.user_id, delivery_driver.vehicle_type,
                delivery_driver.license_number, delivery_driver.vehicle_plate, delivery_driver.driver_rating,
                delivery_driver.total_deliveries,
                user_table.user_id, user_table.fullname, user_table.email, user_table.phone_number,
                user_table.profile_picture_url, user_table.is_active, delivery_driver.is_available
                
        FROM delivery_driver, user_table
        WHERE delivery_driver.user_id = user_table.user_id AND user_table.is_active = 1 AND delivery_driver.is_available = 1 AND delivery_driver.driver_id = %d
    """, driver_id)
    row = cur.fetchone()
    cur.close()
    return [
        Driver(str(row['delivery_driver.driver_id']), str(row['delivery_driver.user_id']), row['delivery_driver.vehicle_type'],
             row['delivery_driver.license_number'], row['delivery_driver.vehicle_plate'], float(row['delivery_driver.driver_rating']),
             int(row['delivery_driver.total_deliveries']),
             row['user_table.fullname'], row['user_table.email'], row['user_table.phone_number'],
             row['user_table.profile_picture_url'], row['delivery_driver.is_available']
             )
    ]

def get_all_driver():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT delivery_driver.driver_id, delivery_driver.user_id, delivery_driver.vehicle_type,
                delivery_driver.license_number, delivery_driver.vehicle_plate, delivery_driver.driver_rating,
                delivery_driver.total_deliveries,
                user_table.user_id, user_table.fullname, user_table.email, user_table.phone_number,
                user_table.profile_picture_url, user_table.is_active, delivery_driver.is_available,
                CASE WHEN delivery_driver.is_available = 1 THEN 'Available'
                WHEN delivery_driver.is_available = 0 THEN 'Unavailable'
                END AS driver_is_available
                
        FROM delivery_driver, user_table
        WHERE delivery_driver.user_id = user_table.user_id AND user_table.is_active = 1
    """)
    results = cur.fetchall()
    cur.close()
    return [
        Driver(str(row['delivery_driver.driver_id']), str(row['delivery_driver.user_id']), row['delivery_driver.vehicle_type'],
             row['delivery_driver.license_number'], row['delivery_driver.vehicle_plate'], float(row['delivery_driver.driver_rating']),
             int(row['delivery_driver.total_deliveries']),
             row['user_table.fullname'], row['user_table.email'], row['user_table.phone_number'],
             row['user_table.profile_picture_url'], row['user_table.is_active'], row['driver_is_available']
             ) for row in results
    ]

def get_available_driver():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT delivery_driver.driver_id, delivery_driver.user_id, delivery_driver.vehicle_type,
                delivery_driver.license_number, delivery_driver.vehicle_plate, delivery_driver.driver_rating,
                delivery_driver.total_deliveries,
                user_table.user_id, user_table.fullname, user_table.email, user_table.phone_number,
                user_table.profile_picture_url, user_table.is_active, delivery_driver.is_available
                
        FROM delivery_driver, user_table
        WHERE delivery_driver.user_id = user_table.user_id AND user_table.is_active = 1 AND delivery_driver.is_available = 1
    """)
    results = cur.fetchall()
    cur.close()
    return [
        Driver(str(row['delivery_driver.driver_id']), str(row['delivery_driver.user_id']), row['delivery_driver.vehicle_type'],
             row['delivery_driver.license_number'], row['delivery_driver.vehicle_plate'], float(row['delivery_driver.driver_rating']),
             int(row['delivery_driver.total_deliveries']),
             row['user_table.fullname'], row['user_table.email'], row['user_table.phone_number'],
             row['user_table.profile_picture_url'], row['delivery_driver.is_available']
             ) for row in results
    ]

#add driver
#update driver
#delete driver

##################
#    ORDER QUERIES   
##################
def get_all_orders_and_products():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT ot.*, cart.*, pt.*, cart.quantity * pt.price as total
        FROM order_table ot
        JOIN cart_items cart ON ot.order_id = cart.order_id
        JOIN product_table pt ON cart.product_id = pt.product_id
    """)
    results = cur.fetchall()
    cur.close()
    # return [
    #     Order(str(row['restaurant_id']), row['owner_id'], row['restaurant_name'],
    #          bool(row['is_indigenous']), row['address'], bool(row['is_active']), row['phone'],
    #          row['email'], row['website'], row['description'], row['image_url']) for row in results
    # ]
    return results

def get_all_orders():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT ordert.order_id, ordert.user_id, ordert.driver_id, ordert.address_id, ordert.status ,ordert.total_price,
                ordert.payment_status, ordert.payment_method, ordert.placed_at, ordert.delivered_at, ordert.canceled_at ,ordert.notes,
                ordert.payment_invoice, ordert.delivery_option,
                usert.fullname, usert.email, usert.phone_number,
                CONCAT(addt.label, ', ', addt.address_line1, ', ',addt.address_line2, ', ',addt.city,', ',addt.state, ', ',addt.postal_code, ', ',addt.country) as address
        FROM order_table ordert, user_table usert, user_address addt
        WHERE ordert.user_id = usert.user_id AND ordert.address_id = addt.address_id
        ORDER BY ordert.status
    """)
    results = cur.fetchall()
    cur.close()
    return [
        Order(str(row['order_id']), row['user_id'], row['driver_id'], row['status'], row['total_price'],
              row['payment_status'], row['payment_method'], row['placed_at'], row['delivered_at'],row['canceled_at'], row['notes'],
              row['payment_invoice'], row['delivery_option'],
              row['fullname'], row['email'],row['phone_number'],
              row['address']
             ) for row in results
    ]

def get_all_orders_by_id(order_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT ordert.order_id, ordert.user_id, ordert.driver_id, ordert.address_id, ordert.status ,ordert.total_price,
                ordert.payment_status, ordert.payment_method, ordert.placed_at, ordert.delivered_at, ordert.canceled_at ,ordert.notes,
                ordert.payment_invoice, ordert.delivery_option,
                usert.fullname, usert.email, usert.phone_number,
                CONCAT(addt.label, ', ', addt.address_line1, ', ',addt.address_line2, ', ',addt.city,', ',addt.state, ', ',addt.postal_code, ', ',addt.country) as address
        FROM order_table ordert, user_table usert, user_address addt
        WHERE ordert.user_id = usert.user_id AND ordert.address_id = addt.address_id AND ordert.order_id = %s
        ORDER BY ordert.status
    """, (order_id,))
    row = cur.fetchone()
    cur.close()
    return [
        Order(str(row['order_id']), row['user_id'], row['driver_id'], row['status'], row['total_price'],
              row['payment_status'], row['payment_method'], row['placed_at'], row['delivered_at'],row['canceled_at'], row['notes'],
              row['payment_invoice'], row['delivery_option'],
              row['fullname'], row['email'],row['phone_number'],
              row['address']
             )
    ]

def get_all_orders_by_user_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT ordert.order_id, ordert.user_id, ordert.driver_id, ordert.address_id, ordert.status ,ordert.total_price,
                ordert.payment_status, ordert.payment_method, ordert.placed_at, ordert.delivered_at, ordert.canceled_at ,ordert.notes,
                ordert.payment_invoice, ordert.delivery_option,
                usert.fullname, usert.email, usert.phone_number,
                CONCAT(addt.label, ', ', addt.address_line1, ', ',addt.address_line2, ', ',addt.city,', ',addt.state, ', ',addt.postal_code, ', ',addt.country) as address
        FROM order_table ordert, user_table usert, user_address addt
        WHERE ordert.user_id = usert.user_id AND ordert.address_id = addt.address_id AND ordert.user_id = %s
        ORDER BY ordert.status
    """, (user_id,))
    results = cur.fetchall()
    cur.close()
    return [
        Order(str(row['order_id']), row['user_id'], row['driver_id'], row['status'], row['total_price'],
              row['payment_status'], row['payment_method'], row['placed_at'], row['delivered_at'],row['canceled_at'], row['notes'],
              row['payment_invoice'], row['delivery_option'],
              row['fullname'], row['email'],row['phone_number'],
              row['address']
             ) for row in results
    ]

def get_all_orders_by_driver_id_status(driver_id, status):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT ordert.order_id, ordert.user_id, ordert.driver_id, ordert.address_id, ordert.status ,ordert.total_price,
                ordert.payment_status, ordert.payment_method, ordert.placed_at, ordert.delivered_at, ordert.canceled_at ,ordert.notes,
                ordert.payment_invoice, ordert.delivery_option,
                usert.fullname, usert.email, usert.phone_number,
                CONCAT(addt.label, ', ', addt.address_line1, ', ',addt.address_line2, ', ',addt.city,', ',addt.state, ', ',addt.postal_code, ', ',addt.country) as address
        FROM order_table ordert, user_table usert, user_address addt
        WHERE ordert.user_id = usert.user_id AND ordert.address_id = addt.address_id AND ordert.driver_id = %s AND ordert.status = %s
        ORDER BY ordert.status
    """, (driver_id, status,))
    results = cur.fetchall()
    cur.close()
    return [
        Order(str(row['order_id']), row['user_id'], row['driver_id'], row['status'], row['total_price'],
              row['payment_status'], row['payment_method'], row['placed_at'], row['delivered_at'],row['canceled_at'], row['notes'],
              row['payment_invoice'], row['delivery_option'],
              row['fullname'], row['email'],row['phone_number'],
              row['address']
             ) for row in results
    ]

def get_all_orders_by_status(status):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT ordert.order_id, ordert.user_id, ordert.driver_id, ordert.address_id, ordert.status ,ordert.total_price,
                ordert.payment_status, ordert.payment_method, ordert.placed_at, ordert.delivered_at, ordert.canceled_at ,ordert.notes,
                ordert.payment_invoice, ordert.delivery_option,
                usert.fullname, usert.email, usert.phone_number,
                CONCAT(addt.label, ', ', addt.address_line1, ', ',addt.address_line2, ', ',addt.city,', ',addt.state, ', ',addt.postal_code, ', ',addt.country) as address
        FROM order_table ordert, user_table usert, user_address addt
        WHERE ordert.user_id = usert.user_id AND ordert.address_id = addt.address_id AND ordert.status = %s
        ORDER BY ordert.status
    """, (status,))
    results = cur.fetchall()
    cur.close()
    return [
        Order(str(row['order_id']), row['user_id'], row['driver_id'], row['status'], row['total_price'],
              row['payment_status'], row['payment_method'], row['placed_at'], row['delivered_at'],row['canceled_at'], row['notes'],
              row['payment_invoice'], row['delivery_option'],
              row['fullname'], row['email'],row['phone_number'],
              row['address']
             ) for row in results
    ]

##################
#    CART QUERIES   
##################
def get_all_cart_items():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT cart.*, pt.*, cart.quantity * pt.price as total
        FROM cart_items cart
        JOIN product_table pt ON cart.product_id = pt.product_id
    """)
    results = cur.fetchall()
    cur.close()
    return [
        CartItem(Product(str(row['product_id']), row['product_name'], row['description'],
             row['category'], float(row['price']), float(row['food_rating']), int(row['prep_time_est']),
             row['food_image_url'], row['is_active'], str(row['restaurant_id'])), row['quantity']) for row in results
    ]
   
    return results

def get_all_cart_items_by_user_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT cart.*, pt.*, cart.quantity * pt.price as total
        FROM cart_items cart
        JOIN product_table pt ON cart.product_id = pt.product_id
        WHERE cart.user_id = %s
    """, (user_id,))
    results = cur.fetchall()
    cur.close()
    return [
        CartItem(Product(str(row['product_id']), row['product_name'], row['description'],
             row['category'], float(row['price']), float(row['food_rating']), int(row['prep_time_est']),
             row['food_image_url'], row['is_active'], str(row['restaurant_id'])), row['quantity']) for row in results
    ]