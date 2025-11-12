#!/bin/bash

# Database initialization script for Render deployment

echo "Starting database initialization..."

# Install dependencies
pip install -r requirements.txt

# Initialize Flask-Migrate if not already done
if [ ! -d "migrations" ]; then
    echo "Initializing Flask-Migrate..."
    python -c "
from app import create_app, db
from flask_migrate import init
import os

app = create_app()
with app.app_context():
    if not os.path.exists('migrations'):
        init()
        print('Flask-Migrate initialized')
    else:
        print('Flask-Migrate already initialized')
"
fi

# Run database migrations
echo "Running database migrations..."
python -c "
from app import create_app, db
from flask_migrate import upgrade
import os

app = create_app()
with app.app_context():
    try:
        # Try to run migrations
        upgrade()
        print('Database migrations completed successfully')
    except Exception as e:
        print(f'Migration failed, creating tables directly: {e}')
        # If migrations fail, create tables directly
        db.create_all()
        print('Database tables created successfully')
"

echo "Database initialization completed!"