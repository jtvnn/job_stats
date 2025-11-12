#!/usr/bin/env python3
"""
Database initialization script for production deployment
"""
import os
import sys
from app import create_app, db
from flask_migrate import upgrade, init, migrate as flask_migrate

def init_database():
    """Initialize the database with tables"""
    app = create_app()
    
    with app.app_context():
        try:
            print("Checking if migrations directory exists...")
            if not os.path.exists('migrations'):
                print("Initializing Flask-Migrate...")
                init()
                print("Creating initial migration...")
                flask_migrate(message='Initial migration')
            
            print("Running database migrations...")
            upgrade()
            print("Database initialized successfully!")
            
        except Exception as e:
            print(f"Migration failed: {e}")
            print("Creating tables directly...")
            try:
                db.create_all()
                print("Database tables created successfully!")
            except Exception as e2:
                print(f"Failed to create tables: {e2}")
                sys.exit(1)

if __name__ == "__main__":
    init_database()