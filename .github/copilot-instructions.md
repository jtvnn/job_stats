<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Job Hunt Statistics Tracker

## Project Overview
This is a job hunt tracking application built with Python backend, SQLite database, and web interface to help track job applications, statistics, and manage job description links.

## Development Guidelines
- Use Python with Flask or FastAPI for the backend
- SQLite for lightweight database storage
- HTML/CSS/JavaScript for the frontend
- Follow clean code practices and proper error handling
- Include comprehensive logging for debugging
- Implement proper data validation and sanitization

## Key Features
- Track job applications with status updates
- Store company information and position details
- Manage links to job descriptions
- Generate analytics and statistics
- Export data functionality
- Search and filter capabilities

## Code Style
- Follow PEP 8 for Python code
- Use descriptive variable and function names
- Include docstrings for functions and classes
- Implement proper exception handling
- Use type hints where appropriate

## Database Schema
- Applications table: id, company, position, status, date_applied, job_link, notes
- Companies table: id, name, industry, location, website
- Statistics tracking for application outcomes

## Testing
- Include unit tests for core functionality
- Test database operations and API endpoints
- Validate form inputs and edge cases