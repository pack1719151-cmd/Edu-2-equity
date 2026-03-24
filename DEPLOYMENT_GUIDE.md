# 🚀 EduEquity OS - Public Deployment Guide

## Current Status
✅ **All systems verified and operational**
✅ **Ready for public deployment**

---

## Pre-Deployment Checklist

### ✅ Completed Tasks
- [x] Backend API fully functional
- [x] Frontend UI decorated and responsive
- [x] Authentication system working
- [x] Database configured
- [x] All endpoints tested
- [x] Security features implemented
- [x] Git repository clean

### Current Servers
- **Backend**: http://localhost:8000 (FastAPI)
- **Frontend**: http://localhost:3000 (Next.js)
- **Database**: SQLite (local)

---

## Deployment Options

### Option 1: Cloud Deployment (Recommended)

#### Using Heroku
```bash
# 1. Create Heroku apps
heroku create eduequity-api
heroku create eduequity-web

# 2. Add buildpacks
heroku buildpacks:add heroku/python --app eduequity-api
heroku buildpacks:add heroku/nodejs --app eduequity-web

# 3. Deploy backend
cd apps/api
git push heroku main

# 4. Deploy frontend
cd ../web
git push heroku main
```

#### Using AWS EC2
```bash
# 1. Launch EC2 instance
# 2. Install dependencies (Python, Node.js, PostgreSQL)
# 3. Clone repository
# 4. Run setup scripts
./scripts/setup.sh

# 5. Start services with PM2
npm install -g pm2
pm2 start "uvicorn app.main:app" --name "api"
pm2 start "npm run dev" --name "web"
pm2 save
```

#### Using Docker
```dockerfile
# Create Dockerfile for backend
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]

# Create Dockerfile for frontend
FROM node:18
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

### Option 2: Traditional VPS Deployment

```bash
# 1. SSH into VPS
ssh root@your-server.com

# 2. Install dependencies
apt-get update
apt-get install python3 python3-pip nodejs npm postgresql

# 3. Clone repository
git clone https://github.com/pack1719151-cmd/eduequity-os.git
cd eduequity-os

# 4. Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r apps/api/requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env with production values

# 6. Start services
# Backend (with Gunicorn)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app

# Frontend
npm install
npm run build
npm start
```

---

## Environment Configuration

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost/eduequity
CORS_ORIGINS=https://yourdomain.com
SECRET_KEY=your-secret-key-here
DEBUG=false
```

### Frontend (.env.production)
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_API_V1=/api/v1
```

---

## Database Setup for Production

### Migration from SQLite to PostgreSQL

```bash
# 1. Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# 2. Create database
createdb eduequity

# 3. Update DATABASE_URL
export DATABASE_URL="postgresql://user:password@localhost/eduequity"

# 4. Run migrations
alembic upgrade head

# 5. Import existing data (if needed)
python scripts/migrate_db.py
```

### Backup Strategy
```bash
# Daily backup
0 2 * * * pg_dump eduequity > /backups/eduequity-$(date +\%Y\%m\%d).sql

# Weekly backup to S3
0 3 * * 0 aws s3 cp /backups/eduequity-latest.sql s3://your-bucket/backups/
```

---

## Security Hardening

### SSL/TLS Setup
```bash
# Using Let's Encrypt with Certbot
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d yourdomain.com
```

### Nginx Configuration
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Authorization $http_authorization;
    }
}
```

### Security Headers
```python
# Add to FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourdomain.com"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Monitoring & Logging

### Setup Monitoring
```bash
# Install PM2 monitoring
pm2 install pm2-logrotate
pm2 monit

# Install error tracking
pip install sentry-sdk
```

### Configure Logging
```python
# Backend
import logging
logger = logging.getLogger(__name__)
logger.info("User registered: %s", email)

# Frontend
import posthog
posthog.capture("user_action", {"action": "registered"})
```

---

## Performance Optimization

### Frontend Optimization
```javascript
// Next.js build optimization
next build
next export  // Static export

// Image optimization
npm install sharp
```

### Backend Optimization
```bash
# Use Gunicorn with multiple workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app

# Enable caching
pip install redis
```

### Database Optimization
```sql
-- Add indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

---

## CI/CD Setup

### GitHub Actions
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Test Backend
        run: |
          cd apps/api
          pip install -r requirements.txt
          pytest
      - name: Test Frontend
        run: |
          cd apps/web
          npm install
          npm run test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          # Your deployment commands here
```

---

## Post-Deployment

### Health Checks
```bash
# Monitor endpoints
curl https://yourdomain.com/health
curl https://yourdomain.com/api/v1/health

# Check logs
pm2 logs
tail -f /var/log/nginx/error.log
```

### Updates & Maintenance
```bash
# Regular updates
git pull origin main
npm update
pip install -r requirements.txt --upgrade

# Database backups
pg_dump eduequity > backup.sql

# Restart services
pm2 restart all
```

---

## Troubleshooting

### Common Issues

**Issue**: CORS errors
```python
# Solution: Update CORS_ORIGINS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Issue**: Database connection
```bash
# Solution: Check connection string
DATABASE_URL=postgresql://user:password@db-host:5432/eduequity
```

**Issue**: Static files not loading
```bash
# Solution: Configure static files in Nginx
location /static/ {
    alias /path/to/apps/web/.next/static/;
}
```

---

## Support & Documentation

- **API Docs**: https://api.yourdomain.com/docs
- **GitHub**: https://github.com/pack1719151-cmd/eduequity-os
- **Issues**: Report bugs on GitHub Issues

---

## License
See LICENSE file for details

