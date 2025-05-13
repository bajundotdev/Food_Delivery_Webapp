from datetime import datetime

class UserAddress:
    def __init__(self, id, user_id, street, city, state, postal_code, country,
                 created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.street = street
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def get_url(self):
        return f"/user/address/{self.id}"
        
    def full_address(self):
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
        
        return ", ".join(p.strip() for p in parts if p and p.strip())

    def __str__(self):
        return f"Address({self.full_address()})"
