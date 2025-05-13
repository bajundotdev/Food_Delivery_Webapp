class Product:
    def __init__(self, id, name, description, category, restaurant_id, price=0.0, image_url=""):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.restaurant_id = restaurant_id
        self.price = price
        self.image_url = image_url

    def get_url(self):
        return f"/product/{self.id}"
    