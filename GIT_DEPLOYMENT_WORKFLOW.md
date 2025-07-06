# 🚀 Git-Based Deployment Workflow

## 🎯 Your Final Deployment Plan (Git-Based Workflow)

### ✅ Local PC (Prepare and Test)

#### Step 1: Complete Local Development
```bash
# Activate your local environment
source .venv/bin/activate

# Make sure all dependencies are captured
pip freeze > requirements.txt

# Test your API locally
uvicorn product_management:app --reload
```

#### Step 2: Test All Endpoints
```bash
# Health check
curl http://localhost:8000/

# Test products endpoint
curl http://localhost:8000/products

# Test search functionality
curl "http://localhost:8000/products/search?q=test"

# Run comprehensive tests
python test_everything.py http://localhost:8000
```

#### Step 3: Commit and Push to Git
```bash
# Add all changes
git add .

# Commit with descriptive message
git commit -m "Final deploy-ready API with image search and full functionality"

# Push to main branch
git push origin main
```

---

### ✅ Server Deployment (Production)

#### Step 1: SSH into Your Server
```bash
ssh aeconlin@your-server-ip
```

#### Step 2: Navigate to Project Directory
```bash
cd ~/product-management
```

#### Step 3: Pull Latest Code
```bash
# Pull the latest changes
git pull origin main

# Verify the pull was successful
git log --oneline -5
```

#### Step 4: Activate Virtual Environment
```bash
# Activate your server's virtual environment
source ~/virtualenv/product-management/3.9/bin/activate

# Verify activation
which python
which pip
```

#### Step 5: Install/Update Dependencies
```bash
# Install or update all dependencies
pip install -r requirements.txt

# Install additional production dependencies if needed
pip install gunicorn uvicorn[standard]

# Verify critical packages
pip list | grep -E "(fastapi|uvicorn|gunicorn|databases|aiosqlite)"
```

#### Step 6: Start/Restart Gunicorn
```bash
# Kill any existing Gunicorn processes
pkill -f gunicorn

# Start Gunicorn with proper configuration
gunicorn product_management:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8010

# Or run in background
nohup gunicorn product_management:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8010 > gunicorn.log 2>&1 &
```

---

### ⚙️ Set up Reverse Proxy (If Not Done Yet)

#### Nginx Configuration
Create or update your Nginx configuration:

```bash
# Edit Nginx site configuration
sudo nano /etc/nginx/sites-available/e-catalog.dahoughengenterprise.com
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name e-catalog.dahoughengenterprise.com;
    
    location / {
        proxy_pass http://localhost:8010;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

#### Enable and Restart Nginx
```bash
# Enable the site (if not already enabled)
sudo ln -s /etc/nginx/sites-available/e-catalog.dahoughengenterprise.com /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Check Nginx status
sudo systemctl status nginx
```

---

### ✅ Optional: Make Gunicorn Persistent

#### Create Systemd Service File
```bash
# Create the service file
sudo nano /etc/systemd/system/product-management.service
```

Add this content:
```ini
[Unit]
Description=Product Management API
After=network.target

[Service]
User=aeconlin
Group=aeconlin
WorkingDirectory=/home/aeconlin/product-management
Environment=PATH=/home/aeconlin/virtualenv/product-management/3.9/bin
ExecStart=/home/aeconlin/virtualenv/product-management/3.9/bin/gunicorn product_management:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8010
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

#### Enable and Start the Service
```bash
# Reload systemd daemon
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable product-management

# Start the service
sudo systemctl start product-management

# Check service status
sudo systemctl status product-management
```

---

### ✅ Final Verifications

#### Test Your Deployed API
```bash
# Test from server
curl http://localhost:8010/

# Test from external (your domain)
curl https://e-catalog.dahoughengenterprise.com/

# Test specific endpoints
curl https://e-catalog.dahoughengenterprise.com/products
curl https://e-catalog.dahoughengenterprise.com/health
```

#### Monitor Logs
```bash
# Monitor systemd service logs
sudo journalctl -u product-management -f

# Monitor Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Monitor Gunicorn logs (if running manually)
tail -f ~/product-management/gunicorn.log
```

---

## 🚀 Quick Deployment Commands

### For Future Updates (Copy-Paste Ready)

#### On Your Local Machine:
```bash
# Test locally
source .venv/bin/activate
uvicorn product_management:app --reload
# Test endpoints...

# Commit and push
git add .
git commit -m "Update: [describe your changes]"
git push origin main
```

#### On Your Server:
```bash
# SSH and deploy
ssh aeconlin@your-server-ip
cd ~/product-management
git pull origin main
source ~/virtualenv/product-management/3.9/bin/activate
pip install -r requirements.txt

# If using systemd service:
sudo systemctl restart product-management

# If running manually:
pkill -f gunicorn
nohup gunicorn product_management:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8010 > gunicorn.log 2>&1 &

# Verify
curl https://e-catalog.dahoughengenterprise.com/
```

---

## 🔧 Troubleshooting Commands

### Check What's Running on Port 8010
```bash
sudo lsof -i :8010
sudo netstat -tlnp | grep :8010
```

### Kill Processes on Port 8010
```bash
sudo kill -9 $(sudo lsof -t -i:8010)
# Or
pkill -f gunicorn
```

### Check Service Status
```bash
sudo systemctl status product-management
sudo systemctl status nginx
```

### View Recent Logs
```bash
sudo journalctl -u product-management --since "10 minutes ago"
sudo journalctl -u nginx --since "10 minutes ago"
```

### Test Database Connection
```bash
cd ~/product-management
source ~/virtualenv/product-management/3.9/bin/activate
python -c "
import os
from databases import Database
from dotenv import load_dotenv
load_dotenv()
db_url = os.getenv('DATABASE_URL', 'sqlite:///./products.db')
print(f'Database URL: {db_url}')
print('✅ Database configuration loaded')
"
```

---

## 🎉 Summary in Gen Z Style

### The Deployment Flow:
- 👉 **Code it** 🖥️ (Local development and testing)
- 👉 **Push it** 🚀 (Git commit and push)
- 👉 **Pull it** 🔄 (Git pull on server)
- 👉 **Install it** 📦 (pip install -r requirements.txt)
- 👉 **Restart it** 🔁 (Restart Gunicorn/systemd service)
- 👉 **Proxy it** 🔂 (Nginx forwards to your app)
- 👉 **Test it** ✅ (Verify endpoints work)
- 👉 **Done** 🎯 (API live at e-catalog.dahoughengenterprise.com)

### One-Liner Deployment (After Initial Setup):
```bash
# Local
git add . && git commit -m "Update" && git push origin main

# Server
ssh aeconlin@your-server-ip "cd ~/product-management && git pull origin main && source ~/virtualenv/product-management/3.9/bin/activate && pip install -r requirements.txt && sudo systemctl restart product-management"
```

**Your API will be live at: https://e-catalog.dahoughengenterprise.com** 🚀