from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum

###################
# Restaurant Models
###################
@dataclass
class Restaurant:
    id: str
    owner_id: str
    name: str
    is_indigenous: bool
    address: str
    is_active: bool
    phone: str
    email: str
    website: str
    description: str
    image_url: str = ""
    
    def get_url(self):
        """Return URL to restaurant detail page."""
        return f"/restaurant/{self.id}"