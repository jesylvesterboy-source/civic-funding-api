# Create DEPLOYMENT.md
echo "# 🚀 Deployment Guide

## Production Deployment Checklist

### Prerequisites
- Python 3.10+
- PostgreSQL database
- Redis server
- Web server (Nginx/Apache)
- Domain name

### Environment Setup
1. Clone repository:
   \`\`\`bash
   git clone https://github.com/yourusername/gates-grant-tracker.git
   cd gates-grant-tracker
   \`\`\`

2. Set up environment:
   \`\`\`bash
   cp .env.example .env
   # Edit .env with production values
   \`\`\`

3. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. Database setup:
   \`\`\`bash
   python manage.py migrate
   python manage.py collectstatic
   python manage.py createsuperuser
   \`\`\`

5. Start services:
   \`\`\`bash
   # Start Celery worker
   celery -A gates_tracker worker --loglevel=info

   # Start Celery beat (for scheduled tasks)
   celery -A gates_tracker beat --loglevel=info

   # Start Django (via Gunicorn in production)
   gunicorn gates_tracker.wsgi:application
   \`\`\`

## Client Handover Checklist
- [ ] GitHub repository transferred to client
- [ ] Production deployment completed
- [ ] Client team training conducted
- [ ] Documentation delivered
- [ ] Support handover process defined

## Support Information
This application is designed for tracking Gates Foundation grant impact.
For technical support, contact the development team.
" > DEPLOYMENT.md

# Create .env.example
echo "# Environment Configuration for Gates Tracker
# Copy this file to .env and fill in your actual values

# Django Settings
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,.yourdomain.com

# Database (PostgreSQL)
POSTGRES_DB=gates_tracker
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# API Settings
API_DEBUG=False

# Production Settings
CSRF_TRUSTED_ORIGINS=https://*.yourdomain.com" > .env.example