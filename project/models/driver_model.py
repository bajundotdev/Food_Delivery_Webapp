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

@dataclass
class Driver:
    id: str
    user_id: str
    vehicle_type: str
    license_number: str
    vehicle_plate: str
    is_available: DriverStatus
    driver_rating: float
    total_deliveries: int
    
    def get_url(self):
        """Return URL to driver detail page."""
        return f"/drivers/{self.id}"
    
    def assign_to_order(self, order_id: str):
        """Assign driver to an order."""
        # Implementation needed
        pass

    