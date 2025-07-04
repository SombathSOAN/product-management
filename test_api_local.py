#!/usr/bin/env python3
"""
Test script to run the API locally with a mock database for testing purposes.
"""

import os
import sys
import asyncio
from fastapi.testclient import TestClient

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set a local database URL for testing
os.environ["DATABASE_URL"] = "postgresql://postgres:OoPOlzJfLMJpYCkXqvvfpNHDuoObQzWC@postgres.railway.internal:5432/railway"

try:
    from main import app
    
    # Create test client
    client = TestClient(app)
    
    print("=== API Local Test ===")
    print("Testing API endpoints locally...")
    
    # Test health endpoint
    print("\n1. Testing /health endpoint...")
    try:
        response = client.get("/health")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test root endpoint
    print("\n2. Testing / endpoint...")
    try:
        response = client.get("/")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test products endpoint
    print("\n3. Testing /products endpoint...")
    try:
        response = client.get("/products")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            products = response.json()
            print(f"   Found {len(products)} products")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n✅ Local API test completed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

    # Test search by image endpoint
    print("\n4. Testing /products/search-by-image endpoint...")
    try:
        with open("test_image.jpg", "rb") as image_file:  # Ensure you have a test image in the directory
            response = client.post("/products/search-by-image", files={"file": ("test_image.jpg", image_file, "image/jpeg")})
            print(f"   Status Code: {response.status_code}")
            if response.status_code == 200:
                results = response.json()
                print(f"   Found {len(results)} similar products")
            else:
                print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n✅ Local API test completed!")