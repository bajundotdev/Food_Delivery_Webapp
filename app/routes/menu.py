from flask import Blueprint, render_template

# Blueprint(plural)
menu_bp = Blueprint('menus', __name__, url_prefix='menu')

@menu_bp.route('/menu')
def index():
    return render_template ('menu.html')