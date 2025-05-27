# dummyDb.py
#from project.models import Product, ProductCategory, Restaurant, User, Driver, UserRole, Order, OrderItem
from project.models import *
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mysqldb import MySQL

current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

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
            return User(row['user_id'], row['fullname'], row['email'], row['phone_number'], row['password_hash'], row['profile_picture_url'], row['user_type'], row['is_active'])
                           
    return None

#####################
#    USER QUERIES   #
#####################

def get_all_users():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT user_id,fullname, email, phone_number,
                password_hash ,profile_picture_url,
                user_type, is_active, last_login
        FROM user_table
    """, )
    results = cur.fetchall()
    cur.close()
    if results is not None:
        return [
            User(str(row['user_id']), row['fullname'], row['email'],row['phone_number'],
                row['password_hash'], row['profile_picture_url'],
                row['user_type'], bool(row['is_active']), row['last_login']) for row in results
        ]
    else:
        return []
    
def get_all_users_by_status(is_active):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT user_id,fullname, email, phone_number,
                password_hash ,profile_picture_url,
                user_type, is_active, last_login
        FROM user_table
        WHERE is_active = %s
    """, (is_active,))
    
    results = cur.fetchall()
    cur.close()
    if results is not None:
        return [
            User(str(row['user_id']), row['fullname'], row['email'],row['phone_number'],
                row['password_hash'], row['profile_picture_url'],
                row['user_type'], bool(row['is_active']), row['last_login']) for row in results
        ]
    else:
        return []

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
        return []

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
    
def get_user_info_with_address_by_user_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT user_table.user_id,fullname, email, phone_number,
                password_hash ,profile_picture_url,
                user_type, is_active, last_login,
                CONCAT(addt.label, ', ', addt.address_line1, ', ',addt.address_line2, ', ',addt.city,', ',addt.state, ', ',addt.postal_code, ', ',addt.country) as address
        FROM user_table, user_address addt
        WHERE user_table.user_id = %s AND user_table.user_id = addt.user_id
    """, (user_id,))
    row = cur.fetchone()
    cur.close()
    if row is not None:
        return [
            User(str(row['user_id']), row['fullname'], row['email'],row['phone_number'],
                row['password_hash'], row['profile_picture_url'],
                row['user_type'], bool(row['is_active']), row['last_login']), row['address']
        ]
    else:
        return None
    
def get_user_info_with_address_by_email(email):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT user_table.user_id,fullname, email, phone_number,
                password_hash ,profile_picture_url,
                user_type, is_active, last_login,
                CONCAT(addt.label, ', ', addt.address_line1, ', ',addt.address_line2, ', ',addt.city,', ',addt.state, ', ',addt.postal_code, ', ',addt.country) as address
        FROM user_table, user_address addt
        WHERE user_table.email = %s AND user_table.user_id = addt.user_id
    """, (email,))
    row = cur.fetchone()
    cur.close()
    if row is not None:
        return [
            User(str(row['user_id']), row['fullname'], row['email'],row['phone_number'],
                row['password_hash'], row['profile_picture_url'],
                row['user_type'], bool(row['is_active']), row['last_login']), row['address']
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
        , (form.email.data, str(generate_password_hash(form.password.data)), form.fullname.data, form.phone_number.data, "Customer", int(1), int(1), current_timestamp, current_timestamp, current_timestamp,"user.jpg"))
    
    user_id = cur.lastrowid

    cur.execute("""
        INSERT INTO user_address (user_id, label, address_line1, address_line2,
                city, state, postal_code, country, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (str(user_id), form.label.data, form.address_line1.data, form.address_line2.data,
                form.city.data, form.state.data, form.postal_code.data, form.country.data,
                current_timestamp, current_timestamp,))
    
    mysql.connection.commit()
    cur.close()

def update_user_profile(fullname, phone, profile_picture_url, email):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE user_table
        SET fullname = %s, phone_number = %s, profile_picture_url = %s
        WHERE  email = %s
    """, (fullname, phone, profile_picture_url,email,))

    mysql.connection.commit()
    cur.close()

def set_user_role(user_id, user_type):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE user_table 
        SET user_type = %s
        WHERE user_id = %s
    """, (user_type, user_id,))

    mysql.connection.commit()
    cur.close()

def set_user_is_active(user_id, is_active):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE user_table
        SET is_active = %s
        WHERE  user_id = %s
    """, (is_active, user_id,))

    mysql.connection.commit()
    cur.close()
#delete

##################
#    ADDRESS QUERIES   
##################
def get_address_by_user_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT address_id,user_id,
                address_line1, address_line2 ,city,
                state, postal_code, country,
                created_at, updated_at
        FROM user_address
        WHERE user_id = %s
    """, (user_id,))
    row = cur.fetchone()
    cur.close()
    return [
        UserAddress(str(row['address_id']), row['user_id'],
             row['address_line1'], row['address_line2'], row['city'],
             row['state'], row['postal_code'], row['country'],
             row['created_at'], row['updated_at']
            )
    ]

def get_address_id_by_user_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT address_id
        FROM user_address
        WHERE user_id = %s
    """, (user_id,))
    row = cur.fetchone()
    cur.close()
    if row:
        return row['address_id']
    else:
        return ""
   
def add_address_by_user_id(form):
    pass
    # cur = mysql.connection.cursor()
    # cur.execute("""
    #     INSERT INTO user_address (
    #                             )
    #     VALUES (%s, %s, %s, %s,
    #             %s, %s, %d, %d,
    #             current_timestamp, current_timestamp
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
        SELECT product_table.*, categories.category_name
        FROM product_table, categories
        WHERE deleted = 0 AND product_table.category = categories.category_id
    """)
    results = cur.fetchall()
    cur.close()

    return [
        Product(str(row['product_id']), row['product_name'], row['description'],
             row['category_name'], float(row['price']), float(row['food_rating']), int(row['prep_time_est']),
             row['food_image_url'], row['is_active'], str(row['restaurant_id'])) for row in results
    ]

def get_product_by_id(product_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT product_table.*, categories.category_name
        FROM product_table, categories
        WHERE product_id = %s AND product_table.category = categories.category_id
    """ , (product_id,))
    row = cur.fetchone()
    #print("id: ", product_id)
    cur.close()
    if row is not None:
        return Product(row['product_id'], row['product_name'], row['description'],
                row['category'], float(row['price']), float(row['food_rating']), int(row['prep_time_est']),
                row['food_image_url'], row['is_active'], str(row['restaurant_id']))
    else:
        return []

def search_product(search_str):
    like_str = "%" + str(search_str) + "%"
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT product_table.*, categories.category_name
        FROM product_table, categories
        WHERE (product_name LIKE %s OR description LIKE %s OR category LIKE %s OR product_id LIKE %s) AND deleted = 0 AND product_table.category = categories.category_id
    """ , (like_str, like_str, like_str, like_str, ))
    results = cur.fetchall()
    cur.close()
    return [
        Product(str(row['product_id']), row['product_name'], row['description'],
             row['category'], float(row['price']), float(row['food_rating']), int(row['prep_time_est']),
             row['food_image_url'], row['is_active'], str(row['restaurant_id'])) for row in results
    ]

def search_order_name_id_status(search_str, status, date_start="2025-05-01 18:35:48", date_end="2025-05-30 18:35:48"):
    like_str = "%" + str(search_str) + "%"
    like_status = "%" + str(status) + "%"
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT ordert.order_id, ordert.user_id, ordert.driver_id, ordert.address_id, ordert.status ,ordert.total_price,
                ordert.payment_status, ordert.payment_method, ordert.placed_at, ordert.delivered_at, ordert.canceled_at ,ordert.notes,
                ordert.payment_invoice, ordert.delivery_option,
                usert.fullname, usert.email, usert.phone_number,
                CONCAT(addt.label, ', ', addt.address_line1, ', ',addt.address_line2, ', ',addt.city,', ',addt.state, ', ',addt.postal_code, ', ',addt.country) as address
        FROM order_table ordert, user_table usert, user_address addt
        WHERE (ordert.user_id = usert.user_id AND ordert.address_id = addt.address_id)
                AND ((ordert.order_id LIKE %s OR usert.fullname LIKE %s) AND ordert.status LIKE %s
                AND (ordert.placed_at BETWEEN %s AND %s))
        ORDER BY ordert.status
    """, (like_str, like_str, like_status, date_start, date_end))
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
    cur.execute("""
        SELECT *
        FROM order_table
        WHERE (product_name LIKE %s OR description LIKE %s OR category LIKE %s OR product_id LIKE %s) AND deleted = 0
    """ , (like_str, like_str, like_str, like_str, ))
    

def search_users(search_str):
    like_str = "%" + str(search_str) + "%"
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT *
        FROM user_table
        WHERE fullname LIKE %s OR user_type LIKE %s OR email LIKE %s
    """ , (like_str, like_str, like_str, ))
    results = cur.fetchall()
    cur.close()
    return [
        User(str(row['user_id']), row['fullname'], row['email'],row['phone_number'],
                row['password_hash'], row['profile_picture_url'],
                row['user_type'], bool(row['is_active']), row['last_login']) for row in results
    ]

def get_product_by_category(categ):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT product_table.*, categories.category_name
        FROM product_table, categories
        WHERE categories.category_name = %s product_table.category = categories.category_id
    """ % categ)
    results = cur.fetchall()
    cur.close()

    return [
        Product(str(row['product_id']), row['product_name'], row['description'],
             row['category'], float(row['price']), float(row['food_rating']), int(row['prep_time_est']),
             row['food_image_url'], row['is_active'], str(row['restaurant_id'])) for row in results
    ]

def add_product_to_db(form):
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            INSERT INTO product_table (product_name,description,category,price,food_rating,
                    prep_time_est,food_image_url,is_active,created_at,updated_at,restaurant_id)
            VALUES (%s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s)"""
            , (form.product_name.data, form.description.data, form.category.data, form.price.data, form.food_rating.data,
            form.prep_time_est.data, form.food_image_url.data.filename, form.is_active.data, current_timestamp, current_timestamp,form.restaurant_id.data))
        mysql.connection.commit()
        cur.close()
    except:
        return

def update_product_table(form):

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE product_table
        SET product_name = %s,category = %s, price = %s, is_active = %s, description = %s, food_image_url = %s
        WHERE  product_id = %s
    """, (form.product_name.data, form.category.data, form.price.data, form.is_active.data, form.description.data, form.food_image_url.data.filename, form.product_id.data, ))

    mysql.connection.commit()
    cur.close()

def delete_product_from_list(product_id):

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE product_table
        SET deleted = 1
        WHERE  product_id = %s
    """, ( product_id,))

    mysql.connection.commit()
    cur.close()

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
def add_driver(form):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO user_table (email, password_hash, fullname, phone_number, user_type,
                is_active, is_verified, created_at, updated_at, last_login, profile_picture_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s)""", (form.email.data, str(generate_password_hash(form.password.data)),
           form.fullname.data, form.phone_number.data, "Delivery Driver",
           int(1), int(1), current_timestamp, current_timestamp, current_timestamp,"zoro.jpg"))
    
    user_id = cur.lastrowid

    cur.execute("""
        INSERT INTO user_address (user_id, label, address_line1, address_line2,
                city, state, postal_code, country, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (str(user_id), form.label.data, form.address_line1.data, form.address_line2.data,
                form.city.data, form.state.data, form.postal_code.data, form.country.data,
                current_timestamp, current_timestamp,))

    cur.execute("""
        INSERT INTO delivery_driver (user_id, vehicle_type, license_number, vehicle_plate,
                is_available, created_at, updated_at, driver_rating, total_deliveries)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (str(user_id), form.vehicle_type.data,
                                                 form.license_number.data, form.vehicle_plate.data,
           int(1), current_timestamp, current_timestamp, int(5), int(0)))

    mysql.connection.commit()
    cur.close()

def get_driver_details_by_user_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT  driver_id, delivery_driver.user_id as uid,  vehicle_type,
                 license_number,  vehicle_plate,  driver_rating,
                 total_deliveries,is_available,
                user_table.user_id, user_table.fullname, user_table.email, user_table.phone_number,
                user_table.profile_picture_url, user_table.is_active
                
        FROM delivery_driver, user_table
        WHERE delivery_driver.user_id = user_table.user_id AND user_table.is_active = 1 AND delivery_driver.user_id = %s
    """, (user_id, ))
    row = cur.fetchone()
    cur.close()
     
    if row is not None:
        return [
            Driver(str(row['driver_id']), str(row['uid']), row['vehicle_type'],
                row['license_number'], row['vehicle_plate'], float(row['driver_rating']),
                int(row['total_deliveries']),
                row['fullname'], row['email'], row['phone_number'],
                row['profile_picture_url'], row['is_available']
                )
        ]
    else:
        return []

def get_driver_by_id(driver_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT  driver_id, delivery_driver.user_id,  vehicle_type,
                 license_number,  vehicle_plate,  driver_rating,
                 total_deliveries,
                user_table.user_id, user_table.fullname, user_table.email, user_table.phone_number,
                user_table.profile_picture_url, user_table.is_active,  is_available
                
        FROM delivery_driver, user_table
        WHERE delivery_driver.user_id = user_table.user_id AND user_table.is_active = 1 AND  driver_id = %s
    """, (driver_id,))
    row = cur.fetchone()
    cur.close()
    if row is not None:
        return [
            Driver(str(row['driver_id']), str(row['user_id']), row['vehicle_type'],
                    row['license_number'], row['vehicle_plate'], float(row['driver_rating']),
                    int(row['total_deliveries']),
                    row['fullname'], row['email'], row['phone_number'],
                    row['profile_picture_url'], row['is_available']
                    )
        ]
    else:
        return []

def get_all_driver():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT  driver_id, delivery_driver.user_id,  vehicle_type,
                 license_number,  vehicle_plate,  driver_rating,
                 total_deliveries,
                user_table.user_id, user_table.fullname, user_table.email, user_table.phone_number,
                user_table.profile_picture_url, user_table.is_active,  is_available,
                CASE WHEN  is_available = 1 THEN 'Available'
                WHEN  is_available = 0 THEN 'Unavailable'
                END AS driver_is_available
                
        FROM delivery_driver, user_table
        WHERE delivery_driver.user_id = user_table.user_id AND user_table.is_active = 1
    """)
    results = cur.fetchall()
    cur.close()
    if results is not None:
        return [
            Driver(str(row['driver_id']), str(row['user_id']), row['vehicle_type'],
                row['license_number'], row['vehicle_plate'], float(row['driver_rating']),
                int(row['total_deliveries']),
                row['fullname'], row['email'], row['phone_number'],
                row['profile_picture_url'], row['is_active'], row['driver_is_available']
                ) for row in results
        ]
    else:
        return []
    
def get_available_driver():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT  driver_id, delivery_driver.user_id,  vehicle_type,
                 license_number,  vehicle_plate,  driver_rating,
                 total_deliveries,
                user_table.user_id, user_table.fullname, user_table.email, user_table.phone_number,
                user_table.profile_picture_url, user_table.is_active,  is_available
                
        FROM delivery_driver, user_table
        WHERE delivery_driver.user_id = user_table.user_id AND user_table.is_active = 1 AND  is_available = 1
    """)
    results = cur.fetchall()
    cur.close()
    if results is not None:
        return [
            Driver(str(row['driver_id']), str(row['user_id']), row['vehicle_type'],
                row['license_number'], row['vehicle_plate'], float(row['driver_rating']),
                int(row['total_deliveries']),
                row['fullname'], row['email'], row['phone_number'],
                row['profile_picture_url'], row['is_active'], row['driver_is_available']
                ) for row in results
        ]
    else:
        return []
    
def set_driver_status(driver_id, status):
    stat = 0
    if status == "Available":
        stat = 1
    else:
        stat = 0

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE delivery_driver
        SET is_available = %s
        WHERE  driver_id = %s
    """, (stat, driver_id, ))
    mysql.connection.commit()
    cur.close()

def get_driver_status_by_driver_id(driver_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT is_available
        FROM delivery_driver 
        WHERE  driver_id = %s
    """, (driver_id, ))
    row = cur.fetchone()
    cur.close() 
    if row['is_available'] == 1:
        status = "Available"
    elif row['is_available'] == 0:
        status = "Unavailable"
    return status

def driver_accept_delivery(driver_id, order_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE order_table
        SET driver_id = %s
        WHERE order_id= %s
    """, (driver_id, order_id,))
    mysql.connection.commit()
    cur.close()
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

def get_products_from_order_id(order_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT cart.quantity, ot.status, ot.total_price, ot.placed_at, pt.*
        FROM product_table pt
        JOIN cart_items cart ON cart.product_id = pt.product_id
        JOIN order_table ot ON ot.order_id = cart.order_id
        WHERE cart.order_id = %s
    """, (order_id, ))
    results = cur.fetchall()
    cur.close()
    if results:
        return results
    else:
        return []

def get_all_order_items_by_order_id(order_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT ot.*, cart.*, pt.*, cart.quantity * pt.price as total
        FROM order_table ot
        JOIN cart_items cart ON ot.order_id = cart.order_id
        JOIN product_table pt ON cart.product_id = pt.product_id
        WHERE ot.order_id = %s
    """, (order_id, ))
    results = cur.fetchall()
    cur.close()
    if results is not None:
        return results
        #[
            # OrderItem(str(row['order_id']), row['product_id'], row['restaurant_name'],
            #     bool(row['is_indigenous']), row['address'], bool(row['is_active']), row['phone'],
            #     row['email'], row['website'], row['description'], row['image_url']) for row in results
        #]
    else:
        return []
def get_all_order_items_by_order_id_status(order_id, status):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT pt.*, ot.*, cart.*, pt.price as total
        FROM order_table ot
        JOIN cart_items cart ON ot.order_id = cart.order_id
        JOIN product_table pt ON cart.product_id = pt.product_id
        WHERE ot.order_id = %s AND ot.status = %s
    """, (order_id, status,))
    results = cur.fetchall()
    cur.close()
    if results is not None:
        return results
        
    else:
        return []

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
    return Order(str(row['order_id']), row['user_id'], row['driver_id'], row['status'], row['total_price'],
              row['payment_status'], row['payment_method'], row['placed_at'], row['delivered_at'],row['canceled_at'], row['notes'],
              row['payment_invoice'], row['delivery_option'],
              row['fullname'], row['email'],row['phone_number'],
              row['address']
             )
    

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
def set_order_status(order_id, status):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE order_table
        SET status = %s
        WHERE order_id = %s
    """, (status,order_id,))
    mysql.connection.commit()
    cur.close()


#####################################################
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

def get_uncheckedout_cart_items_by_user_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT cart.*, pt.*, cart.quantity * pt.price as total
        FROM cart_items cart
        JOIN product_table pt ON cart.product_id = pt.product_id
        WHERE cart.user_id = %s AND order_id IS NULL
    """, (user_id,))
    results = cur.fetchall()
    cur.close()
    return [
        CartItem(Product(str(row['product_id']), row['product_name'], row['description'],
             row['category'], float(row['price']), float(row['food_rating']), int(row['prep_time_est']),
             row['food_image_url'], row['is_active'], str(row['restaurant_id'])),  row['cart_id'], row['quantity']) for row in results
    ]

def check_if_item_in_cart(product_id, user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 1 FROM cart_items WHERE product_id = %s AND user_id = %s AND order_id IS NULL
    """, (product_id, user_id,))
    results = cur.fetchone()
    cur.close()
    return results

def add_cart_item_to_db(product_id, user_id, quantity, temp_id):
    item_exists = check_if_item_in_cart(product_id, user_id)
    cur = mysql.connection.cursor()
    # IF PRODUCT ID EXISTS, ADD QUANTITY AND UPDATE TEMP ID
    if item_exists:
        cur.execute("""
        UPDATE cart_items
        SET quantity = %s, temp_id = %s
        WHERE product_id = %s AND user_id = %s AND order_id IS NULL;
        """, (quantity, temp_id, product_id, user_id))
    else:
        cur.execute("""
            INSERT INTO cart_items (product_id, user_id, created_at, quantity, temp_id)
            VALUES (%s, %s, %s, %s, %s)"""
            , (product_id, user_id, current_timestamp, quantity, str(temp_id),))
        
    mysql.connection.commit()
    cur.close()

def delete_cart_item_from_db(product_id, user_id,):
    cur = mysql.connection.cursor()
    cur.execute("""
            DELETE FROM cart_items WHERE product_id = %s AND user_id = %s AND order_id IS NULL
            """, (product_id, user_id,))
    mysql.connection.commit()
    cur.close()

def clear_cart_db(user_id,):
    cur = mysql.connection.cursor()
    cur.execute("""
        DELETE FROM cart_items WHERE user_id = %s AND order_id IS NULL
        """
        , (user_id,))
    mysql.connection.commit()
    cur.close()

################################    CHECK OUT QUERIES       #####
def add_order_to_db(order, form, address_id):
    cur = mysql.connection.cursor() 
    cur.execute("""
        INSERT INTO
                order_table (user_id, address_id, status, total_price, payment_status,
                                payment_method, placed_at, notes, payment_invoice, address
                )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        , (order.user_id, address_id ,OrderStatus.PENDING.value, order.total, order.payment_status,
           form.payment_method.data, current_timestamp, form.notes.data ,
           str(str(order.user_id)+str(current_timestamp)), form.address.data, ))
    order_id = cur.lastrowid

    for item in order.items:
        #update order_id in cart_items where product_id = product_id and user_id = user_id
        cur.execute("""
            UPDATE cart_items
            SET order_id = %s
            WHERE product_id = %s AND user_id = %s AND order_id IS NULL
        """, (order_id, item.product.id, order.user_id, ))
        
    mysql.connection.commit()
    cur.close()

####################################    CRUD CATEGORIES     ##################
def add_category_db(category_name):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO categories (category_name)
        VALUES (%s)"""
        , (category_name, ))
    
    mysql.connection.commit()
    cur.close()

def delete_category_db(category_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        DELETE FROM categories
        WHERE category_id = %s
        """
        , (category_id, ))
    
    mysql.connection.commit()
    cur.close()

def update_category_db(category_id, category_name):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE categories
        SET category_name = %s
        WHERE category_id = %s
        """
        , (category_name, category_id,))
    
    mysql.connection.commit()
    cur.close()

def get_all_category_by_categ_id(category_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT * FROM categories WHERE category_id = %s
        """
        ,(category_id,))
    results = cur.fetchone()
    cur.close()
    if results is not None:
        return results
    else:
        return []

def get_all_category():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT * FROM categories
        ORDER BY category_name
        """
        ,)
    results = cur.fetchall()
    cur.close()
    if results is not None:
        return results
    else:
        return []

