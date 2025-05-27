# __init__.py
from flask import Flask
from flask_mysqldb import MySQL
from .routes import all_blueprints
from .routes.error_handlers_route import not_found_error, internal_error
from .session import init_session
import logging

mysql = MySQL()

# create a function that creates a web application
# a web server will run this web application
def create_app():
    app = Flask(__name__)
    app.secret_key = 'BetterSecretNeeded123'
    # MySQL configurations
    # Change to the actual database name once saved in the folder
    app.config['MYSQL_HOST'] = 'localhost'        # Database host (usually localhost)
    app.config['MYSQL_USER'] = 'root'         # Your MySQL username
    app.config['MYSQL_PASSWORD'] = 'n12333492'     # Your MySQL password
    app.config['MYSQL_DB'] = 'foodah_database'      # Name of the database you created. Change the file name to match your database name.
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    
    UPLOAD_FOLDER = 'project/static/img/'

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Application created successfully.")
    
    # Initialize MySQL
    mysql.init_app(app)

    # Initialize session
    @app.before_request
    def setup_session():
        init_session()
        
    # Register all blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)
    
    # Register error handlers
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_error)
    
    # Print all routes for debugging
    print("\nAvailable Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} -> {rule.endpoint}")
    print()
    
    # Return the Flask application instance
    return app