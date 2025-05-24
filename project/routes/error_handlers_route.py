from flask import Blueprint, render_template, request, session, flash
import logging

error_bp = Blueprint('error_bp', __name__)

@error_bp.app_errorhandler(404)
def not_found_error(error):
    """Handle 404 Not Found errors."""
    logging.warning(f"404 error: {request.url} not found")
    flash("The page you're looking for doesn't exist.", "error")
    user_info = session.get('user', {})
    return render_template('errors/404.html', error=error, user=user_info), 404

@error_bp.app_errorhandler(403)
def forbidden_error(error):
    """Handle 403 Forbidden errors."""
    logging.warning(f"403 error: Access forbidden to {request.url}")
    flash("You don't have permission to access this page.", "error")
    user_info = session.get('user', {})
    return render_template('errors/403.html', error=error, user=user_info), 403

@error_bp.app_errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors."""
    logging.error(f"500 error: {str(error)}")
    flash("Something went wrong on our end. Please try again later.", "error")
    user_info = session.get('user', {})
    return render_template('errors/500.html', error=error, user=user_info), 500