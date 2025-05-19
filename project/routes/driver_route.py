from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from project.models import Driver, DriverStatus

# Import dummy database db.py
from db import (get_all_driver)

# Create blueprints for different sections of the application
driver_bp = Blueprint('driver', __name__, url_prefix='/drivers')

# ###################
# # Driver Routes     #
# ###################

@driver_bp.route('/profile')
def profile():
    """Display all drivers."""
    drivers = get_all_driver()
    return render_template('drivers/profile.html', drivers=drivers)

