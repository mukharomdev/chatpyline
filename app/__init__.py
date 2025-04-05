from flask import Flask
from flask_migrate import Migrate
from .config import Config
from .extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    Migrate(app, db)
    # Initialize extensions
    db.init_app(app)
    # Create tables
    with app.app_context():
        db.create_all()
    # Register blueprints
    from app.handlers.webhook_handler import webhook_bp
    app.register_blueprint(webhook_bp)
    
    return app


__all__ = ['create_app']