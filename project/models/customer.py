from models.user import User
from models import UserRole
from datetime import datetime

class Customer(User):
    def __init__(self, id=None, name=None, email=None, password=None, 
                 phone=None, address=None):
        # Set the role in the parent constructor
        super().__init__(id, name, email, password, UserRole.CUSTOMER)
        self.phone = phone
        self.address = address
