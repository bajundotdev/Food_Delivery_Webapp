from flask import Flask, render_template

def create_app():
    # Create Flask app instance
    app = Flask(__name__)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.cart import cart_bp
    from app.routes.orders import orders_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)

    return app
    