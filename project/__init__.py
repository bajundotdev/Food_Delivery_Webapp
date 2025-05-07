# __init__.py
from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    ### Change to the actual database name once saved in the folder
    app.config['MYSQL_HOST'] = 'localhost'        # Database host (usually localhost)
    app.config['MYSQL_USER'] = 'username'         # Your MySQL username
    app.config['MYSQL_PASSWORD'] = 'password'     # Your MySQL password
    app.config['MYSQL_DB'] = 'database_name'      # Name of the database you created. Change the file name to match your database name.
    
     # Initialize MySQL
    mysql.init_app(app)

    # Register all blueprints
    from . import views
    app.register_blueprint(views.main_bp)
    app.register_blueprint(views.user_bp)
    app.register_blueprint(views.auth_bp)
    app.register_blueprint(views.cart_bp)
    app.register_blueprint(views.menu_bp)
    app.register_blueprint(views.order_bp)
    app.register_blueprint(views.admin_bp)
    app.register_blueprint(views.driver_bp)
    
    return app