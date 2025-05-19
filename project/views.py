# views.py
from .routes import all_blueprints

def register_views(app):
    for bp in all_blueprints:
        app.register_blueprint(bp)