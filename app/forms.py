from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, URLField
from wtforms.validators import DataRequired, Optional, URL, Length
from datetime import date
from app.models import ApplicationStatus

class ApplicationForm(FlaskForm):
    """Form for adding/editing job applications"""
    position = StringField('Position', validators=[DataRequired(), Length(max=120)])
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=120)])
    status = SelectField('Status', choices=[(status, status) for status in ApplicationStatus.get_all_statuses()],
                        default=ApplicationStatus.APPLIED)
    job_link = URLField('Job Link', validators=[Optional(), URL()])
    salary_range = StringField('Salary Range', validators=[Optional(), Length(max=100)])
    date_applied = DateField('Date Applied', validators=[DataRequired()], default=date.today)
    priority = SelectField('Priority', choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')],
                          default='Medium')
    notes = TextAreaField('Notes', validators=[Optional()])

class CompanyForm(FlaskForm):
    """Form for adding/editing companies"""
    name = StringField('Company Name', validators=[DataRequired(), Length(max=120)])
    industry = StringField('Industry', validators=[Optional(), Length(max=100)])
    location = StringField('Location', validators=[Optional(), Length(max=100)])
    website = URLField('Website', validators=[Optional(), URL()])
    notes = TextAreaField('Notes', validators=[Optional()])