from flask import Blueprint, render_template, request, url_for, session

# Create a Blueprint for user routes
users_bp = Blueprint('users', __name__, url_prefix='/account')

@users_bp.route('/')
@login_required

def profile():

def edit_profile():
    """Edit user profile"""

    if request.method == 'POST':
        #Update basic profile information
        user.name = request.form.get('name')

        #Check if email exists
        new_email = request.form.get('email')