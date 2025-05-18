# filepath: project/models/user_model.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum

#####################
# Enums             #
#####################

class UserRole(Enum):
    CUSTOMER = "Customer"
    ADMIN = "Admin"
    DRIVER = "Delivery Driver"
    RESTAURANTOWNER = "Restaurant Manager"

###################
# User Models
###################

@dataclass
class User:
    id: str
    name: str
    email: str
    phone: str
    password: str
    profile_picture_url: str = ""
    role: UserRole = UserRole.CUSTOMER
    
    def get_url(self):
        """Return URL to user profile."""
        return f"/user/profile/{self.id}"
    
    def is_admin(self):
        """Check if user has admin role."""
        return self.role == UserRole.ADMIN