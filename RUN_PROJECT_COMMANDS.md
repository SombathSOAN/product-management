# 🚀 Commands to Run Your Product Management API

## 📋 Quick Start Commands

### 1. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 2. Run the Project (Choose One Option)

#### Option A: With Local SQLite Database (Easiest)
```bash
# Create local database configuration
echo "DATABASE_URL=sqlite:///./local_products.db" > .env

# Start the server
python run_server.py
```

#### Option B: With Your Remote MySQL Database
```bash
# Use your existing database
echo "DATABASE_URL=mysql+aiomysql://aeconlin_pm:admindahfh%40pm2025%21%21@192.250.235.86:3306/aeconlin_pmdb" > .env

# Start the server
python run_server.py
```

#### Option C: Direct Uvicorn Command
```bash
# Simple direct command
uvicorn product_management:app --host 0.0.0.0 --port 8001 --reload
```

### 3. Access Your API
```
🌐 API URL: http://localhost:8001
📚 Documentation: http://localhost:8001/docs
🔍 Health Check: http://localhost:8001/health
```

---

## 🧪 Test Commands

### Run All Tests
```bash
# Activate environment
source venv/bin/activate

# Test imports and setup
python test_import_only.py
python test_optimizations.py
python test_local_simple.py

# Test full API (after server is running)
python test_everything.py
```

### One-Line Test Command
```bash
source venv/bin/activate && python test_import_only.py && python test_optimizations.py && python test_local_simple.py
```

---

## 🔧 Production Commands

### For Development
```bash
source venv/bin/activate
python run_server.py
```

### For Production (Gunicorn)
```bash
source venv/bin/activate
USE_GUNICORN=true python run_server.py
```

### Manual Gunicorn
```bash
source venv/bin/activate
gunicorn product_management:app -c gunicorn.conf.py
```

---

## 🌐 API Endpoints to Test

Once running, test these URLs:

### Health Checks
- http://localhost:8001/
- http://localhost:8001/health

### Products
- http://localhost:8001/products
- http://localhost:8001/products/search?q=test
- http://localhost:8001/products/top-rated

### Interactive Documentation
- http://localhost:8001/docs (Swagger UI)
- http://localhost:8001/redoc (ReDoc)

---

## 📱 cURL Commands for Testing

```bash
# Health check
curl http://localhost:8001/

# List products
curl http://localhost:8001/products

# Search products
curl "http://localhost:8001/products/search?q=coffee"

# Image search (with test image)
curl -X POST http://localhost:8001/products/search-by-image \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.jpg"
```

---

## 🛠️ Troubleshooting Commands

### If Port 8001 is Busy
```bash
# The run_server.py automatically finds available ports 8001-8010
python run_server.py
```

### Check What's Running on Port
```bash
lsof -i :8001
```

### Kill Process on Port
```bash
kill -9 $(lsof -t -i:8001)
```

### Reset Environment
```bash
deactivate
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🎯 Recommended Workflow

### First Time Setup
```bash
# 1. Activate environment
source venv/bin/activate

# 2. Run tests to verify setup
python test_import_only.py
python test_optimizations.py
python test_local_simple.py

# 3. Create local database config
echo "DATABASE_URL=sqlite:///./local_products.db" > .env

# 4. Start server
python run_server.py
```

### Daily Development
```bash
# Quick start
source venv/bin/activate && python run_server.py
```

### Testing
```bash
# In another terminal while server runs
source venv/bin/activate && python test_everything.py
```

---

## 🎉 Success Indicators

You'll know it's working when you see:

✅ **Server starts:** "Server will be available at http://0.0.0.0:8001"  
✅ **Health check:** http://localhost:8001/ returns JSON  
✅ **Documentation:** http://localhost:8001/docs loads  
✅ **Products API:** http://localhost:8001/products responds  

**Your Google Lens-like Product Management API is now running! 🚀**