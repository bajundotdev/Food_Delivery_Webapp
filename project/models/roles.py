# project/models/roles.py
from enum import Enum

class UserRole(Enum):
    CUSTOMER = "Customer"
    ADMIN = "Admin" 
    DRIVER = "Driver"
    RESTAURANT = "Restaurant Manager"
