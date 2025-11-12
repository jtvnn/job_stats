from app import create_app

# Create the Flask application instance
application = create_app()

# For Gunicorn - it looks for 'application' by default
app = application

if __name__ == '__main__':
    application.run(debug=True)