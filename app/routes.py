from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from app import db
from app.models import Application, Company, ApplicationStatus
from app.forms import ApplicationForm, CompanyForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Dashboard with statistics and recent applications"""
    # Get basic statistics
    total_apps = Application.query.count()
    pending_apps = Application.query.filter(
        Application.status.in_([ApplicationStatus.APPLIED, ApplicationStatus.INTERVIEW_SCHEDULED])
    ).count()
    
    # Status breakdown
    status_counts = db.session.query(
        Application.status, func.count(Application.id)
    ).group_by(Application.status).all()
    
    # Recent applications (last 10)
    recent_apps = Application.query.order_by(desc(Application.date_applied)).limit(10).all()
    
    # Applications this week
    week_ago = datetime.now().date() - timedelta(days=7)
    this_week = Application.query.filter(Application.date_applied >= week_ago).count()
    
    return render_template('index.html',
                         total_apps=total_apps,
                         pending_apps=pending_apps,
                         status_counts=status_counts,
                         recent_apps=recent_apps,
                         this_week=this_week)

@main.route('/applications')
def applications():
    """List all applications with filtering"""
    status_filter = request.args.get('status')
    company_filter = request.args.get('company')
    
    query = Application.query
    
    if status_filter:
        query = query.filter(Application.status == status_filter)
    if company_filter:
        query = query.filter(Application.company_name.contains(company_filter))
    
    applications = query.order_by(desc(Application.date_applied)).all()
    statuses = ApplicationStatus.get_all_statuses()
    
    return render_template('applications.html',
                         applications=applications,
                         statuses=statuses,
                         current_status=status_filter,
                         current_company=company_filter)

@main.route('/applications/add', methods=['GET', 'POST'])
def add_application():
    """Add a new job application"""
    form = ApplicationForm()
    
    if form.validate_on_submit():
        # Create or get company
        company = Company.query.filter_by(name=form.company_name.data).first()
        if not company:
            company = Company(name=form.company_name.data)
            db.session.add(company)
            db.session.flush()  # Get the ID
        
        # Create application
        application = Application(
            position=form.position.data,
            company_id=company.id,
            company_name=form.company_name.data,
            status=form.status.data,
            job_link=form.job_link.data,
            salary_range=form.salary_range.data,
            date_applied=form.date_applied.data,
            priority=form.priority.data,
            notes=form.notes.data
        )
        
        db.session.add(application)
        db.session.commit()
        
        flash(f'Application for {form.position.data} at {form.company_name.data} added successfully!', 'success')
        return redirect(url_for('main.applications'))
    
    return render_template('add_application.html', form=form)

@main.route('/applications/<int:id>/edit', methods=['GET', 'POST'])
def edit_application(id):
    """Edit an existing application"""
    application = Application.query.get_or_404(id)
    form = ApplicationForm(obj=application)
    
    if form.validate_on_submit():
        application.position = form.position.data
        application.company_name = form.company_name.data
        application.status = form.status.data
        application.job_link = form.job_link.data
        application.salary_range = form.salary_range.data
        application.date_applied = form.date_applied.data
        application.priority = form.priority.data
        application.notes = form.notes.data
        
        db.session.commit()
        flash('Application updated successfully!', 'success')
        return redirect(url_for('main.applications'))
    
    return render_template('edit_application.html', form=form, application=application)

@main.route('/applications/<int:id>/delete', methods=['POST'])
def delete_application(id):
    """Delete an application"""
    application = Application.query.get_or_404(id)
    db.session.delete(application)
    db.session.commit()
    flash('Application deleted successfully!', 'info')
    return redirect(url_for('main.applications'))

@main.route('/companies')
def companies():
    """List all companies"""
    companies = Company.query.order_by(Company.name).all()
    return render_template('companies.html', companies=companies)

@main.route('/companies/add', methods=['GET', 'POST'])
def add_company():
    """Add a new company"""
    form = CompanyForm()
    
    if form.validate_on_submit():
        company = Company(
            name=form.name.data,
            industry=form.industry.data,
            location=form.location.data,
            website=form.website.data,
            notes=form.notes.data
        )
        
        db.session.add(company)
        db.session.commit()
        
        flash(f'Company {form.name.data} added successfully!', 'success')
        return redirect(url_for('main.companies'))
    
    return render_template('add_company.html', form=form)

@main.route('/companies/delete/<int:id>', methods=['POST'])
def delete_company(id):
    """Delete a company and all associated applications"""
    company = Company.query.get_or_404(id)
    company_name = company.name
    
    # Count applications before deletion for feedback message
    applications_count = len(company.applications)
    
    try:
        # Delete the company (cascade will handle applications)
        db.session.delete(company)
        db.session.commit()
        
        if applications_count > 0:
            flash(f'Company "{company_name}" and {applications_count} associated application(s) deleted successfully!', 'success')
        else:
            flash(f'Company "{company_name}" deleted successfully!', 'success')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting company: {str(e)}', 'error')
    
    return redirect(url_for('main.companies'))

@main.route('/init-db')
def init_database():
    """Initialize database tables - useful for production deployment"""
    try:
        db.create_all()
        flash('Database initialized successfully!', 'success')
    except Exception as e:
        flash(f'Database initialization failed: {str(e)}', 'error')
    
    return redirect(url_for('main.index'))

@main.route('/analytics')
def analytics():
    """Analytics and statistics page"""
    # Status distribution
    status_results = db.session.query(
        Application.status, func.count(Application.id)
    ).group_by(Application.status).all()
    
    # Convert to JSON-serializable format
    status_data = [{"status": row[0], "count": row[1]} for row in status_results]
    
    # Applications over time (last 30 days)
    thirty_days_ago = datetime.now().date() - timedelta(days=30)
    daily_results = db.session.query(
        Application.date_applied, func.count(Application.id)
    ).filter(Application.date_applied >= thirty_days_ago)\
     .group_by(Application.date_applied)\
     .order_by(Application.date_applied).all()
    
    # Convert to JSON-serializable format
    daily_apps = [{"date": row[0].isoformat() if row[0] else None, "count": row[1]} for row in daily_results]
    
    # Top companies by application count
    company_results = db.session.query(
        Application.company_name, func.count(Application.id)
    ).group_by(Application.company_name)\
     .order_by(desc(func.count(Application.id))).limit(10).all()
    
    # Convert to JSON-serializable format
    top_companies = [{"company": row[0], "count": row[1]} for row in company_results]
    
    return render_template('analytics.html',
                         status_data=status_data,
                         daily_apps=daily_apps,
                         top_companies=top_companies)

@main.route('/api/status-update/<int:id>', methods=['POST'])
def update_status(id):
    """API endpoint to quickly update application status"""
    application = Application.query.get_or_404(id)
    new_status = request.json.get('status')
    
    if new_status in ApplicationStatus.get_all_statuses():
        application.status = new_status
        db.session.commit()
        return jsonify({'success': True, 'status': new_status})
    
    return jsonify({'success': False, 'error': 'Invalid status'}), 400