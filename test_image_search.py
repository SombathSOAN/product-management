#!/usr/bin/env python3
"""
Test script for the enhanced image search functionality
This demonstrates how the new Google Lens-like search works
"""

import requests
import json
from pathlib import Path

# API endpoint
BASE_URL = "postgresql://postgres:OoPOlzJfLMJpYCkXqvvfpNHDuoObQzWC@postgres.railway.internal:5432/railway"
SEARCH_ENDPOINT = f"{BASE_URL}/products/search-by-image"

def test_image_search():
    """Test the image search with different parameters"""
    
    print("🔍 Testing Enhanced Image Search (Google Lens-like functionality)")
    print("=" * 60)
    
    # Test parameters
    test_cases = [
        {
            "name": "Strict matching (threshold=10)",
            "params": {"threshold": 10, "max_results": 5, "use_advanced_matching": True}
        },
        {
            "name": "Moderate matching (threshold=20)", 
            "params": {"threshold": 20, "max_results": 10, "use_advanced_matching": True}
        },
        {
            "name": "Loose matching (threshold=30)",
            "params": {"threshold": 30, "max_results": 15, "use_advanced_matching": True}
        },
        {
            "name": "Basic matching only",
            "params": {"threshold": 20, "max_results": 10, "use_advanced_matching": False}
        }
    ]
    
    # You would need to provide an actual image file for testing
    # For now, we'll show how to use it
    print("📝 Usage Instructions:")
    print("1. Start your FastAPI server: uvicorn product_management:app --reload")
    print("2. Use curl or a tool like Postman to test:")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. {test_case['name']}:")
        params_str = "&".join([f"{k}={v}" for k, v in test_case['params'].items()])
        print(f"   curl -X POST '{SEARCH_ENDPOINT}?{params_str}' \\")
        print(f"        -H 'Content-Type: multipart/form-data' \\")
        print(f"        -F 'file=@your_image.jpg'")
        print()
    
    print("🚀 Key Features of the Enhanced Search:")
    print("• Multiple hash algorithms (perceptual, difference, wavelet)")
    print("• Color histogram matching for color-based similarity")
    print("• Edge detection for shape matching")
    print("• Async processing for better performance")
    print("• Batch processing to handle large product catalogs")
    print("• Confidence scoring (0-100%)")
    print("• Smart caching and error handling")
    print()
    
    print("📊 API Parameters:")
    print("• threshold: Similarity threshold (0-50, lower = more strict)")
    print("• max_results: Maximum number of results (1-50)")
    print("• use_advanced_matching: Enable color/edge matching (true/false)")
    print()
    
    print("🎯 Expected Response Format:")
    response_example = {
        "products": [
            {
                "id": "product-123",
                "name": "Sample Product",
                "price": 29.99,
                "thumbnail_url": "https://example.com/image.jpg",
                "similarity_score": 85.5,
                "tags": ["electronics", "gadget"]
            }
        ],
        "search_time": "2.34s",
        "total_compared": 150,
        "matches_found": 5
    }
    
    print(json.dumps(response_example, indent=2))

def check_server_status():
    """Check if the server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running!")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Server is not running: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Image Search Test Suite")
    print("=" * 40)
    
    if check_server_status():
        test_image_search()
    else:
        print("\n💡 To start the server, run:")
        print("uvicorn product_management:app --reload")
        print("\nThen run this test script again.")