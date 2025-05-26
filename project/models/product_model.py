# filepath: project/models/product_model.py
from dataclasses import dataclass

@dataclass
class Product:
    id: str
    name: str
    description: str
    category: str = ""
    price: float = 0.00
    food_rating: float = 0.00
    prep_time: int = 5
    image_url: str = ""
    is_active: bool = True
    restaurant_id: str = 1
    deleted: str = ""
    
    def get_url(self):
        """Return URL to product detail page."""
        return f"/product/{self.id}"