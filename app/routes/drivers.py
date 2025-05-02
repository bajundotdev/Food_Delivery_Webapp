from flask import Blueprint, render_template

# Shopping Cart Management
drivers_bp = Blueprint('drivers', __name__, url_prefix='/drivers')

@drivers_bp.route('/')
def index():
    return render_template ('')