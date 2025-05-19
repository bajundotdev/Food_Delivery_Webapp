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

#####################
# Driver Models     #
#####################

@dataclass
class Driver:
    id: str
    user_id: str
    phone: str
    status: DriverStatus = DriverStatus.AVAILABLE
    
    def get_url(self):
        """Return URL to driver detail page."""
        return f"/driver/{self.id}"
    
    def assign_to_order(self, order_id: str):
        """Assign driver to an order."""
        # Implementation needed
        pass

@dataclass
class DriverVehicle:
    id: int
    name: str
    plate_number: str

    def get_url(self):
        """Return URL to driver vehicle."""
        return f"/driver/vehicle"
