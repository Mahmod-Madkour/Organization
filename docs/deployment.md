# Deployment Guide

## Overview

This guide covers deployment options for the Quran Organization Management System, including development, staging, and production environments.

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Django 5.0+
- Web server (Nginx, Apache)
- WSGI server (Gunicorn, uWSGI)
- Database (SQLite for development, PostgreSQL/MySQL for production)
- SSL certificate (for production)

### Software Dependencies
- All requirements from `requirements.txt`
- Additional production dependencies (if needed)

## Environment Setup

### Development Environment

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd Organization
   ```

2. **Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   ```bash
   # Create .env file
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python auto_fill_data.py  # Optional initial data
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

### Production Environment

#### 1. Server Preparation

**Update System Packages**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib -y
```

**Create Application User**
```bash
sudo adduser djangoapp
sudo usermod -aG sudo djangoapp
```

#### 2. Application Setup

**Clone and Setup Code**
```bash
sudo -u djangoapp git clone <repository-url> /home/djangoapp/Organization
cd /home/djangoapp/Organization
sudo -u djangoapp python3 -m venv venv
sudo -u djangoapp venv/bin/pip install -r requirements.txt
```

**Production Settings**
```python
# Organization/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-production-secret-key')
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quran_org',
        'USER': 'quran_user',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Session security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
```

**Environment Variables**
```bash
# Create .env file
sudo -u djangoapp nano /home/djangoapp/Organization/.env
```

Content:
```
SECRET_KEY=your-very-secure-secret-key
DB_PASSWORD=your-database-password
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

#### 3. Database Setup (PostgreSQL)

**Create Database and User**
```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE quran_org;
CREATE USER quran_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE quran_org TO quran_user;
\q
```

**Install PostgreSQL Adapter**
```bash
sudo -u djangoapp venv/bin/pip install psycopg2-binary
```

**Run Migrations**
```bash
sudo -u djangoapp venv/bin/python manage.py migrate
sudo -u djangoapp venv/bin/python manage.py createsuperuser
sudo -u djangoapp venv/bin/python manage.py collectstatic --noinput
```

#### 4. Gunicorn Setup

**Install Gunicorn**
```bash
sudo -u djangoapp venv/bin/pip install gunicorn
```

**Create Gunicorn Service File**
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Content:
```ini
[Unit]
Description=gunicorn daemon for Quran Organization
After=network.target

[Service]
User=djangoapp
Group=djangoapp
WorkingDirectory=/home/djangoapp/Organization
Environment="PATH=/home/djangoapp/Organization/venv/bin"
EnvironmentFile=/home/djangoapp/Organization/.env
ExecStart=/home/djangoapp/Organization/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/gunicorn.sock \
    Organization.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Start and Enable Gunicorn**
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

#### 5. Nginx Configuration

**Create Nginx Config**
```bash
sudo nano /etc/nginx/sites-available/quran_org
```

Content:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Django Media
    location /media/ {
        alias /home/djangoapp/Organization/media/;
    }

    # Django Static
    location /static/ {
        alias /home/djangoapp/Organization/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Gunicorn
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

**Enable Site**
```bash
sudo ln -s /etc/nginx/sites-available/quran_org /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. SSL Certificate (Let's Encrypt)

**Install Certbot**
```bash
sudo apt install certbot python3-certbot-nginx -y
```

**Get SSL Certificate**
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

**Auto-renewal**
```bash
sudo crontab -e
```

Add:
```
0 12 * * * /usr/bin/certbot renew --quiet
```

## PythonAnywhere Deployment

The project is pre-configured for PythonAnywhere deployment.

### Setup Steps

1. **Create PythonAnywhere Account**
   - Sign up at pythonanywhere.com
   - Choose appropriate plan

2. **Create Web App**
   - Go to Web tab
   - Add new web app
   - Choose Django framework
   - Select Python version

3. **Upload Code**
   ```bash
   # Using PythonAnywhere console
   git clone <repository-url>
   cd Organization
   ```

4. **Configure Virtual Environment**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Web App**
   - Set working directory: `/home/username/Organization`
   - Set WSGI file: `/home/username/Organization/Organization/wsgi.py`
   - Set virtualenv path: `/home/username/.virtualenvs/venv`

6. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

7. **Update Allowed Hosts**
   ```python
   ALLOWED_HOSTS = ['username.pythonanywhere.com']
   ```

8. **Reload Web App**
   - Click reload button in Web tab

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create and run migrations
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Organization.wsgi:application"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: quran_org
      POSTGRES_USER: quran_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    command: gunicorn --bind 0.0.0.0:8000 Organization.wsgi:application
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DEBUG=False
      - SECRET_KEY=your-secret-key
      - DB_HOST=db
      - DB_NAME=quran_org
      - DB_USER=quran_user
      - DB_PASSWORD=secure_password

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

## Monitoring and Maintenance

### Log Management

**Gunicorn Logs**
```bash
sudo journalctl -u gunicorn
```

**Nginx Logs**
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

**Django Logs**
```python
# Add to settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/djangoapp/Organization/logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Backup Strategy

**Database Backup**
```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/home/djangoapp/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U quran_user quran_org > $BACKUP_DIR/backup_$DATE.sql
```

**Media Files Backup**
```bash
rsync -av /home/djangoapp/Organization/media/ /home/djangoapp/backups/media/
```

### Performance Optimization

**Database Optimization**
```python
# Add to settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quran_org',
        'USER': 'quran_user',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'MAX_CONNS': 20,
        }
    }
}
```

**Caching**
```python
# Add to settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

## Troubleshooting

### Common Issues

**502 Bad Gateway**
- Check Gunicorn status: `sudo systemctl status gunicorn`
- Check socket file: `ls -la /run/gunicorn.sock`
- Check Nginx error logs

**Database Connection Errors**
- Verify database credentials
- Check PostgreSQL status: `sudo systemctl status postgresql`
- Test connection: `psql -h localhost -U quran_user -d quran_org`

**Static Files Not Loading**
- Run collectstatic: `python manage.py collectstatic`
- Check Nginx static file configuration
- Verify file permissions

**Permission Errors**
```bash
sudo chown -R djangoapp:djangoapp /home/djangoapp/Organization
sudo chmod -R 755 /home/djangoapp/Organization
```

### Performance Issues

**Slow Database Queries**
- Use Django Debug Toolbar
- Add database indexes
- Optimize queries with select_related/prefetch_related

**High Memory Usage**
- Reduce Gunicorn workers
- Implement caching
- Optimize database connections

## Security Checklist

### Production Security
- [ ] DEBUG = False
- [ ] Secure SECRET_KEY
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enabled
- [ ] Security headers set
- [ ] Database credentials secured
- [ ] File permissions correct
- [ ] Regular backups configured
- [ ] SSL certificate valid
- [ ] Firewall configured

### Django Security
- [ ] CSRF protection enabled
- [ ] XSS protection enabled
- [ ] SQL injection protection
- [ ] Secure password storage
- [ ] Session security configured
- [ ] Clickjacking protection enabled

## Update and Maintenance

### Regular Updates
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Python packages
pip install -r requirements.txt --upgrade

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart gunicorn nginx
```

### Maintenance Schedule
- **Daily**: Check logs, backup database
- **Weekly**: Update packages, check security
- **Monthly**: Review performance, clean up logs
- **Quarterly**: Security audit, update SSL certificates
