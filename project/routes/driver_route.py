from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from project.models import Driver, DriverStatus

# Import dummy database db.py
from db import (get_all_products, 
                get_product_by_id,
                get_all_restaurants, 
                check_user, 
                add_user,
                get_all_driver)

# Create blueprints for different sections of the application
driver_bp = Blueprint('driver', __name__, url_prefix='/drivers')

##########################
# Session Management     #
##########################

# def is_logged_in():
#     """Check if user is logged in."""
#     return 'user_id' in session

# def get_user_id():
#     """Get the logged-in user's ID."""
#     return session.get('user_id')s

# def get_user_role():
#     """Get the logged-in user's role."""
#     return session.get('user_role')

# def set_user_role(role):
#     """Set the logged-in user's role."""
#     session['user_role'] = role

# def clear_user_session():
#     """Clear user session data."""
#     session.pop('user_id', None)
#     session.pop('user_role', None)


# ###################
# # Driver Routes     #
# ###################

@driver_bp.route('/')
def profile():
    """Display all drivers."""
    drivers = get_all_driver()
    return render_template('drivers/profile.html', drivers=drivers)



# def profile():
#     """View and edit user profile on the same page."""
#     if not is_logged_in():
#         flash('Please log in to view your profile')
#         return redirect(url_for('auth.login'))
        
#     user_id = get_user_id()
#     user = User.get_by_id(user_id)
    
#     if not user:
#         flash('User not found')
#         return redirect(url_for('auth.login'))
    
#     # Get user's recent orders and addresses
#     orders = Order.get_by_user(user_id)
#     addresses = UserAddress.get_by_user(user_id)
    
#     form = UserForm()
    
#     if form.validate_on_submit():
#         user.name = form.name.data
#         user.email = form.email.data
#         # Other fields as needed
#         user.save()
        
#         flash('Profile updated successfully!')
#         return redirect(url_for('user.profile'))
#     elif request.method == 'GET':
#         # Populate form with user data
#         form.name.data = user.name
#         form.email.data = user.email
    
#     return render_template('profile.html', 
#                           user=user,
#                           orders=orders, 
#                           addresses=addresses,
#                           form=form)