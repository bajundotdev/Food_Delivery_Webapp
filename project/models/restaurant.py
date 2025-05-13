from models.user import User
from models import UserRole
from datetime import datetime

class Restaurant:
    id: str
    name: str
    address: str
    phone: str
    email: str
    website: str
    description: str
    image_url: str = ""
    
    def get_url(self):
        """Return URL to restaurant detail page."""
        return f"/restaurant/{self.id}"

class Restaurant_Manager(User):
    def __init__(self, id=None, name=None, email=None, password=None, 
                 phone=None, address=None):
        # Set the role in the parent constructor
        super().__init__(id, name, email, password, UserRole.RESTAURANT)
        self.phone = phone
        self.address = address