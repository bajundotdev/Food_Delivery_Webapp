
# models/user.py
from project.models.roles import UserRole
from flask_mysqldb import MySQLdb
from datetime import datetime

class User:
    def __init__(self, id=None, name=None, email=None, password=None, role=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
    
    @staticmethod
    def get_by_id(user_id):
        cursor = MySQLdb.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if not user_data:
            return None
        
        # Create the appropriate user type based on role
        role = user_data.get('role', 'Customer')
        
        if role == UserRole.ADMIN.value:
            from project.models.admin import Admin
            return Admin.create_from_data(user_data)
        elif role == UserRole.RESTAURANT.value:
            from project.models.restaurant import Restaurant
            return Restaurant.create_from_data(user_data)
        elif role == UserRole.DRIVER.value:
            from project.models.driver import Driver
            return Driver.create_from_data(user_data)
        else:
            from project.models.customer import Customer
            return Customer.create_from_data(user_data)
    
    @staticmethod
    def get_by_email(email):
        cursor = MySQLdb.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if not user_data:
            return None
        
        # Return the appropriate user type based on role
        return User.get_by_id(user_data['id'])
    
    def save(self):
        cursor = MySQLdb.connection.cursor()
        
        if self.id:
            # Update
            cursor.execute("""
                UPDATE users 
                SET name = %s, email = %s, password = %s, role = %s
                WHERE id = %s
            """, (
                self.name, 
                self.email, 
                self.password, 
                self.role.value if isinstance(self.role, UserRole) else self.role, 
                self.id
            ))
        else:
            # Create
            cursor.execute("""
                INSERT INTO users (name, email, password, role)
                VALUES (%s, %s, %s, %s)
            """, (
                self.name, 
                self.email, 
                self.password, 
                self.role.value if isinstance(self.role, UserRole) else self.role
            ))
            self.id = cursor.lastrowid
            
        MySQLdb.connection.commit()
        cursor.close()
        return self
