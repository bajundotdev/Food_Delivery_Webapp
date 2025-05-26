# filepath: project/models/product_category_model.py
from dataclasses import dataclass

@dataclass
class ProductCategory:
    id: str
    category_name: str
    description: str
    
    def get_url(self):
        """Return URL to product category detail page."""
        return f"/category/{self.id}"