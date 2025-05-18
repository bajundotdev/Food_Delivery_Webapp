# filepath: project/models/product_model.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum

#####################
# Enums             #
#####################

class ProductCategory(Enum):
    MAIN_COURSE = "Main"

@dataclass
class Product:
    id: str
    name: str
    description: str
    category: ProductCategory.MAIN_COURSE
    price: float = 0.00
    food_rating: float = 0.00
    prep_time: int = 5
    image_url: str = ""
    is_active: bool = False
    restaurant_id: str = ""
    
    def get_url(self):
        """Return URL to product detail page."""
        return f"/product/{self.id}"