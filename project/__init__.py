from flask import Flask
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap5
from datetime import timedelta

mysql = MySQL()
bootstrap = Bootstrap5()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'BetterSecretNeeded123'
    mysql.init_app(app) 
    bootstrap.init_app(app)

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'username'
    app.config['MYSQL_PASSWORD'] = 'password'
    app.config['MYSQL_DB'] = 'database_name'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
    
    # Import views and blueprints here to avoid circular import issues
    from .views import (
        main_bp, user_bp, auth_bp, cart_bp, product_bp,
        order_bp, admin_bp, driver_bp, restaurant_bp
    )

    # Register blueprints
    app.register_blueprint(views.main_bp)
    app.register_blueprint(views.user_bp)
    app.register_blueprint(views.auth_bp)
    app.register_blueprint(views.cart_bp)
    app.register_blueprint(views.product_bp)
    app.register_blueprint(views.order_bp)
    app.register_blueprint(views.admin_bp)
    app.register_blueprint(views.driver_bp)
    app.register_blueprint(views.restaurant_bp)

    return app
