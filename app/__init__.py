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
    
    # Database configuration
    database_url = os.environ.get('DATABASE_URL') or 'sqlite:///instance/job_tracker.db'
    
    # Fix for Render's PostgreSQL URL format
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
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
    
    # Create database tables
    with app.app_context():
        try:
            # Ensure the instance directory exists for SQLite
            if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:'):
                instance_path = os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
                if instance_path and not os.path.exists(instance_path):
                    os.makedirs(instance_path, exist_ok=True)
            
            # Create all database tables
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Database initialization warning: {e}")
            # Don't fail app startup if database creation fails initially
            # Tables will be created on first request if needed
    
    return app