#!/usr/bin/env python3
"""
Comprehensive API Testing Script
Tests all major functionality of the Product Management API
"""
import requests
import time
import json
from PIL import Image
import io
import sys

def test_api_comprehensive(base_url="http://localhost:8001"):
    """Comprehensive API testing"""
    print(f"🧪 Testing API at: {base_url}")
    print("=" * 50)
    
    tests = []
    
    # Test 1: Health check
    print("1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            tests.append(("Health Check", "✅ PASSED"))
            print(f"✅ Health check: PASSED - {data.get('message', 'OK')}")
        else:
            tests.append(("Health Check", f"❌ FAILED ({response.status_code})"))
            print(f"❌ Health check: FAILED ({response.status_code})")
    except Exception as e:
        tests.append(("Health Check", f"❌ ERROR: {str(e)}"))
        print(f"❌ Health check: ERROR - {str(e)}")
    
    # Test 2: Health endpoint
    print("\n2️⃣ Testing Health Endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            tests.append(("Health Endpoint", "✅ PASSED"))
            print(f"✅ Health endpoint: PASSED - {data.get('status', 'OK')}")
        else:
            tests.append(("Health Endpoint", f"❌ FAILED ({response.status_code})"))
            print(f"❌ Health endpoint: FAILED ({response.status_code})")
    except Exception as e:
        tests.append(("Health Endpoint", f"❌ ERROR: {str(e)}"))
        print(f"❌ Health endpoint: ERROR - {str(e)}")
    
    # Test 3: Products list
    print("\n3️⃣ Testing Products List...")
    try:
        response = requests.get(f"{base_url}/products", timeout=10)
        if response.status_code == 200:
            products = response.json()
            tests.append(("Products List", f"✅ PASSED ({len(products)} products)"))
            print(f"✅ Products list: PASSED ({len(products)} products)")
            
            # Show sample product if available
            if products:
                sample = products[0]
                print(f"   📦 Sample product: {sample.get('name', 'N/A')}")
                print(f"   💰 Price: ${sample.get('price', 'N/A')}")
        else:
            tests.append(("Products List", f"❌ FAILED ({response.status_code})"))
            print(f"❌ Products list: FAILED ({response.status_code})")
            if response.text:
                print(f"   Error: {response.text[:200]}")
    except Exception as e:
        tests.append(("Products List", f"❌ ERROR: {str(e)}"))
        print(f"❌ Products list: ERROR - {str(e)}")
    
    # Test 4: Product search
    print("\n4️⃣ Testing Product Search...")
    try:
        response = requests.get(f"{base_url}/products/search?q=test", timeout=10)
        if response.status_code == 200:
            results = response.json()
            tests.append(("Product Search", f"✅ PASSED ({len(results)} results)"))
            print(f"✅ Product search: PASSED ({len(results)} results)")
        else:
            tests.append(("Product Search", f"❌ FAILED ({response.status_code})"))
            print(f"❌ Product search: FAILED ({response.status_code})")
            if response.text:
                print(f"   Error: {response.text[:200]}")
    except Exception as e:
        tests.append(("Product Search", f"❌ ERROR: {str(e)}"))
        print(f"❌ Product search: ERROR - {str(e)}")
    
    # Test 5: Top-rated products
    print("\n5️⃣ Testing Top-Rated Products...")
    try:
        response = requests.get(f"{base_url}/products/top-rated", timeout=10)
        if response.status_code == 200:
            results = response.json()
            tests.append(("Top-Rated Products", f"✅ PASSED ({len(results)} products)"))
            print(f"✅ Top-rated products: PASSED ({len(results)} products)")
        else:
            tests.append(("Top-Rated Products", f"❌ FAILED ({response.status_code})"))
            print(f"❌ Top-rated products: FAILED ({response.status_code})")
    except Exception as e:
        tests.append(("Top-Rated Products", f"❌ ERROR: {str(e)}"))
        print(f"❌ Top-rated products: ERROR - {str(e)}")
    
    # Test 6: Image search
    print("\n6️⃣ Testing Image Search...")
    try:
        # Create test image
        print("   📸 Creating test image...")
        img = Image.new('RGB', (100, 100), color='blue')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
        print("   🔍 Uploading image for search...")
        response = requests.post(f"{base_url}/products/search-by-image", 
                               files=files, timeout=30)
        
        if response.status_code == 200:
            results = response.json()
            tests.append(("Image Search", f"✅ PASSED ({len(results)} matches)"))
            print(f"✅ Image search: PASSED ({len(results)} matches)")
            
            # Show top match if available
            if results:
                top_match = results[0]
                print(f"   🎯 Top match: {top_match.get('name', 'N/A')}")
        else:
            tests.append(("Image Search", f"❌ FAILED ({response.status_code})"))
            print(f"❌ Image search: FAILED ({response.status_code})")
            if response.text:
                print(f"   Error: {response.text[:200]}")
    except Exception as e:
        tests.append(("Image Search", f"❌ ERROR: {str(e)}"))
        print(f"❌ Image search: ERROR - {str(e)}")
    
    # Test 7: Banners
    print("\n7️⃣ Testing Banners...")
    try:
        response = requests.get(f"{base_url}/banners", timeout=10)
        if response.status_code == 200:
            banners = response.json()
            tests.append(("Banners", f"✅ PASSED ({len(banners)} banners)"))
            print(f"✅ Banners: PASSED ({len(banners)} banners)")
        else:
            tests.append(("Banners", f"❌ FAILED ({response.status_code})"))
            print(f"❌ Banners: FAILED ({response.status_code})")
    except Exception as e:
        tests.append(("Banners", f"❌ ERROR: {str(e)}"))
        print(f"❌ Banners: ERROR - {str(e)}")
    
    # Test 8: Reviews
    print("\n8️⃣ Testing Reviews...")
    try:
        response = requests.get(f"{base_url}/reviews", timeout=10)
        if response.status_code == 200:
            reviews = response.json()
            tests.append(("Reviews", f"✅ PASSED ({len(reviews)} reviews)"))
            print(f"✅ Reviews: PASSED ({len(reviews)} reviews)")
        else:
            tests.append(("Reviews", f"❌ FAILED ({response.status_code})"))
            print(f"❌ Reviews: FAILED ({response.status_code})")
    except Exception as e:
        tests.append(("Reviews", f"❌ ERROR: {str(e)}"))
        print(f"❌ Reviews: ERROR - {str(e)}")
    
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
        print("🚀 Your API is ready for production!")
    elif passed >= total * 0.75:
        print("✅ Most tests passed! API is mostly functional.")
        print("⚠️  Check failed tests above for issues.")
    else:
        print("⚠️  Many tests failed. Check the errors above.")
        print("🔧 API may need troubleshooting.")
    
    return passed, total

def create_test_image():
    """Create a test image for image search testing"""
    try:
        img = Image.new('RGB', (200, 200), color='red')
        img.save('test_image.jpg')
        print("✅ Test image created: test_image.jpg")
        return True
    except Exception as e:
        print(f"❌ Failed to create test image: {e}")
        return False

def main():
    """Main function"""
    print("🧪 Product Management API - Comprehensive Test Suite")
    print("=" * 60)
    
    # Get base URL from command line or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8001"
    
    print(f"🎯 Target URL: {base_url}")
    print(f"⏰ Starting tests at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create test image
    print("\n📸 Preparing test resources...")
    create_test_image()
    
    # Run comprehensive tests
    passed, total = test_api_comprehensive(base_url)
    
    # Final summary
    print("\n" + "=" * 60)
    print("🏁 Final Results:")
    print("=" * 60)
    print(f"✅ Tests Passed: {passed}")
    print(f"❌ Tests Failed: {total - passed}")
    print(f"📊 Success Rate: {(passed/total)*100:.1f}%")
    print(f"⏰ Completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if passed == total:
        print("\n🎉 CONGRATULATIONS!")
        print("Your Product Management API is fully functional!")
        print("🚀 Ready for production deployment!")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)