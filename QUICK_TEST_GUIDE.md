# 🚀 Quick Test Guide

## 🎯 How to Test Your API in 3 Steps

### Step 1: Run Basic Tests (No Server Required)
```bash
# Activate virtual environment
source venv/bin/activate

# Test imports and optimizations
python test_import_only.py
python test_optimizations.py
python test_local_simple.py
```

**Expected Result:** All tests should pass ✅

---

### Step 2: Test with Local Server (Optional)
```bash
# Option A: Test with your remote database
echo "DATABASE_URL=mysql+aiomysql://aeconlin_pm:admindahfh%40pm2025%21%21@192.250.235.86:3306/aeconlin_pmdb" > .env
python run_server.py

# Option B: Test with local database (easier)
echo "DATABASE_URL=sqlite:///./test.db" > .env
python run_server.py
```

**Expected Result:** Server starts at http://localhost:8001 ✅

---

### Step 3: Run Comprehensive API Tests
```bash
# In another terminal (while server is running)
source venv/bin/activate
python test_everything.py

# Or test your production server
python test_everything.py http://aeconlineshop.com/api
```

**Expected Result:** Most tests pass, API is functional ✅

---

## 🌐 Browser Testing

Open these URLs in your browser:

### Local Testing:
- http://localhost:8001/ (Health check)
- http://localhost:8001/docs (Interactive API documentation)
- http://localhost:8001/products (List products)

### Production Testing:
- http://aeconlineshop.com/api/ (Health check)
- http://aeconlineshop.com/api/docs (Interactive API documentation)
- http://aeconlineshop.com/api/products (List products)

---

## 🔧 Quick Commands

```bash
# Test everything at once
source venv/bin/activate && \
python test_import_only.py && \
python test_optimizations.py && \
python test_local_simple.py && \
echo "✅ All basic tests passed!"

# Start server with local database
echo "DATABASE_URL=sqlite:///./test.db" > .env && \
source venv/bin/activate && \
python run_server.py

# Test API endpoints
curl http://localhost:8001/
curl http://localhost:8001/products
curl "http://localhost:8001/products/search?q=test"
```

---

## 🎉 Success Indicators

You'll know everything is working when:

✅ **Import tests pass** - All modules load correctly  
✅ **Optimization tests pass** - Production settings applied  
✅ **Server starts** - No database connection errors  
✅ **Health check works** - `/` returns 200 OK  
✅ **API docs load** - `/docs` shows interactive documentation  
✅ **Endpoints respond** - `/products` returns data  

**Your API is then ready for production! 🚀**

---

## 🆘 Need Help?

1. **Check `LOCAL_TEST_RESULTS.md`** for detailed test results
2. **Check `HOW_TO_TEST.md`** for comprehensive testing guide
3. **Run `python test_everything.py`** for full API testing

**Your Product Management API with Google Lens-like image search is ready to go!**