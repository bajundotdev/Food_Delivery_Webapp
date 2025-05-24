# __init__.py
from flask import Flask
from flask_mysqldb import MySQL
from .routes import all_blueprints
from .routes.error_handlers_route import not_found_error, internal_error

mysql = MySQL()

# create a function that creates a web application
# a web server will run this web application
def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'BetterSecretNeeded123'
    # MySQL configurations
    # Change to the actual database name once saved in the folder
    app.config['MYSQL_HOST'] = 'localhost'        # Database host (usually localhost)
    app.config['MYSQL_USER'] = 'root'         # Your MySQL username
    app.config['MYSQL_PASSWORD'] = 'n12333492'     # Your MySQL password
    app.config['MYSQL_DB'] = 'foodah_database'      # Name of the database you created. Change the file name to match your database name.
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    
    UPLOAD_FOLDER = 'project/static/img/profile_photos'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
     # Initialize MySQL
    mysql.init_app(app)

    # Register all blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)

    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_error)
    
    return app