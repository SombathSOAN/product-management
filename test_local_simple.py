#!/usr/bin/env python3
"""
Simple local test without database connection
"""
import sys
import os

def test_basic_imports():
    """Test basic imports without database connection"""
    print("🧪 Testing basic imports...")
    
    try:
        # Test FastAPI import
        from fastapi import FastAPI
        print("✅ FastAPI imported successfully")
        
        # Test other core dependencies
        import uvicorn
        print("✅ Uvicorn imported successfully")
        
        import databases
        print("✅ Databases imported successfully")
        
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
        
        import aiohttp
        print("✅ Aiohttp imported successfully")
        
        import PIL
        print("✅ PIL imported successfully")
        
        import imagehash
        print("✅ ImageHash imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_app_creation():
    """Test creating FastAPI app without database"""
    print("\n🚀 Testing FastAPI app creation...")
    
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        # Create a simple test app
        test_app = FastAPI(title="Test API")
        
        # Add CORS
        test_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Add a simple endpoint
        @test_app.get("/")
        async def root():
            return {"message": "Test API is working"}
        
        @test_app.get("/health")
        async def health():
            return {"status": "healthy"}
        
        print("✅ FastAPI app created successfully")
        print("✅ CORS middleware added")
        print("✅ Test endpoints added")
        
        return True
        
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        return False

def test_image_processing():
    """Test image processing capabilities"""
    print("\n🖼️  Testing image processing...")
    
    try:
        from PIL import Image
        import imagehash
        import io
        
        # Create a simple test image
        test_image = Image.new('RGB', (100, 100), color='red')
        
        # Test image hash
        hash_value = imagehash.phash(test_image)
        print(f"✅ Image hash generated: {hash_value}")
        
        # Test image conversion
        if test_image.mode != 'RGB':
            test_image = test_image.convert('RGB')
        print("✅ Image conversion works")
        
        # Test BytesIO
        img_bytes = io.BytesIO()
        test_image.save(img_bytes, format='JPEG')
        print("✅ Image to bytes conversion works")
        
        return True
        
    except Exception as e:
        print(f"❌ Image processing failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔧 Local Environment Test (No Database)")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("FastAPI App Creation", test_app_creation),
        ("Image Processing", test_image_processing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All local tests passed!")
        print("🚀 Your environment is ready for deployment!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)