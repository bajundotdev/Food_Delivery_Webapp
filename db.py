# dummyDb.py
from project.models import Product, ProductCategory, Restaurant, DriverVehicle
from datetime import datetime
from typing import List
from enum import Enum

# Dummy data
# users = [
#     User(1, "Alice", "alice@example.com"),
#     User(2, "Bob", "bob@example.com"),
#     User(3, "Charlie", "charlie@example.com"),
# ]

################## 
# ENUMS
################## 
class ProductCategory(Enum):
    MAIN_COURSE = "Main Course"



# DriverVehicle
driver_vehicles = [
    DriverVehicle(1, "vehicle 1", "JB2345"),
    DriverVehicle(2, "vehicle 2", "AD6789"),
    DriverVehicle(3, "vehicle 3", "NJ4123")
]

def get_all_vehicles():
    return driver_vehicles

products = [
    Product("1", "Pizza", "Delicious cheese pizza", ProductCategory.MAIN_COURSE, "101", 12.99, "https://example.com/pizza.jpg"),
    Product("2", "Burger", "Juicy beef burger", ProductCategory.MAIN_COURSE, "102", 9.99, "https://example.com/burger.jpg"),
    Product("3", "Pizza", "Delicious cheese pizza", ProductCategory.MAIN_COURSE, "101", 12.99, "https://example.com/pizza.jpg"),
    Product("4", "Burger", "Juicy beef burger", ProductCategory.MAIN_COURSE, "102", 9.99, "https://example.com/burger.jpg"),
]

restaurants = [
    Restaurant("101", "Pizza Palace", "123 Main St", "1234567", "test@email.com", "www.google.com","This is a sample description", "https://example.com/pizzapalace.jpg"),
    Restaurant("102", "Burger Barn", "456 Elm St", "1234567", "test@email.com", "www.google.com","This is a sample description",  "https://example.com/burgerbarn.jpg"),
    Restaurant("103", "Taco Town", "789 Oak St", "1234567", "test@email.com", "www.google.com","This is a sample description",  "https://example.com/tacotown.jpg"),
]

# Simulated query functions
# def get_all_users():
#     return users

# def get_user_by_id(user_id):
#     return next((user for user in users if user.id == user_id), None)

def get_all_products():
    return products

def get_all_restaurants():
    return restaurants

# def get_product_by_id(product_id):
#     return next((product for product in products if product.id == product_id), None)

