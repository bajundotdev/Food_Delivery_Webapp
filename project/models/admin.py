# models/admin.py
# project/models/admin.py
from project.models.roles import UserRole  # No circular import now
from project.models.user import User
from flask_mysqldb import MySQLdb
from datetime import datetime

class Admin(User):
    def __init__(self, id=None, name=None, email=None, password=None, is_super_admin=False):
        super().__init__(id, name, email, password, UserRole.ADMIN)
        self.is_super_admin = is_super_admin
    
    def save(self):
        # First save the base user
        super().save()
        
        # Then save admin-specific fields
        cursor = MySQLdb.connection.cursor()
        
        cursor.execute("""
            INSERT INTO admin_details (user_id, is_super_admin)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE is_super_admin = VALUES(is_super_admin)
        """, (self.id, self.is_super_admin))
        
        MySQLdb.connection.commit()
        cursor.close()
        return self
    
    @staticmethod
    def create_from_data(user_data):
        """Create Admin from database row."""
        # Get admin-specific data
        cursor = MySQLdb.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin_details WHERE user_id = %s", (user_data['id'],))
        admin_data = cursor.fetchone() or {}
        cursor.close()
        
        admin = Admin(
            id=user_data['id'],
            name=user_data['name'],
            email=user_data['email'],
            password=user_data['password'],
            is_super_admin=admin_data.get('is_super_admin', False)
        )
        
        return admin
    
    def log_action(self, action, entity_type, entity_id, details=""):
        """Log an admin action for audit trail."""
        cursor = MySQLdb.connection.cursor()
        
        cursor.execute("""
            INSERT INTO admin_logs (admin_id, action, entity_type, entity_id, details, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            self.id, action, entity_type, entity_id, details, datetime.now()
        ))
        
        MySQLdb.connection.commit()
        cursor.close()
