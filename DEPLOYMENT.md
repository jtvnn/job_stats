# Deployment Guide - Job Hunt Tracker

## PostgreSQL + Render Deployment

This guide will help you deploy your Job Hunt Tracker to Render with a PostgreSQL database.

### Prerequisites

- GitHub account with your code pushed to a repository
- Render account (sign up at https://render.com)

### Step 1: Prepare Your Repository

Ensure your repository contains these files:
- `requirements.txt` (updated with PostgreSQL support)
- `render.yaml` (Render configuration)
- `runtime.txt` (Python version specification)
- `init_db.py` (Database initialization script)
- `Procfile` (Alternative deployment configuration)

### Step 2: Deploy to Render

#### Option A: Using render.yaml (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add PostgreSQL and Render support"
   git push origin main
   ```

2. **Connect to Render**:
   - Go to https://render.com/dashboard
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository containing your Job Hunt Tracker
   - Render will automatically detect the `render.yaml` file

3. **Deploy**:
   - Review the services that will be created:
     - Web service (your Flask app)
     - PostgreSQL database
   - Click "Apply"
   - Wait for deployment to complete (5-10 minutes)

#### Option B: Manual Setup

1. **Create PostgreSQL Database**:
   - Go to Render Dashboard → "New +" → "PostgreSQL"
   - Database Name: `job-tracker-db`
   - User: `job_tracker_user`
   - Region: Choose closest to your users
   - Click "Create Database"
   - Note the connection details

2. **Create Web Service**:
   - Go to Render Dashboard → "New +" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - Name: `job-hunt-tracker`
     - Runtime: Python 3
     - Build Command: `pip install -r requirements.txt && python init_db.py`
     - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

3. **Configure Environment Variables**:
   - Add these environment variables in your web service:
     - `FLASK_ENV`: `production`
     - `SECRET_KEY`: Generate a secure random key
     - `DATABASE_URL`: Copy from your PostgreSQL database connection string

### Step 3: Verify Deployment

1. **Check Service Status**:
   - Both services should show "Live" status
   - Web service should have a URL (e.g., https://job-hunt-tracker-xxx.onrender.com)

2. **Test the Application**:
   - Visit your web service URL
   - Try adding a company
   - Try adding a job application
   - Check the analytics page

3. **Monitor Logs**:
   - Click on your web service → "Logs"
   - Look for any errors or warnings
   - Database initialization logs should show successful table creation

### Step 4: Post-Deployment Configuration

#### Database Management

- **Access Database**: Use the connection details from Render to connect with tools like pgAdmin or DBeaver
- **Backups**: Render automatically backs up PostgreSQL databases
- **Monitoring**: Use Render's monitoring tools to track performance

#### Custom Domain (Optional)

1. Go to your web service settings
2. Add your custom domain
3. Configure DNS settings as instructed by Render

### Troubleshooting

#### Common Issues:

1. **Build Failed**:
   - Check that `requirements.txt` is valid
   - Ensure Python version in `runtime.txt` is supported
   - Review build logs for specific error messages

2. **Database Connection Error**:
   - Verify `DATABASE_URL` environment variable is set correctly
   - Check PostgreSQL service is running
   - Ensure database initialization script ran successfully

3. **Application Won't Start**:
   - Check that gunicorn is in requirements.txt
   - Verify the start command is correct
   - Review application logs for Python errors

4. **Static Files Not Loading**:
   - Ensure Flask is serving static files correctly
   - Check browser console for 404 errors
   - Verify static file paths in templates

### Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `production` |
| `SECRET_KEY` | Flask secret key | `your-super-secure-secret-key` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:port/db` |

### Local Development with PostgreSQL

To test PostgreSQL locally before deployment:

1. **Install PostgreSQL** locally
2. **Create a database**:
   ```sql
   CREATE DATABASE job_tracker;
   CREATE USER job_tracker_user WITH ENCRYPTED PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE job_tracker TO job_tracker_user;
   ```
3. **Update .env file**:
   ```
   DATABASE_URL=postgresql://job_tracker_user:your_password@localhost/job_tracker
   ```
4. **Run migrations**:
   ```bash
   python init_db.py
   python app.py
   ```

### Maintenance

- **Monitor Performance**: Use Render's metrics dashboard
- **Scale if Needed**: Upgrade your service plan for more resources
- **Update Dependencies**: Regularly update requirements.txt
- **Database Maintenance**: Monitor database size and performance

### Cost Considerations

- **Free Tier**: Render offers free tier for web services and PostgreSQL
- **Limitations**: Free services may spin down after inactivity
- **Upgrades**: Consider paid plans for production use with guaranteed uptime

### Security Best Practices

1. **Use Strong Secret Keys**: Generate cryptographically secure secret keys
2. **Environment Variables**: Never commit sensitive data to code
3. **Database Security**: Use strong passwords and limit access
4. **HTTPS**: Render provides SSL certificates automatically
5. **Regular Updates**: Keep dependencies updated for security patches

Your Job Hunt Tracker is now ready for production deployment with PostgreSQL and Render! 🚀