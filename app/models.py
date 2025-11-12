from datetime import datetime
from app import db

class Company(db.Model):
    """Company model for storing company information"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    industry = db.Column(db.String(100))
    location = db.Column(db.String(100))
    website = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with applications (cascade delete)
    applications = db.relationship('Application', backref='company_ref', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Company {self.name}>'

class Application(db.Model):
    """Application model for tracking job applications"""
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(120), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company_name = db.Column(db.String(120), nullable=False)  # Denormalized for quick access
    status = db.Column(db.String(50), nullable=False, default='Applied')
    job_link = db.Column(db.String(500))
    salary_range = db.Column(db.String(100))
    date_applied = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text)
    priority = db.Column(db.String(20), default='Medium')  # High, Medium, Low
    
    def __repr__(self):
        return f'<Application {self.position} at {self.company_name}>'
    
    @property
    def status_color(self):
        """Return color class for status"""
        colors = {
            'Applied': 'primary',
            'Interview Scheduled': 'info',
            'Interviewed': 'warning',
            'Offer': 'success',
            'Rejected': 'danger',
            'Withdrawn': 'secondary'
        }
        return colors.get(self.status, 'secondary')

class ApplicationStatus:
    """Constants for application statuses"""
    APPLIED = 'Applied'
    INTERVIEW_SCHEDULED = 'Interview Scheduled'
    INTERVIEWED = 'Interviewed'
    OFFER = 'Offer'
    REJECTED = 'Rejected'
    WITHDRAWN = 'Withdrawn'
    
    @classmethod
    def get_all_statuses(cls):
        return [cls.APPLIED, cls.INTERVIEW_SCHEDULED, cls.INTERVIEWED, 
                cls.OFFER, cls.REJECTED, cls.WITHDRAWN]