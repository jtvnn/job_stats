#!/usr/bin/env python3

"""Test database configuration"""

import os
import sys

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

def test_database_config():
    app = create_app()
    
    print("Flask app created successfully")
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Test database connection
    from app import db
    with app.app_context():
        try:
            # Try to query the database
            result = db.engine.execute('SELECT 1')
            print("Database connection successful!")
            
            # Try to create tables
            db.create_all()
            print("Database tables created successfully!")
            
        except Exception as e:
            print(f"Database error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_database_config()