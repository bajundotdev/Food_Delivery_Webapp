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
    is_active: bool = True
    last_login: str = ""
    
    def get_url(self):
        """Return URL to user profile."""
        return f"/user/profile/{self.id}"
    
    def is_admin(self):
        """Check if user has admin role."""
        return self.role == UserRole.ADMIN

@dataclass
class UserAddress:
    id: str
    user_id: str
    address_line1: str
    address_line2: str
    city: str
    state: str
    postal_code: str
    country: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def get_url(self):
        """Return URL to edit address page."""
        return f"/user/address/{self.id}"
        
    def full_address(self):
        """Return formatted full address string."""
        parts = [self.street]
        if self.city and self.state:
            parts.append(f"{self.city}, {self.state}")
        elif self.city:
            parts.append(self.city)
        elif self.state:
            parts.append(self.state)
        
        if self.postal_code:
            parts.append(self.postal_code)
        
        if self.country:
            parts.append(self.country)
        
        return ", ".join(parts)

#####################
# Search Models     #
#####################
@dataclass
class SearchResult:
    type: str  # 'product', 'restaurant', etc.
    item: object  # The actual object (Product, Restaurant, etc.)

@dataclass
class Search:
    query: str
    user_id: str
    results: List[SearchResult] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    @staticmethod
    def search_all(query: str):
        """Search across all relevant entities."""
        # Implementation needed
        pass