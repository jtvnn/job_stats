#!/usr/bin/env python3
"""
Test script to verify database connectivity and configuration
"""
import os
from app import create_app, db

def test_database_connection():
    """Test database connection and basic operations"""
    app = create_app()
    
    with app.app_context():
        try:
            print(f"Testing database connection...")
            print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Test connection
            result = db.engine.execute("SELECT 1")
            print("✅ Database connection successful!")
            
            # Test table creation
            db.create_all()
            print("✅ Database tables created/verified successfully!")
            
            # Test basic query
            from app.models import Company, Application
            company_count = Company.query.count()
            application_count = Application.query.count()
            
            print(f"✅ Database query successful!")
            print(f"   - Companies: {company_count}")
            print(f"   - Applications: {application_count}")
            
            return True
            
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            return False

if __name__ == "__main__":
    success = test_database_connection()
    exit(0 if success else 1)