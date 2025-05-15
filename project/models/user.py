from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Type, TypeVar
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, current_app
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T', bound='User')

@dataclass
class User:
    id: int
    email: str
    password_hash: str
    role: str
    is_active: bool = True
    created_at: datetime = datetime.now()

    # Authentication interface
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return True
    
    def is_active(self) -> bool:
        """Check if user account is active"""
        return self.is_active
    
    def is_anonymous(self) -> bool:
        """Check if user is anonymous (always False for registered users)"""
        return False
    
    def get_id(self) -> str:
        """Get user ID as string (required for session management)"""
        return str(self.id)

    def set_password(self, password: str) -> None:
        """Set password hash from plaintext password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        return check_password_hash(self.password_hash, password)

    @classmethod
    def _create_user(cls, email: str, password_hash: str, role: str) -> Optional[int]:
        """Internal method to create user in database"""
        try:
            with current_app.mysql.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO users (email, password_hash, role, created_at) 
                    VALUES (%s, %s, %s, %s)""",
                    (email, password_hash, role, datetime.now())
                )
                current_app.mysql.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            current_app.mysql.connection.rollback()
            logger.error(f"Error creating user: {e}")
            return None

    @classmethod
    def get_by_id(cls: Type[T], user_id: int) -> Optional[T]:
        """Get user by ID with proper typing"""
        with current_app.mysql.connection.cursor() as cursor:
            cursor.execute(
                """SELECT id, email, password_hash, role, is_active, created_at 
                FROM users WHERE id = %s""",
                (user_id,)
            )
            result = cursor.fetchone()
            return cls._from_db_row(result) if result else None

    @classmethod
    def get_by_email(cls: Type[T], email: str) -> Optional[T]:
        """Get user by email with proper typing"""
        with current_app.mysql.connection.cursor() as cursor:
            cursor.execute(
                """SELECT id, email, password_hash, role, is_active, created_at 
                FROM users WHERE email = %s""",
                (email,)
            )
            result = cursor.fetchone()
            return cls._from_db_row(result) if result else None

    @classmethod
    def _from_db_row(cls: Type[T], row: tuple) -> T:
        """Factory method to create appropriate user subclass from DB row"""
        id, email, password_hash, role, is_active, created_at = row
        user_class = {
            "customer": Customer,
            "driver": Driver,
            "admin": Admin
        }.get(role, cls)
        return user_class(id, email, password_hash, role, is_active, created_at)

    def __post_init__(self):
        """Type conversion for dataclass fields"""
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)


@dataclass
class Customer(User):
    """Customer subclass with shopping cart functionality"""
    
    @classmethod
    def create(cls, email: str, password: str) -> Optional['Customer']:
        """Create new customer with associated cart"""
        password_hash = generate_password_hash(password)
        user_id = cls._create_user(email, password_hash, "customer")
        if not user_id:
            return None

        try:
            with current_app.mysql.connection.cursor() as cursor:
                cursor.execute("INSERT INTO carts (user_id) VALUES (%s)", (user_id,))
                current_app.mysql.connection.commit()
                return cls.get_by_id(user_id)
        except Exception as e:
            current_app.mysql.connection.rollback()
            logger.error(f"Error creating customer cart: {e}")
            return None

    @staticmethod
    def add_to_cart(user_id: int, product_id: int, quantity: int = 1) -> bool:
        """Add product to customer's cart with stock validation"""
        if quantity <= 0:
            return False

        try:
            with current_app.mysql.connection.cursor() as cursor:
                # Verify product stock
                cursor.execute(
                    """SELECT stock FROM products 
                    WHERE id = %s FOR UPDATE""", 
                    (product_id,)
                )
                product = cursor.fetchone()
                if not product or product[0] < quantity:
                    return False

                # Get or create cart
                cursor.execute(
                    "SELECT id FROM carts WHERE user_id = %s FOR UPDATE", 
                    (user_id,)
                )
                cart = cursor.fetchone()
                
                if not cart:
                    cursor.execute(
                        "INSERT INTO carts (user_id) VALUES (%s)", 
                        (user_id,)
                    )
                    cart_id = cursor.lastrowid
                    current_app.mysql.connection.commit()
                else:
                    cart_id = cart[0]

                # Upsert cart item with transaction
                cursor.execute("""
                    INSERT INTO cart_items (cart_id, product_id, quantity)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)
                """, (cart_id, product_id, quantity))
                
                # Update product stock
                cursor.execute(
                    "UPDATE products SET stock = stock - %s WHERE id = %s",
                    (quantity, product_id)
                )
                
                current_app.mysql.connection.commit()
                return True
        except Exception as e:
            current_app.mysql.connection.rollback()
            logger.error(f"Error in cart operation: {e}")
            return False


@dataclass
class Driver(User):
    """Driver subclass with availability checking"""
    
    @classmethod
    def create(cls, email: str, password: str) -> Optional['Driver']:
        """Create new driver"""
        password_hash = generate_password_hash(password)
        user_id = cls._create_user(email, password_hash, "driver")
        return cls.get_by_id(user_id) if user_id else None

    def is_available(self) -> bool:
        """Check if driver is available for new orders"""
        with current_app.mysql.connection.cursor() as cursor:
            cursor.execute("""
                SELECT 1 FROM orders 
                WHERE driver_id = %s AND status IN ('assigned', 'in_transit')
                LIMIT 1
            """, (self.id,))
            return cursor.fetchone() is None


@dataclass
class Admin(User):
    """Admin subclass with elevated privileges"""
    
    @classmethod
    def create(cls, email: str, password: str) -> Optional['Admin']:
        """Create new admin"""
        password_hash = generate_password_hash(password)
        user_id = cls._create_user(email, password_hash, "admin")
        return cls.get_by_id(user_id) if user_id else None