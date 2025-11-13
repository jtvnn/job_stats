from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Database configuration - SQLite only
    database_url = 'sqlite:///job_tracker.db'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Production settings
    if os.environ.get('FLASK_ENV') == 'production':
        app.config['DEBUG'] = False
    else:
        app.config['DEBUG'] = True
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models to register them with SQLAlchemy
    from app.models import Application, Company
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Create database tables when first accessing the database
    # We'll do this lazily to avoid startup errors
    print("Application initialized successfully!")
    
    return app