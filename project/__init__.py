# Use of :file:`__init__.py` is resolved in each folder to form as the python package
from flask import Flask
from flask_mysqldb import MySQL
from .routes import all_blueprints
from .routes.error_handlers_route import error_bp
import logging

mysql = MySQL()

# create a function that creates a web application
# a web server will run this web application
def create_app():
    """
    Creation of flask application and acts as the main object.
    Name of module is passed of the application.
    Acts as the central registry of view functions, URL rules, template and database configuration.
    """
    
    app = Flask(__name__)

    # Session configurations
    app.config['SECRET_KEY'] = 'BetterSecretNeeded123' # Needed for sessions
    app.config['SESSION_COOKIE_SECURE'] = False #Change to true after development
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

    app.debug = True # False in production
            
    # MySQL configurations
    # Change to the actual database name once saved in the folder
    app.config['MYSQL_HOST'] = 'localhost'        # Database host (usually localhost)
    app.config['MYSQL_USER'] = 'root'         # Your MySQL username
    app.config['MYSQL_PASSWORD'] = 'n12333492'     # Your MySQL password
    app.config['MYSQL_DB'] = 'foodah_database'      # Name of the database you created. Change the file name to match your database name.
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

     # Initialize MySQL
    mysql.init_app(app)

    # Register all blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)
    
    # Register error blueprint
    app.register_blueprint(error_bp)

    # Debug route for development to check routes
    if app.debug:
        @app.route('/debug/routes/')
        def debug_routes():
            routes = []
            for rule in app.url_map.iter_rules():
                if not rule.rule.startswith('/static'):
                    routes.append(f"{rule.rule} to {rule.endpoint}")
                return "<br>".join(routes)
    
    return app