# Assignment_2

Flask-based food delivery application for IFN582 group assignment

## Project Overview

This Flask application implements a web-based platform for e-commerce or food delivery services, with features for user management, products, orders, stores, and more.

## Application Structure

The application follows a modular architecture using Flask blueprints, with clear separation between models, views, and controllers:

```bash
A2_Group_72_582_A2.zip
├── run.py
├── README.txt (brief setup instructions) 
└── project/
    ├── forms/
    ├── models/
    ├── static/
    │   ├── css/
    │   └── img/
    ├── templates/
    │   ├── admin/
    │   │   ├── manage_products.html
    │   │   ├── manage_category.html
    │   │   ├── manage_orders.html
    │   │   ├── manage_customers.html
    │   ├── drivers/
    │   │   ├── profile.html
    │   ├── errors/
    │   ├── login/
    │   ├── products/ 
    │   ├── registration/
    │   └── users/
    │       ├── profile.html
    ├── views/
    ├── __init__.py
    ├── database.sql (pre-populated)
    └── db.py
```

## How to Run the Project

1. **(Optional) Create and activate a virtual environment:**

   ```bash
   python -m venv venv # On MacOS: python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   Make sure to install the required libraries using the requirements.txt file

   ```bash
   python -m pip install -r requirements.txt
   python3 -m pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   python3 run.py
   ```

   The app will be available at [http://127.0.0.1](http://127.0.0.1).

## Notes

- Make sure you have Python 3.8+ installed.
- The database is pre-populated using `database.sql`. If you need to reset the database, you can re-import this file into your database system.
- For any issues, refer to the `README.txt`.
