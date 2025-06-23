#!/usr/bin/env python3
"""
Railway Deployment Monitor and API Tester
This script monitors the Railway deployment and tests all API endpoints.
"""

import requests
import json
import time
from datetime import datetime
import sys

# Railway deployment URL
RAILWAY_URL = "https://product-management-production.up.railway.app"

def test_endpoint(url, method="GET", data=None, timeout=10):
    """Test a single endpoint and return detailed results"""
    try:
        start_time = time.time()
        
        if method == "GET":
            response = requests.get(url, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=timeout)
        
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds
        
        return {
            "url": url,
            "method": method,
            "status_code": response.status_code,
            "response_time_ms": response_time,
            "success": 200 <= response.status_code < 300,
            "response_body": response.text[:500] if response.text else "",  # First 500 chars
            "headers": dict(response.headers),
            "error": None
        }
    except requests.exceptions.Timeout:
        return {
            "url": url,
            "method": method,
            "status_code": None,
            "response_time_ms": None,
            "success": False,
            "response_body": "",
            "headers": {},
            "error": "Request timeout"
        }
    except requests.exceptions.ConnectionError:
        return {
            "url": url,
            "method": method,
            "status_code": None,
            "response_time_ms": None,
            "success": False,
            "response_body": "",
            "headers": {},
            "error": "Connection error - service may be down"
        }
    except Exception as e:
        return {
            "url": url,
            "method": method,
            "status_code": None,
            "response_time_ms": None,
            "success": False,
            "response_body": "",
            "headers": {},
            "error": str(e)
        }

def print_test_result(result):
    """Print formatted test result"""
    status_icon = "✅" if result["success"] else "❌"
    print(f"{status_icon} {result['method']} {result['url']}")
    print(f"   Status: {result['status_code'] or 'N/A'}")
    if result["response_time_ms"]:
        print(f"   Response Time: {result['response_time_ms']}ms")
    if result["error"]:
        print(f"   Error: {result['error']}")
    if result["response_body"]:
        try:
            # Try to parse as JSON for better formatting
            json_body = json.loads(result["response_body"])
            print(f"   Response: {json.dumps(json_body, indent=2)[:200]}...")
        except:
            print(f"   Response: {result['response_body'][:200]}...")
    print()

def monitor_railway_deployment():
    """Monitor Railway deployment and test all endpoints"""
    print("=" * 60)
    print("RAILWAY DEPLOYMENT MONITOR")
    print("=" * 60)
    print(f"Target URL: {RAILWAY_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Define endpoints to test
    endpoints = [
        {"url": f"{RAILWAY_URL}/", "method": "GET", "description": "Root endpoint"},
        {"url": f"{RAILWAY_URL}/health", "method": "GET", "description": "Health check"},
        {"url": f"{RAILWAY_URL}/docs", "method": "GET", "description": "API documentation"},
        {"url": f"{RAILWAY_URL}/products", "method": "GET", "description": "List products"},
        {"url": f"{RAILWAY_URL}/products/search?q=test", "method": "GET", "description": "Search products"},
        {"url": f"{RAILWAY_URL}/banners", "method": "GET", "description": "List banners"},
    ]
    
    results = []
    successful_tests = 0
    
    print("TESTING ENDPOINTS:")
    print("-" * 40)
    
    for endpoint in endpoints:
        print(f"Testing: {endpoint['description']}")
        result = test_endpoint(endpoint["url"], endpoint["method"])
        print_test_result(result)
        results.append(result)
        
        if result["success"]:
            successful_tests += 1
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {len(endpoints)}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {len(endpoints) - successful_tests}")
    print(f"Success Rate: {(successful_tests / len(endpoints)) * 100:.1f}%")
    
    if successful_tests == 0:
        print("\n🚨 DEPLOYMENT ISSUE DETECTED:")
        print("- No endpoints are responding successfully")
        print("- The Railway deployment may be down or misconfigured")
        print("- Check Railway dashboard for deployment logs")
        print("- Verify the deployment URL is correct")
    elif successful_tests < len(endpoints):
        print(f"\n⚠️  PARTIAL DEPLOYMENT ISSUES:")
        print(f"- {len(endpoints) - successful_tests} endpoints are failing")
        print("- Some functionality may not be working correctly")
    else:
        print("\n✅ ALL TESTS PASSED:")
        print("- Railway deployment is working correctly")
        print("- All API endpoints are responding")
    
    return results

def continuous_monitoring(interval_seconds=30, max_iterations=10):
    """Run continuous monitoring for a specified duration"""
    print(f"Starting continuous monitoring (every {interval_seconds}s, max {max_iterations} iterations)")
    print("Press Ctrl+C to stop early")
    print()
    
    try:
        for i in range(max_iterations):
            print(f"MONITORING ITERATION {i + 1}/{max_iterations}")
            results = monitor_railway_deployment()
            
            if i < max_iterations - 1:  # Don't sleep after the last iteration
                print(f"Waiting {interval_seconds} seconds before next check...")
                time.sleep(interval_seconds)
                print()
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        continuous_monitoring()
    else:
        monitor_railway_deployment()