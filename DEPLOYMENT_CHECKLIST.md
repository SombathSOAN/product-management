# 🚀 Deployment Checklist - Product Management API

## 📋 Pre-Deployment Checklist

### ✅ Local Development Ready
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Environment variables configured (`.env` file)
- [ ] All tests passing (`python test_everything.py`)
- [ ] Server starts locally (`uvicorn product_management:app --reload`)
- [ ] API endpoints responding correctly
- [ ] Database connection working

### ✅ Code Quality
- [ ] No syntax errors or import issues
- [ ] All functions have proper error handling
- [ ] Database queries are optimized
- [ ] Security best practices implemented
- [ ] API documentation is complete
- [ ] Logging is properly configured

### ✅ Production Configuration
- [ ] Production environment variables set
- [ ] Database URL configured for production
- [ ] Debug mode disabled (`DEBUG=false`)
- [ ] Secret keys generated and secured
- [ ] CORS settings configured properly
- [ ] SSL/TLS certificates ready (if applicable)

---

## 🌐 Deployment Options

### Option 1: Shared Hosting (cPanel)

#### Requirements
- [ ] Python 3.9+ support
- [ ] SSH access (preferred)
- [ ] MySQL database available
- [ ] Sufficient storage (1GB+)
- [ ] Passenger WSGI support

#### Steps
```bash
# 1. Upload files
tar -czf project.tar.gz .
# Upload via cPanel File Manager

# 2. Extract and setup
cd public_html/api
tar -xzf project.tar.gz
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Configure database
echo "DATABASE_URL=mysql+aiomysql://user:pass@localhost:3306/dbname" > .env

# 4. Set permissions
chmod 755 public_html/api
chmod 644 *.py
chmod 644 .htaccess
```

#### Verification
- [ ] Files uploaded successfully
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Database connection working
- [ ] WSGI file configured
- [ ] Permissions set correctly
- [ ] API accessible via domain

### Option 2: VPS/Cloud Server

#### Requirements
- [ ] Ubuntu 20.04+ or similar
- [ ] Root/sudo access
- [ ] 2GB+ RAM
- [ ] Python 3.9+ installed
- [ ] Nginx/Apache for reverse proxy

#### Steps
```bash
# 1. System setup
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv nginx -y

# 2. Project setup
sudo mkdir -p /var/www/product-management
sudo chown $USER:$USER /var/www/product-management
cd /var/www/product-management

# 3. Install project
# Upload files here
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt gunicorn

# 4. Configure environment
echo "DATABASE_URL=postgresql://user:pass@localhost:5432/dbname" > .env

# 5. Create systemd service
sudo cp product-management.service /etc/systemd/system/
sudo systemctl enable product-management
sudo systemctl start product-management

# 6. Configure Nginx
sudo cp nginx.conf /etc/nginx/sites-available/product-management
sudo ln -s /etc/nginx/sites-available/product-management /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

#### Verification
- [ ] System dependencies installed
- [ ] Project files deployed
- [ ] Virtual environment working
- [ ] Database connected
- [ ] Systemd service running
- [ ] Nginx proxy configured
- [ ] SSL certificate installed
- [ ] Domain pointing to server

### Option 3: Platform as a Service (Railway, Heroku, etc.)

#### Requirements
- [ ] Git repository
- [ ] Platform account
- [ ] Database addon (if needed)
- [ ] Environment variables configured

#### Steps for Railway
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login and init
railway login
railway init

# 3. Set environment variables
railway variables set DATABASE_URL=postgresql://...
railway variables set ENVIRONMENT=production

# 4. Deploy
railway up

# 5. Get URL
railway status
```

#### Verification
- [ ] Repository connected
- [ ] Build successful
- [ ] Environment variables set
- [ ] Database connected
- [ ] Application deployed
- [ ] Custom domain configured (optional)

---

## 🔧 Environment Configuration

### Local Development
```bash
DATABASE_URL=sqlite:///./local_products.db
DEBUG=true
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
```

### Production
```bash
DATABASE_URL=postgresql://user:password@host:5432/database
DEBUG=false
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Database URLs
```bash
# SQLite (development)
DATABASE_URL=sqlite:///./database.db

# MySQL
DATABASE_URL=mysql+aiomysql://user:password@host:3306/database

# PostgreSQL
DATABASE_URL=postgresql://user:password@host:5432/database

# MySQL with SSL
DATABASE_URL=mysql+aiomysql://user:password@host:3306/database?ssl=true
```

---

## 🧪 Testing Checklist

### Pre-Deployment Testing
```bash
# 1. Run all tests locally
python test_everything.py

# 2. Test with production-like environment
export DATABASE_URL=postgresql://...
python test_everything.py

# 3. Load testing (optional)
pip install locust
locust -f locustfile.py --host=http://localhost:8000
```

### Post-Deployment Testing
```bash
# 1. Health check
curl https://yourdomain.com/
curl https://yourdomain.com/health

# 2. API endpoints
curl https://yourdomain.com/products
curl https://yourdomain.com/reviews
curl https://yourdomain.com/banners

# 3. Comprehensive tests
python test_everything.py https://yourdomain.com

# 4. Performance check
curl -w "@curl-format.txt" -o /dev/null -s https://yourdomain.com/
```

---

## 🔍 Monitoring & Maintenance

### Health Monitoring
```bash
# Create monitoring script
cat > monitor.sh << 'EOF'
#!/bin/bash
URL="https://yourdomain.com/health"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $URL)

if [ $RESPONSE -eq 200 ]; then
    echo "✅ API is healthy"
else
    echo "❌ API is down (HTTP $RESPONSE)"
    # Send alert (email, Slack, etc.)
fi
EOF

# Add to crontab
echo "*/5 * * * * /path/to/monitor.sh" | crontab -
```

### Log Monitoring
```bash
# System logs
sudo journalctl -u product-management -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Application logs
tail -f /var/www/product-management/app.log
```

### Backup Strategy
```bash
# Database backup
pg_dump $DATABASE_URL > backup-$(date +%Y%m%d).sql

# File backup
tar -czf backup-files-$(date +%Y%m%d).tar.gz /var/www/product-management

# Automated backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d)
pg_dump $DATABASE_URL > /backups/db-$DATE.sql
tar -czf /backups/files-$DATE.tar.gz /var/www/product-management
# Upload to cloud storage
EOF
```

---

## 🚨 Troubleshooting

### Common Deployment Issues

#### 1. "Module not found" errors
```bash
# Solution: Reinstall dependencies
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### 2. Database connection errors
```bash
# Check database URL
echo $DATABASE_URL

# Test connection
python -c "
import os
from databases import Database
db = Database(os.getenv('DATABASE_URL'))
print('Database URL is valid')
"
```

#### 3. Permission errors
```bash
# Fix file permissions
chmod 755 /var/www/product-management
chmod 644 /var/www/product-management/*.py
chown -R www-data:www-data /var/www/product-management
```

#### 4. Port conflicts
```bash
# Check what's using the port
sudo lsof -i :8000

# Kill conflicting process
sudo kill -9 $(sudo lsof -t -i:8000)
```

#### 5. SSL/HTTPS issues
```bash
# Install Let's Encrypt certificate
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### Emergency Recovery
```bash
# 1. Stop services
sudo systemctl stop product-management
sudo systemctl stop nginx

# 2. Restore from backup
cd /var/www/product-management
tar -xzf /backups/files-latest.tar.gz

# 3. Restore database
psql $DATABASE_URL < /backups/db-latest.sql

# 4. Restart services
sudo systemctl start product-management
sudo systemctl start nginx

# 5. Verify
curl https://yourdomain.com/health
```

---

## ✅ Success Criteria

### Deployment is successful when:
- [ ] API responds to health checks
- [ ] All endpoints return expected responses
- [ ] Database operations work correctly
- [ ] Image upload and processing functional
- [ ] Search functionality working
- [ ] Performance meets requirements
- [ ] SSL certificate valid (if applicable)
- [ ] Monitoring alerts configured
- [ ] Backup system operational
- [ ] Documentation updated

### Performance Benchmarks
- [ ] Response time < 200ms for simple endpoints
- [ ] Response time < 2s for image processing
- [ ] Can handle 100+ concurrent requests
- [ ] Database queries optimized
- [ ] Memory usage < 512MB
- [ ] CPU usage < 50% under normal load

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks
- [ ] Update dependencies monthly
- [ ] Monitor disk space and logs
- [ ] Review and rotate log files
- [ ] Test backup and recovery procedures
- [ ] Update SSL certificates
- [ ] Security patches and updates
- [ ] Performance monitoring and optimization

### Emergency Contacts
- [ ] Server provider support
- [ ] Database administrator
- [ ] Domain registrar
- [ ] SSL certificate provider
- [ ] Development team contacts

---

**🎉 Congratulations! Your Product Management API is now ready for production deployment!**