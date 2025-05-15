from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from flask_mysqldb import MySQL

class User:
    def __init__(self, id, email, password_hash, role, is_active, created_at):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.is_active = is_active
        self.created_at = created_at

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def create_user(email, password, role='customer'):
        cursor = current_app.mysql.connection.cursor()
        password_hash = generate_password_hash(password)
        try:
            cursor.execute("INSERT INTO users (email, password_hash, role, created_at) VALUES (%s, %s, %s, %s)",
                           (email, password_hash, role, datetime.now()))
            current_app.mysql.connection.commit()
            user_id = cursor.lastrowid
            cursor.execute("INSERT INTO carts (user_id) VALUES (%s)", (user_id,))
            current_app.mysql.connection.commit()
            return User.get_by_id(user_id)
        except Exception as e:
            current_app.mysql.connection.rollback()
            print(f"Error creating user: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_id(user_id):
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT id, email, password_hash, role, is_active, created_at FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return User(*result)
        return None

    @staticmethod
    def get_by_email(email):
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT id, email, password_hash, role, is_active, created_at FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return User(*result)
        return None

    def is_available_driver(self):
        if self.role == 'driver':
            cursor = current_app.mysql.connection.cursor()
            cursor.execute("""
                SELECT status
                FROM orders
                WHERE driver_id = %s AND status IN ('assigned', 'in_transit')
            """, (self.id,))
            active_orders = cursor.fetchall()
            cursor.close()
            return not active_orders
        return False

    @staticmethod
    def add_to_cart(user_id, product_id, quantity=1):
        cursor = current_app.mysql.connection.cursor()
        try:
            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            user_result = cursor.fetchone()
            if not user_result:
                return False

            # Check if product exists and has enough stock
            cursor.execute("SELECT stock FROM products WHERE id = %s", (product_id,))
            product_result = cursor.fetchone()
            if not product_result or product_result[0] < quantity:
                return False

            # Get the user's cart ID
            cursor.execute("SELECT id FROM carts WHERE user_id = %s", (user_id,))
            cart_result = cursor.fetchone()
            if not cart_result:
                # Create a cart if it doesn't exist (though create_user should handle this)
                cursor.execute("INSERT INTO carts (user_id) VALUES (%s)", (user_id,))
                current_app.mysql.connection.commit()
                cart_id = cursor.lastrowid
            else:
                cart_id = cart_result[0]

            # Check if the item is already in the cart
            cursor.execute("SELECT id, quantity FROM cart_items WHERE cart_id = %s AND product_id = %s", (cart_id, product_id))
            existing_item = cursor.fetchone()

            if existing_item:
                new_quantity = existing_item[1] + quantity
                cursor.execute("UPDATE cart_items SET quantity = %s WHERE id = %s", (new_quantity, existing_item[0]))
            else:
                cursor.execute("INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (%s, %s, %s)",
                               (cart_id, product_id, quantity))

            current_app.mysql.connection.commit()
            return True
        except Exception as e:
            current_app.mysql.connection.rollback()
            print(f"Error adding to cart: {e}")
            return False
        finally:
            cursor.close()

class Product:
    def __init__(self, id, name, price, stock, description):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
        self.description = description

    @staticmethod
    def get_by_id(product_id):
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT id, name, price, stock, description FROM products WHERE id = %s", (product_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return Product(*result)
        return None

    def update_stock(self, change):
        cursor = app.mysql.connection.cursor()
        new_stock = self.stock + change
        if new_stock >= 0:
            cursor.execute("UPDATE products SET stock = %s WHERE id = %s", (new_stock, self.id))
            current_app.mysql.connection.commit()
            self.stock = new_stock
            cursor.close()
            return True
        cursor.close()
        return False

class Cart:
    def __init__(self, id, user_id):
        self.id = id
        self.user_id = user_id
        self.items = self._get_items()

    @staticmethod
    def get_by_user_id(user_id):
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT id FROM carts WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return Cart(result[0], user_id)
        return None

    def _get_items(self):
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("""
            SELECT cart_items.id, cart_items.product_id, cart_items.quantity, products.name, products.price
            FROM cart_items
            JOIN products ON cart_items.product_id = products.id
            WHERE cart_items.cart_id = %s
        """, (self.id,))
        results = cursor.fetchall()
        cursor.close()
        return [CartItem(row[0], self.id, row[1], row[2], row[3], row[4]) for row in results]

    @property
    def total(self):
        return sum(item.subtotal for item in the items)

    def add_item(self, product_id, quantity=1):
        if quantity <= 0:
            return False
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT stock FROM products WHERE id = %s", (product_id,))
        product_stock = cursor.fetchone()
        if not product_stock or product_stock[0] < quantity:
            cursor.close()
            return False

        cursor.execute("SELECT id, quantity FROM cart_items WHERE cart_id = %s AND product_id = %s", (self.id, product_id))
        existing_item = cursor.fetchone()
        if existing_item:
            new_quantity = existing_item[1] + quantity
            cursor.execute("UPDATE cart_items SET quantity = %s WHERE id = %s", (new_quantity, existing_item[0]))
        else:
            cursor.execute("INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (%s, %s, %s)",
                           (self.id, product_id, quantity))
        current_app.mysql.connection.commit()
        cursor.close()
        self.items = self._get_items() # Refresh items
        return True

    def clear(self):
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("DELETE FROM cart_items WHERE cart_id = %s", (self.id,))
        current_app.mysql.connection.commit()
        cursor.close()
        self.items = []

class CartItem:
    def __init__(self, id, cart_id, product_id, quantity, product_name, product_price):
        self.id = id
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity
        self.product_name = product_name
        self.product_price = product_price

    @property
    def subtotal(self):
        return self.product_price * self.quantity

class Order:
    def __init__(self, id, customer_id, driver_id, status, created_at, delivered_at):
        self.id = id
        self.customer_id = customer_id
        self.driver_id = driver_id
        self.status = status
        self.created_at = created_at
        self.delivered_at = delivered_at
        self.items = self._get_items()

    @staticmethod
    def create_order(user_id, cart_items):
        cursor = current_app.mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO orders (customer_id, status, created_at) VALUES (%s, %s, %s)",
                           (user_id, 'pending', datetime.utcnow()))
            order_id = cursor.lastrowid
            for item in cart_items:
                cursor.execute("""
                    INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase)
                    VALUES (%s, %s, %s, %s)
                """, (order_id, item.product_id, item.quantity, item.product_price))
                cursor.execute("UPDATE products SET stock = stock - %s WHERE id = %s", (item.quantity, item.product_id))
            cursor.execute("DELETE FROM cart_items WHERE cart_id = (SELECT id FROM carts WHERE user_id = %s)", (user_id,))
            current_app.mysql.connection.commit()
            return Order.get_by_id(order_id)
        except Exception as e:
            current_app.mysql.connection.rollback()
            print(f"Error creating order: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_id(order_id):
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT id, customer_id, driver_id, status, created_at, delivered_at FROM orders WHERE id = %s", (order_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return Order(*result)
        return None

    def _get_items(self):
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("""
            SELECT order_items.id, order_items.product_id, order_items.quantity, order_items.price_at_purchase, products.name
            FROM order_items
            JOIN products ON order_items.product_id = products.id
            WHERE order_items.order_id = %s
        """, (self.id,))
        results = cursor.fetchall()
        cursor.close()
        return [OrderItem(row[0], self.id, row[1], row[2], row[3], row[4]) for row in results]

    @property
    def total(self):
        return sum(item.subtotal for item in self.items)

    def confirm(self):
        if self.status == 'pending':
            cursor = current_app.mysql.connection.cursor()
            cursor.execute("UPDATE orders SET status = 'confirmed' WHERE id = %s", (self.id,))
            current_app.mysql.connection.commit()
            cursor.close()
            self.status = 'confirmed'
            return True
        return False

    def assign_driver(self):
        if self.status != 'confirmed':
            return False
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("""
            SELECT id FROM users
            WHERE role = 'driver' AND id NOT IN (SELECT driver_id FROM orders WHERE status IN ('assigned', 'in_transit'))
            LIMIT 1
        """)
        driver_result = cursor.fetchone()
        if driver_result:
            driver_id = driver_result[0]
            cursor.execute("UPDATE orders SET driver_id = %s, status = 'assigned' WHERE id = %s", (driver_id, self.id))
            current_app.mysql.connection.commit()
            cursor.close()
            self.driver_id = driver_id
            self.status = 'assigned'
            return True
        cursor.close()
        return False

    def mark_delivered(self):
        if self.status == 'assigned':
            cursor = current_app.mysql.connection.cursor()
            cursor.execute("UPDATE orders SET status = 'delivered', delivered_at = %s WHERE id = %s", (datetime.utcnow(), self.id))
            current_app.mysql.connection.commit()
            cursor.close()
            self.status = 'delivered'
            self.delivered_at = datetime()
            return True
        return False

    @staticmethod
    def process_checkout(user_id):
        cart = Cart.get_by_user_id(user_id)
        if not cart or not cart.items:
            return None

        with app.mysql.connection.cursor() as cursor:
            try:
                # Verify stock
                for item in cart.items:
                    cursor.execute("SELECT stock FROM products WHERE id = %s", (item.product_id,))
                    product_stock = cursor.fetchone()
                    if not product_stock or product_stock[0] < item.quantity:
                        return None # Insufficient stock

                order = Order.create_order(user_id, cart.items)
                if order:
                    # Update product stock and clear cart
                    for item in cart.items:
                        cursor.execute("UPDATE products SET stock = stock - %s WHERE id = %s", (item.quantity, item.product_id))
                    cursor.execute("DELETE FROM cart_items WHERE cart_id = (SELECT id FROM carts WHERE user_id = %s)", (user_id,))
                    current_app.mysql.connection.commit()

                    # Attempt to assign a driver immediately after checkout
                    order = Order.get_by_id(order.id) # Refresh order object
                    order.assign_driver()
                    return order
                return None
            except Exception as e:
                app.mysql.connection.rollback()
                print(f"Error during checkout: {e}")
                return None
            finally:
                cursor.close()

    def accept_delivery(self, driver_id):
        cursor = current_app.mysql.connection.cursor()
        try:
            if self.driver_id == driver_id and self.status == 'confirmed':
                cursor.execute("UPDATE orders SET status = 'assigned' WHERE id = %s", (self.id,))
                current_app.mysql.connection.commit()
                self.status = 'assigned'
                return True
            return False
        except Exception as e:
            current_app.mysql.connection.rollback()
            print(f"Error accepting delivery for order {self.id}: {e}")
            return False
        finally:
            cursor.close()

    @staticmethod
    def get_orders_by_status(status):
        cursor = current_app.mysql.connection.cursor()
        try:
            cursor.execute("SELECT id, customer_id, driver_id, status, created_at, delivered_at FROM orders WHERE status = %s", (status,))
            results = cursor.fetchall()
            cursor.close()
            return [Order(*row) for row in results]
        except Exception as e:
            print(f"Error getting orders by status: {e}")
            return []
        finally:
            cursor.close()

class OrderItem:
    def __init__()
            