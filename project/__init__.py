from flask import Flask, render_template, session
from flask_bootstrap import Bootstrap5
from flask_mysqldb import MySQL

mysql = MySQL()


#create a function that creates a web application
# a web server will run this web application
def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'BetterSecretNeeded123'

    ### Change to the actual database name once saved in the folder
    app.config['MYSQL_HOST'] = 'localhost'        # Database host (usually localhost)
    app.config['MYSQL_USER'] = 'root'         # Your MySQL username
    app.config['MYSQL_PASSWORD'] = 'n12300136'     # Your MySQL password
    app.config['MYSQL_DB'] = 'foodah_database'      # Name of the database you created. Change the file name to match your database name.
    
     # Initialize MySQL
    mysql.init_app(app)

    # Register all blueprints
    from . import views
    app.register_blueprint(views.main_bp)
    app.register_blueprint(views.user_bp)
    app.register_blueprint(views.auth_bp)
    app.register_blueprint(views.cart_bp)
    app.register_blueprint(views.product_bp)
    app.register_blueprint(views.order_bp)
    app.register_blueprint(views.admin_bp)
    app.register_blueprint(views.driver_bp)
    app.register_blueprint(views.restaurant_bp)
    
    
    from . import session

    return app

