# Assignment_2

Flask-based food delivery application for IFN582 group assignment

## Project Overview

This Flask application implements a web-based platform for e-commerce or food delivery services, with features for user management, products, orders, stores, and more.

## Application Structure

The application follows a modular architecture using Flask blueprints, with clear separation between models, views, and controllers:

```bash
A2_Group72_582_A2.zip
├── requirements.txt
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
    │   ├── auth/
    │   ├── driver/
    │   ├── errors/
    │   ├── products/ 
    │   ├── user/ 
    │   ├── base.html
    │   └── index.html 
    ├── __init__.py
    ├── database.sql (pre-populated)
    ├── db.py
    ├── decorators.py
    ├── session.py
    └── views.py
```

## System Prerequisites

1. Python 3.8+
2. MySQL Server
3. MySQL Workbench

## How to Run the Project

1. **Install MySQL Workbench:**

   Download and install MySQL Workbench from the [official MySQL website](https://dev.mysql.com/downloads/workbench/).

2. **Configure MySQL Workbench:**

   - Open MySQL Workbench and create a new connection to your MySQL Server.
   - Use MySQL Workbench to import the pre-populated database schema:
     - Go to `Server` > `Data Import`.
     - Select "Import from Self-Contained File" and choose your `database.sql` file.
     - Select the target schema (e.g., `foodah_database`).
     - Click `Start Import`.

3. **(Optional) Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies:**

   Make sure to install the required libraries using the requirements.txt file

   ```bash
   # On Windows
   python -m pip install -r requirements.txt

   # On MacOS
   python3 -m pip install -r requirements.txt
   ```

5. **Configure MySQL Connection:**

   Update the MySQL configuration in `project` > `__init__.py` with your MySQL credentials:

   ```bash
   app.config['MYSQL_USER'] = 'your_mysql_username'
   app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
   ```

6. **Run the application:**

   ```bash
   python3 run.py
   ```

   The app will be available at [http://127.0.0.1:8888](http://127.0.0.1:8888).

## User Credentials

   Use the following user accounts to login:

1. Log in as **System Admin**:

   ```bash
   Email Address: admin@foodah.com
   Password: hello 
   ```

2. Log in as **Customer**:

   ```bash
   Email Address: jamizan@foodah.com
   Password: hello 
   ```

3. Log in as **Delivery Driver**:

   ```bash
   Email Address: tomasen@foodah.com
   Password: hello 
   ```

## Notes

- The database is pre-populated using `project` > `database.sql`. If you need to reset the database, you can re-import this file into your database system.
- For any issues, refer to the `README.txt`.
