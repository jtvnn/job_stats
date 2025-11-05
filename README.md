# Job Hunt Statistics Tracker

A comprehensive web application for tracking job applications, managing company information, and analyzing job search statistics.

## Features

- **Application Tracking**: Record and manage job applications with detailed information
- **Company Management**: Store company details and track applications per company
- **Status Management**: Track application progress through different stages
- **Analytics Dashboard**: Visualize application statistics and trends
- **Link Management**: Store and access job description links
- **Priority Tracking**: Set priority levels for applications
- **Export Functionality**: Export data for external analysis

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript with Bootstrap 5
- **Charts**: Chart.js for data visualization
- **Forms**: Flask-WTF for form handling

## Prerequisites

Before running this application, ensure you have:

1. **Python 3.7 or higher** installed on your system
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version` or `python3 --version`

2. **pip** (Python package installer) - usually comes with Python
   - Verify installation: `pip --version`

## Installation & Setup

### Quick Start (Recommended)

1. **Open the project** in VS Code or your preferred editor

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   - Open your web browser
   - Navigate to `http://localhost:5000`

### Using Virtual Environment (Best Practice)

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

### Using VS Code Tasks

This project includes pre-configured VS Code tasks:

1. **Install Dependencies**: `Ctrl+Shift+P` → "Tasks: Run Task" → "Install Dependencies"
2. **Run Application**: `Ctrl+Shift+P` → "Tasks: Run Task" → "Run Application"

### First Time Setup

When you first run the application:
- The SQLite database will be automatically created in the `instance/` directory
- Database tables will be initialized automatically
- You can immediately start adding companies and applications

The application will be available at `http://localhost:5000`

## Usage

### Adding Applications
1. Navigate to "Applications" → "Add Application"
2. Fill in job details including position, company, status, and job link
3. Set priority and add notes as needed

### Managing Companies
1. Go to "Companies" to view all tracked companies
2. Add new companies with industry and location information
3. Track multiple applications per company

### Viewing Analytics
1. Visit the "Analytics" page for insights
2. View status distribution charts
3. Analyze application trends over time
4. Review success rates and statistics

### Status Updates
- Quickly update application statuses from the applications list
- Track progress from "Applied" through "Interview" to "Offer"

## Database Schema

### Applications Table
- `id`: Primary key
- `position`: Job position title
- `company_id`: Foreign key to companies table
- `company_name`: Company name (denormalized)
- `status`: Application status
- `job_link`: URL to job description
- `salary_range`: Expected salary range
- `date_applied`: Date application was submitted
- `priority`: Priority level (High/Medium/Low)
- `notes`: Additional notes

### Companies Table
- `id`: Primary key
- `name`: Company name
- `industry`: Industry sector
- `location`: Company location
- `website`: Company website URL
- `notes`: Company notes

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
export FLASK_APP=app.py
flask run
```

### Database Migrations
```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

### Running Tests
```bash
python -m pytest tests/
```

## Troubleshooting

### Common Issues

1. **Python not found error**:
   - Ensure Python is installed and added to your system PATH
   - Try using `python3` instead of `python`
   - On Windows, you may need to use `py` instead of `python`

2. **Port 5000 already in use**:
   - Change the port in `app.py`: `app.run(debug=True, port=5001)`
   - Or stop other services using port 5000

3. **Database errors**:
   - Delete the `instance/` directory and restart the app to recreate the database
   - Check file permissions in the project directory

4. **Missing dependencies**:
   - Run `pip install -r requirements.txt` again
   - Ensure you're in the correct project directory
   - Try using a virtual environment

5. **VS Code tasks not working**:
   - Ensure you have the Python extension installed in VS Code
   - Check that your Python interpreter is correctly selected
   - Use `Ctrl+Shift+P` → "Python: Select Interpreter"

### Getting Help

- Check the terminal output for specific error messages
- Ensure all project files are present
- Verify Python and pip are properly installed
- Try running in a virtual environment to isolate dependencies

## Configuration

The application uses the following environment variables:

- `FLASK_APP`: Application entry point (app.py)
- `FLASK_ENV`: Environment mode (development/production)
- `SECRET_KEY`: Secret key for session security
- `DATABASE_URL`: Database connection string

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please open an issue in the repository.