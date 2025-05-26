# filepath: project/models/driver_model.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum

#####################
# Enums             #
#####################

class DriverStatus(Enum):
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"
    EN_ROUTE = "En Route"
    OFFLINE = "Offline"

@dataclass
class Driver:
    id: str
    user_id: str
    vehicle_type: str
    license_number: str
    vehicle_plate: str
    driver_rating: float
    total_deliveries: int
    fullname: str
    email: str
    phone_number: str
    profile_picture_url: str
    is_active: bool
    status: DriverStatus = DriverStatus.AVAILABLE

    def get_url(self):
        """Return URL to driver detail page."""
        return f"/drivers/{self.id}"
    
    def assign_to_order(self, order_id: str):
        """Assign driver to an order."""
        # Implementation needed
        pass

    