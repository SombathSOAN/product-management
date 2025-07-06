# 🚀 Complete Setup Guide - Product Management API

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Server Deployment](#server-deployment)
4. [Testing & Verification](#testing--verification)
5. [Troubleshooting](#troubleshooting)
6. [Production Deployment](#production-deployment)

---

## 🔧 Prerequisites

### System Requirements
- **Python:** 3.9+ (recommended 3.11+)
- **Operating System:** macOS, Linux, or Windows
- **Memory:** Minimum 2GB RAM
- **Storage:** 1GB free space

### Check Your System
```bash
# Check Python version
python3 --version
# Should show Python 3.9.0 or higher

# Check pip
pip3 --version

# Check if git is installed
git --version
```

---

## 💻 Local Development Setup

### Step 1: Clone/Download Project
```bash
# If using git
git clone <your-repository-url>
cd "product management"

# Or if you have the files already, navigate to the directory
cd "/path/to/product management"
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate

# Verify activation (should show (.venv) in prompt)
which python
```

### Step 3: Install Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Install additional packages for local development
pip install aiosqlite

# Verify installation
pip list | grep fastapi
pip list | grep uvicorn
pip list | grep aiosqlite
```

### Step 4: Environment Configuration
```bash
# Create environment file for local development
cat > .env << EOF
DATABASE_URL=sqlite:///./local_products.db
DEBUG=true
ENVIRONMENT=development
EOF

# Verify environment file
cat .env
```

### Step 5: Test Installation
```bash
# Test basic imports
python test_import_only.py

# Test optimizations
python test_optimizations.py

# Test local environment
python test_local_simple.py

# All tests should show ✅ PASSED
```

### Step 6: Start Local Server
```bash
# Method 1: Using uvicorn directly (recommended for development)
uvicorn product_management:app --host 0.0.0.0 --port 8000 --reload

# Method 2: Using the run script
python run_server.py

# Method 3: Using start script
chmod +x start_server.sh
./start_server.sh
```

### Step 7: Verify Local Setup
```bash
# In another terminal, test the API
curl http://localhost:8000/
# Should return: {"message":"Product Management API is running","status":"healthy"}

# Test products endpoint
curl http://localhost:8000/products
# Should return: []

# Run comprehensive tests
python test_everything.py http://localhost:8000
# Should show 8/8 tests passed
```

---

## 🌐 Server Deployment

### Option A: Shared Hosting (cPanel)

#### Step 1: Upload Files
```bash
# Compress project files
tar -czf product_management.tar.gz .

# Upload via cPanel File Manager or SCP
scp product_management.tar.gz username@your-server.com:~/public_html/

# SSH into server
ssh username@your-server.com

# Extract files
cd public_html
tar -xzf product_management.tar.gz
```

#### Step 2: Server Environment Setup
```bash
# On the server, create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install aiosqlite

# Create production environment
cat > .env << EOF
DATABASE_URL=mysql+aiomysql://your_db_user:your_db_password@localhost:3306/your_db_name
ENVIRONMENT=production
DEBUG=false
EOF
```

#### Step 3: Set Permissions
```bash
# Set correct permissions
chmod 755 public_html
chmod 755 public_html/api
chmod 644 public_html/api/*.py
chmod 644 public_html/api/.htaccess
chmod 644 public_html/api/passenger_wsgi.py
```

#### Step 4: Test Server Installation
```bash
# Test Python import
python3 -c "
import sys
sys.path.insert(0, '.')
from product_management import app
print('✅ App imported successfully')
"

# Test WSGI
python3 wsgi.py
```

### Option B: VPS/Cloud Server

#### Step 1: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Install additional system packages
sudo apt install build-essential libssl-dev libffi-dev python3-dev -y
```

#### Step 2: Project Setup
```bash
# Create project directory
sudo mkdir -p /var/www/product-management
sudo chown $USER:$USER /var/www/product-management
cd /var/www/product-management

# Clone/upload project files
# ... (upload your files here)

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn aiosqlite
```

#### Step 3: Database Setup
```bash
# For SQLite (development)
echo "DATABASE_URL=sqlite:///./production.db" > .env

# For MySQL (production)
echo "DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/dbname" > .env

# For PostgreSQL (production)
echo "DATABASE_URL=postgresql://user:password@localhost:5432/dbname" > .env
```

#### Step 4: Create Systemd Service
```bash
# Create service file
sudo tee /etc/systemd/system/product-management.service << EOF
[Unit]
Description=Product Management API
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=/var/www/product-management
Environment=PATH=/var/www/product-management/.venv/bin
ExecStart=/var/www/product-management/.venv/bin/gunicorn product_management:app -c gunicorn.conf.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable product-management
sudo systemctl start product-management
sudo systemctl status product-management
```

#### Step 5: Nginx Configuration
```bash
# Create Nginx config
sudo tee /etc/nginx/sites-available/product-management << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/product-management /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option C: Railway Platform

#### Step 1: Prepare for Railway
```bash
# Ensure these files exist in your project:
ls railway.toml Procfile requirements.txt

# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login
```

#### Step 2: Deploy to Railway
```bash
# Initialize Railway project
railway init

# Set environment variables
railway variables set DATABASE_URL=postgresql://...

# Deploy
railway up

# Get deployment URL
railway status
```

---

## 🧪 Testing & Verification

### Local Testing Commands
```bash
# Activate environment
source .venv/bin/activate

# Basic tests
python test_import_only.py
python test_optimizations.py
python test_local_simple.py

# Start server (in background)
uvicorn product_management:app --host 0.0.0.0 --port 8000 &

# Wait for server to start
sleep 5

# Comprehensive API tests
python test_everything.py http://localhost:8000

# Manual endpoint tests
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/products
curl "http://localhost:8000/products/search?q=test"

# Stop background server
pkill -f uvicorn
```

### Server Testing Commands
```bash
# Test server endpoints
curl http://your-domain.com/
curl http://your-domain.com/health
curl http://your-domain.com/products

# Test from another machine
curl http://your-server-ip:8000/

# Check server logs
sudo journalctl -u product-management -f

# Check Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Performance Testing
```bash
# Install testing tools
pip install locust

# Create simple load test
cat > locustfile.py << EOF
from locust import HttpUser, task

class APIUser(HttpUser):
    @task
    def test_health(self):
        self.client.get("/")
    
    @task
    def test_products(self):
        self.client.get("/products")
EOF

# Run load test
locust -f locustfile.py --host=http://localhost:8000
```

---

## 🔍 Troubleshooting

### Common Issues & Solutions

#### 1. "Module not found" Error
```bash
# Solution: Reinstall dependencies
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install aiosqlite
```

#### 2. "Port already in use" Error
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 $(lsof -t -i:8000)

# Or use different port
uvicorn product_management:app --port 8001
```

#### 3. Database Connection Error
```bash
# For SQLite issues
echo "DATABASE_URL=sqlite:///./local.db" > .env

# For MySQL issues
pip install aiomysql pymysql

# For PostgreSQL issues
pip install asyncpg psycopg2-binary
```

#### 4. Permission Denied (Server)
```bash
# Fix file permissions
chmod 755 /path/to/project
chmod 644 /path/to/project/*.py
chmod +x /path/to/project/start_server.sh
```

#### 5. SSL/TLS Issues
```bash
# Install certificates
pip install --upgrade certifi

# For development, disable SSL verification
export PYTHONHTTPSVERIFY=0
```

### Debug Commands
```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Check installed packages
pip list

# Check environment variables
env | grep DATABASE_URL

# Test database connection
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('DATABASE_URL:', os.getenv('DATABASE_URL'))
"

# Check server process
ps aux | grep uvicorn
ps aux | grep gunicorn
```

---

## 🚀 Production Deployment

### Pre-deployment Checklist
```bash
# 1. Run all tests
python test_everything.py

# 2. Check security
pip install safety
safety check

# 3. Update dependencies
pip list --outdated

# 4. Create backup
tar -czf backup-$(date +%Y%m%d).tar.gz .

# 5. Set production environment
echo "ENVIRONMENT=production" >> .env
echo "DEBUG=false" >> .env
```

### Production Environment Variables
```bash
# Required environment variables
cat > .env.production << EOF
DATABASE_URL=your_production_database_url
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
EOF
```

### Production Server Commands
```bash
# Start with Gunicorn (production)
gunicorn product_management:app -c gunicorn.conf.py

# Start with systemd (recommended)
sudo systemctl start product-management
sudo systemctl enable product-management

# Monitor logs
sudo journalctl -u product-management -f

# Check status
sudo systemctl status product-management

# Restart service
sudo systemctl restart product-management
```

### Health Monitoring
```bash
# Create health check script
cat > health_check.sh << 'EOF'
#!/bin/bash
HEALTH_URL="http://localhost:8000/health"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)

if [ $RESPONSE -eq 200 ]; then
    echo "✅ API is healthy"
    exit 0
else
    echo "❌ API is down (HTTP $RESPONSE)"
    exit 1
fi
EOF

chmod +x health_check.sh

# Add to crontab for monitoring
echo "*/5 * * * * /path/to/health_check.sh" | crontab -
```

---

## 📊 Success Indicators

### You'll know everything is working when:

#### Local Development ✅
- Virtual environment activates without errors
- All dependencies install successfully
- All tests pass (8/8)
- Server starts on http://localhost:8000
- API documentation loads at http://localhost:8000/docs
- Health check returns 200 OK

#### Server Deployment ✅
- Files upload successfully to server
- Dependencies install without errors
- Database connection works
- Server starts without errors
- API accessible from external IP
- All endpoints respond correctly

#### Production Ready ✅
- SSL certificate installed
- Domain name configured
- Database optimized
- Monitoring setup
- Backup system in place
- Load balancing configured (if needed)

---

## 🎯 Quick Start Commands

### For Absolute Beginners
```bash
# 1. Download/clone project
cd "product management"

# 2. Setup environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install aiosqlite

# 3. Configure database
echo "DATABASE_URL=sqlite:///./local.db" > .env

# 4. Test setup
python test_import_only.py

# 5. Start server
uvicorn product_management:app --host 0.0.0.0 --port 8000 --reload

# 6. Test API (in new terminal)
curl http://localhost:8000/
```

### For Production Deployment
```bash
# 1. Server setup
sudo apt update && sudo apt install python3 python3-pip python3-venv nginx -y

# 2. Project setup
cd /var/www/product-management
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt gunicorn

# 3. Configure production
echo "DATABASE_URL=your_production_db_url" > .env

# 4. Start production server
gunicorn product_management:app -c gunicorn.conf.py

# 5. Setup reverse proxy (Nginx)
# Configure Nginx as shown in server deployment section
```

---

## 🎉 Congratulations!

If you've followed this guide, you now have:
- ✅