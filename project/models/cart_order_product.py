from datetime import datetime
from enum import Enum
from flask import current_app
from models import User

"""
Requires delivery dependency confirming order has been accepted and delivered by driver
"""

###################
# Cart Models
###################

class CartItem:
    def __init__(self, product, quantity=1):
        self.product = product
        self.quantity = quantity

    def get_subtotal(self):
        """Calculate subtotal for this cart item."""
        return self.product.price * self.quantity

    def increment_quantity(self, quantity):
        """Increment the quantity of this cart item."""
        self.quantity += quantity

    def decrement_quantity(self, quantity):
        """Decrement the quantity of this cart item."""
        if self.quantity > quantity:
            self.quantity -= quantity

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        """Add item to cart."""
        cart_item = next((item for item in self.items if item.product.product_id == product.product_id), None)
        if cart_item:
            cart_item.increment_quantity(quantity)
        else:
            self.items.append(CartItem(product, quantity))

    def remove_item(self, product_id):
        """Remove item from cart."""
        self.items = [item for item in self.items if item.product.product_id != product_id]
    
    def clear(self):
        """Empty the cart."""
        self.items = []
    
    def total_cost(self):
        """Calculate the total cost of the cart."""
        total = 0
        for item in self.items:
            total += item.get_subtotal()
        return total

###################
# Order Models
###################

class OrderStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

    @classmethod
    def get_all_values(cls):
        """Return all possible status values as strings."""
        return [status.value for status in cls]

class Order:
    """Model for customer orders."""
    def __init__(self, id, user_id, address="", payment_method="", driver_id="", total=0.0, items=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.status = OrderStatus.PENDING.value  # Default status
        self.address = address
        self.payment_method = payment_method
        self.driver_id = driver_id
        self.total = total
        self.items = items or []
        self.created_at = created_at or datetime.now()

    def get_url(self):
        """Return URL of the order."""
        return f"/order/{self.id}"

    def calculate_total(self):
        """Calculate the total cost of the order based on items."""
        self.total = sum(item.get_subtotal() for item in self.items)
        return self.total

    def update_status(self, status):
        """Update the status of the order."""
        if status in OrderStatus.get_all_values():
            self.status = status

    @staticmethod
    def create_from_cart(cursor, user_id, cart_items, address, payment_method):
        created_at = datetime.now()
        status = OrderStatus.PENDING.value
        total = sum(item['price'] * item['quantity'] for item in cart_items)

        # Insert into orders table
        cursor.execute("""
            INSERT INTO orders (user_id, status, address, payment_method, total, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, status, address, payment_method, total, created_at))

        order_id = cursor.lastrowid  # Get the ID of the newly created order

        # Insert items into order_items table
        for item in cart_items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, item['product_id'], item['quantity'], item['price']))

        return order_id

###################
# Product Model
###################

class Product:
    def __init__(self, product_id, name, description, price):
        """
        Initialises the product with the given attributes..
        """
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price

    def __repr__(self):
        """
        A string representation of the product object.
        """
        return f"<Product(id={self.product_id}, name={self.name}, price={self.price})>"

    def get_product_details(self):
        """
        Returns the full details of the product.
        """
        return {
            "id": self.product_id,
            "name": self.name,
            "description": self.description,
            "price": self.price
        }

    def update_price(self, new_price):
        self.price = new_price

    def is_in_stock(self, inventory):
        return inventory.get(self.product_id, 0) > 0

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
    def __init__(