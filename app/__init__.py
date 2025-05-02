from flask import Flask, render_template
from flask_mysqldb import MySQL
from forms import forms
from routes import blueprints
from models import db

def create_app():
    # Create Flask app instance
    app = Flask(__name__)
    
    # Register blueprints from app.route
    for bp in blueprints:
        app.register_blueprint(bp)

    mysql = MySQL(app)
    return app
