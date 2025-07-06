# Manual Deployment Steps (You're Already on Server!)

## 🎯 Current Status
✅ You're already SSH'd into your server: `aeconlin@s3490 api`
✅ Files are already pulled from GitHub
✅ You're in the right directory: `/home/aeconlin/public_html/api/`

## 🚀 IMMEDIATE STEPS TO COMPLETE DEPLOYMENT

### Step 1: Set File Permissions
```bash
# You're already in /home/aeconlin/public_html/api/
chmod 755 wsgi.py
chmod 644 product_management.py
chmod 644 .htaccess
chmod 644 requirements.txt
```

### Step 2: Create Environment File
```bash
# Create .env file for production
cat > .env << 'EOF'
DATABASE_URL=sqlite:///./product_management.db
ENVIRONMENT=production
DEBUG=false
EOF
```

### Step 3: Test Python Environment
```bash
# Check Python version and modules
python3 --version

# Test if FastAPI is available
python3 -c "
try:
    import fastapi
    print('✅ FastAPI is available')
    print('FastAPI version:', fastapi.__version__)
except ImportError:
    print('❌ FastAPI not available')
    print('You may need to contact hosting provider to install it')

try:
    import sqlite3
    print('✅ SQLite is available')
except ImportError:
    print('❌ SQLite not available')

try:
    import uvicorn
    print('✅ Uvicorn is available')
except ImportError:
    print('❌ Uvicorn not available')
"
```

### Step 4: Test WSGI Application
```bash
# Test the WSGI file directly
python3 wsgi.py
```

### Step 5: Create Database Directory (if needed)
```bash
# Make sure directory is writable for database creation
chmod 755 .
touch product_management.db
chmod 666 product_management.db
```

### Step 6: Test Web Access
```bash
# Test if the API is accessible
curl -I http://aeconlineshop.com/api/health
# or
wget -O - http://aeconlineshop.com/api/health
```

## 🔧 If FastAPI is Not Available

### Option A: Contact Hosting Provider
Ask them to install:
- `python3-fastapi`
- `python3-uvicorn`
- `python3-pydantic`

### Option B: User-level Installation (if pip is available)
```bash
# Try installing in user directory
pip3 install --user fastapi uvicorn pydantic

# Or try with python -m pip
python3 -m pip install --user fastapi uvicorn pydantic
```

### Option C: Check Alternative Python Versions
```bash
# Check what Python versions are available
ls /usr/bin/python*

# Try different versions
python3.8 -c "import fastapi; print('FastAPI available')"
python3.9 -c "import fastapi; print('FastAPI available')"
python3.10 -c "import fastapi; print('FastAPI available')"
```

## 🌐 Expected Results

After successful deployment, these URLs should work:
- **API Docs**: http://aeconlineshop.com/api/docs
- **Health Check**: http://aeconlineshop.com/api/health
- **OpenAPI**: http://aeconlineshop.com/api/openapi.json

## 🐛 Troubleshooting

### Check Apache Error Logs
```bash
# Look for error logs (common locations)
tail -f ~/logs/error_log
# or
tail -f /home/aeconlin/logs/error_log
# or check cPanel Error Logs interface
```

### Test .htaccess Rules
```bash
# Check if .htaccess is being read
echo "# Test comment" >> .htaccess
```

### Verify File Structure
```bash
# Your directory should look like this:
ls -la
# Should show:
# -rw-r--r-- .htaccess
# -rw-r--r-- product_management.py
# -rwxr-xr-x wsgi.py
# -rw-r--r-- requirements.txt
# -rw-r--r-- .env
```

## 📋 Quick Commands Summary

Run these commands in order:
```bash
# Set permissions
chmod 755 wsgi.py && chmod 644 product_management.py .htaccess requirements.txt

# Create environment
echo "DATABASE_URL=sqlite:///./product_management.db" > .env
echo "ENVIRONMENT=production" >> .env

# Test Python
python3 -c "import fastapi; print('FastAPI OK')"

# Test WSGI
python3 wsgi.py

# Test web access
curl -I http://aeconlineshop.com/api/health
```

## 🎉 Success Indicators

You'll know it's working when:
- ✅ `python3 wsgi.py` runs without errors
- ✅ `curl http://aeconlineshop.com/api/health` returns 200 OK
- ✅ http://aeconlineshop.com/api/docs loads in browser
- ✅ No errors in Apache error logs

---

**You're almost there!** The files are deployed, now just need to set permissions and test. 🚀