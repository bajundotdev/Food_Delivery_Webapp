# __init__.py
from flask import Flask
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
    app.config['MYSQL_PASSWORD'] = 'n12333492'     # Your MySQL password
    app.config['MYSQL_DB'] = 'foodah_database'      # Name of the database you created. Change the file name to match your database name.
    
     # Initialize MySQL
    mysql.init_app(app)

    # Register all blueprints
    from .views import register_views
    register_views(app)
    
    return app