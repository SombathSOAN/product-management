# 🧪 How to Test Your Product Management API

## 🎯 Testing Options

You have several ways to test your API:

1. **Local Testing** (without database connection)
2. **Remote Testing** (with your shared hosting database)
3. **Production Testing** (on your live server)

---

## 1. 🖥️ Local Testing (Recommended First)

### Quick Environment Tests
```bash
# Activate virtual environment
source venv/bin/activate

# Test 1: Basic imports and dependencies
python test_import_only.py

# Test 2: Production optimizations
python test_optimizations.py

# Test 3: Environment without database
python test_local_simple.py

# Test 4: WSGI configuration
python wsgi.py
```

### Expected Results:
- ✅ All imports successful
- ✅ All optimizations working
- ✅ FastAPI app creation successful
- ✅ Image processing capabilities confirmed

---

## 2. 🌐 Remote Database Testing

### Option A: Test with Your Hosting Database

Create a local environment file to connect to your remote database:

```bash
# Create .env file
cat > .env << EOF
DATABASE_URL=mysql+aiomysql://aeconlin_pm:admindahfh%40pm2025%21%21@192.250.235.86:3306/aeconlin_pmdb
EOF
```

Then run:
```bash
source venv/bin/activate
python run_server.py
```

### Option B: Test with Local SQLite (No Database Setup)

```bash
# Create temporary local database
cat > .env << EOF
DATABASE_URL=sqlite:///./test.db
EOF

source venv/bin/activate
python run_server.py
```

---

## 3. 🚀 Production Testing (On Your Server)

### SSH into Your Server
```bash
ssh aeconlin@192.250.235.86
# Password: jw]abwqg8$J}
```

### Test on Server
```bash
# Navigate to your API directory
cd public_html/api

# Test Python import
python3 -c "
import sys
sys.path.insert(0, '.')
from product_management import app
print('✅ App imported successfully')
print(f'✅ App title: {app.title}')
"

# Test WSGI
python3 wsgi.py
```

---

## 4. 🔧 API Endpoint Testing

### Once Server is Running

#### Health Check Endpoints
```bash
# Test basic health
curl http://localhost:8001/
curl http://localhost:8001/health

# Or on your server
curl http://aeconlineshop.com/api/
curl http://aeconlineshop.com/api/health
```

#### Product Endpoints
```bash
# List products
curl http://localhost:8001/products

# Search products
curl "http://localhost:8001/products/search?q=coffee"

# Get top-rated products
curl http://localhost:8001/products/top-rated
```

#### Image Search Testing
```bash
# Test image search (need a test image)
curl -X POST http://localhost:8001/products/search-by-image \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.jpg"
```

---

## 5. 🖼️ Image Search Testing

### Create Test Image
```bash
# Create a simple test image using Python
python3 -c "
from PIL import Image
img = Image.new('RGB', (200, 200), color='red')
img.save('test_image.jpg')
print('✅ Test image created: test_image.jpg')
"
```

### Test Image Search
```bash
# Basic image search
curl -X POST http://localhost:8001/products/search-by-image \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.jpg"

# High accuracy search
curl -X POST "http://localhost:8001/products/search-by-image?threshold=90" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.jpg"
```

---

## 6. 🌐 Browser Testing

### Open in Browser
```
# Local testing
http://localhost:8001/
http://localhost:8001/docs  # FastAPI documentation

# Production testing
http://aeconlineshop.com/api/
http://aeconlineshop.com/api/docs
```

### Interactive API Documentation
FastAPI automatically generates interactive documentation at `/docs` endpoint where you can:
- See all available endpoints
- Test endpoints directly in browser
- Upload files for image search testing
- View request/response examples

---

## 7. 🧪 Comprehensive Test Script

Create a complete test script:

```bash
# Create comprehensive test
cat > test_everything.py << 'EOF'
#!/usr/bin/env python3
import requests
import time
import json
from PIL import Image
import io

def test_api_comprehensive(base_url="http://localhost:8001"):
    """Comprehensive API testing"""
    print(f"🧪 Testing API at: {base_url}")
    print("=" * 50)
    
    tests = []
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            tests.append(("Health Check", "✅ PASSED"))
            print("✅ Health check: PASSED")
        else:
            tests.append(("Health Check", f"❌ FAILED ({response.status_code})"))
            print(f"❌ Health check: FAILED ({response.status_code})")
    except Exception as e:
        tests.append(("Health Check", f"❌ ERROR: {str(e)}"))
        print(f"❌ Health check: ERROR - {str(e)}")
    
    # Test 2: Products list
    try:
        response = requests.get(f"{base_url}/products", timeout=10)
        if response.status_code == 200:
            products = response.json()
            tests.append(("Products List", f"✅ PASSED ({len(products)} products)"))
            print(f"✅ Products list: PASSED ({len(products)} products)")
        else:
            tests.append(("Products List", f"❌ FAILED ({response.status_code})"))
            print(f"❌ Products list: FAILED ({response.status_code})")
    except Exception as e:
        tests.append(("Products List", f"❌ ERROR: {str(e)}"))
        print(f"❌ Products list: ERROR - {str(e)}")
    
    # Test 3: Search
    try:
        response = requests.get(f"{base_url}/products/search?q=test", timeout=10)
        if response.status_code == 200:
            results = response.json()
            tests.append(("Product Search", f"✅ PASSED ({len(results)} results)"))
            print(f"✅ Product search: PASSED ({len(results)} results)")
        else:
            tests.append(("Product Search", f"❌ FAILED ({response.status_code})"))
            print(f"❌ Product search: FAILED ({response.status_code})")
    except Exception as e:
        tests.append(("Product Search", f"❌ ERROR: {str(e)}"))
        print(f"❌ Product search: ERROR - {str(e)}")
    
    # Test 4: Image search
    try:
        # Create test image
        img = Image.new('RGB', (100, 100), color='blue')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
        response = requests.post(f"{base_url}/products/search-by-image", 
                               files=files, timeout=30)
        
        if response.status_code == 200:
            results = response.json()
            tests.append(("Image Search", f"✅ PASSED ({len(results)} matches)"))
            print(f"✅ Image search: PASSED ({len(results)} matches)")
        else:
            tests.append(("Image Search", f"❌ FAILED ({response.status_code})"))
            print(f"❌ Image search: FAILED ({response.status_code})")
    except Exception as e:
        tests.append(("Image Search", f"❌ ERROR: {str(e)}"))
        print(f"❌ Image search: ERROR - {str(e)}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print("=" * 50)
    for test_name, result in tests:
        print(f"{test_name:20} | {result}")
    
    passed = sum(1 for _, result in tests if "✅ PASSED" in result)
    total = len(tests)
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    import sys
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8001"
    test_api_comprehensive(base_url)
EOF

# Make it executable
chmod +x test_everything.py
```

### Run Comprehensive Test
```bash
# Test locally
source venv/bin/activate
python test_everything.py

# Test production (if server is running)
python test_everything.py http://aeconlineshop.com/api
```

---

## 8. 🎯 Step-by-Step Testing Guide

### Step 1: Basic Local Tests
```bash
source venv/bin/activate
python test_import_only.py
python test_optimizations.py
python test_local_simple.py
```

### Step 2: Start Local Server (Optional)
```bash
# Option A: With your remote database
echo "DATABASE_URL=mysql+aiomysql://aeconlin_pm:admindahfh%40pm2025%21%21@192.250.235.86:3306/aeconlin_pmdb" > .env
python run_server.py

# Option B: With local SQLite
echo "DATABASE_URL=sqlite:///./test.db" > .env
python run_server.py
```

### Step 3: Test Endpoints
```bash
# In another terminal
curl http://localhost:8001/
curl http://localhost:8001/products
curl "http://localhost:8001/products/search?q=test"
```

### Step 4: Test on Production Server
```bash
ssh aeconlin@192.250.235.86
cd public_html/api
python3 wsgi.py
```

### Step 5: Browser Testing
Open: `http://localhost:8001/docs` or `http://aeconlineshop.com/api/docs`

---

## 🔍 Troubleshooting

### Common Issues:

1. **"Module not found"**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **"Database connection failed"**
   - Check if using correct database URL
   - Test with SQLite: `DATABASE_URL=sqlite:///./test.db`

3. **"Port already in use"**
   ```bash
   python run_server.py  # Auto-detects available port
   ```

4. **"Permission denied" on server**
   ```bash
   chmod 755 public_html/api
   chmod 644 public_html/api/*.py
   ```

---

## 🎉 Success Indicators

You'll know everything is working when you see:

✅ **Local Tests:** All import and optimization tests pass  
✅ **Server Start:** Server starts without errors  
✅ **Health Check:** `/` and `/health` endpoints return 200  
✅ **Products:** `/products` returns product list  
✅ **Search:** `/products/search?q=test` returns results  
✅ **Image Search:** `/products/search-by-image` processes images  
✅ **Documentation:** `/docs` shows interactive API docs  

Your API is then ready for production use!