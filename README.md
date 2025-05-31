
# Assignment_2

Foodah!—A Food Delivery Service Web Application

The socially aware web app Foodah! revolutionises food delivery by combining technology with morality. The app delivers freshly prepared meals from partner restaurants to clients' doorsteps. The goal is to make food ordering and delivery quick, easy, and culturally sensitive.

Students, families, busy professionals, and city and semi-urban residents who need easy dining access were the app's target audience. Restaurants benefit from using the platform to increase client base and order fulfilment. Foodah! follows the AIATSIS Code of Ethics by respecting cultural diversity and welcoming all. This means the site respects and values users' cultural identities and promote the equitable promotion of local companies, particularly Indigenous food enterprises.

Foodah! has several useful features. From the landing page, users can browse personally featured restaurants and culinary items. They can also use advanced search and filter options to find foods they like. They can view ingredients, prices, and customer reviews for each food item. The delivery request summary page lets them see their cart items, while the checkout page lets customers finalise their purchases and choose a delivery option. The interface is dynamic, user-friendly, and built for different technical levels.

Unique, value-driven features set Foodah! apart from other delivery systems. Initially, the platform allows fast delivery of nearby objects. The meals will arrive hot and fresh in 30 minutes, guaranteed. Second, it promotes electric scooters and bicycles for delivery, which minimises carbon emissions and supports green practices. Foodah!'s AI-powered meal recommendations match users' preferences, diets, and seasonal specials to improve their experience. The suggestions are carefully crafted to avoid generalising or misrepresenting cultural dishes.

Foodah! goes beyond delivery. Community participation, social responsibility, and innovation were the goals of this platform. It delivers meals and fulfils digital obligations, representation, and respect.

## Project Overview

This Flask application implements a web-based platform for e-commerce or food delivery services, with features for user management, products, orders, stores, and more.

## Application Structure

The application follows a modular architecture using Flask blueprints, with clear separation between models, views, and controllers:

```bash
A2_Group_72_582_A2.zip
├── requirements.txt
├── run.py
├── README.txt (brief setup instructions) 
└── project/
    ├── forms/
    ├── models/
    ├── static/
    │   ├── css/
    │   └── img/
    ├── templates/
    │   ├── admin/
    │   ├── auth/
    │   ├── driver/
    │   ├── errors/
    │   ├── products/ 
    │   ├── user/ 
    │   ├── base.html
    │   └── index.html 
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
   source venv/bin/activate  # On Windows: venv\Scripts\activate
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
   Password: helloworld
```

2. Log in as **Customer**:

```bash
   Email Address: jamizan@foodah.com
   Password: helloworld
```

3. Log in as **Delivery Driver**:

```bash
   Email Address: tomasen@foodah.com
   Password: hello
```

## Notes

- The database is pre-populated using `project` > `database.sql`. If you need to reset the database, you can re-import this file into your database system.
- For any issues, refer to the `README.txt`.