from flask import Blueprint, render_template

# Authentication (login/register)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def ():
    return render_template ('')