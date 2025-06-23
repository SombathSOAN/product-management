#!/usr/bin/env python3
"""
Test script to verify that the main module can be imported correctly.
This helps debug import issues before deployment.
"""

import sys
import os

print("=== Import Test ===")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Files in current directory: {sorted(os.listdir('.'))}")
print(f"Python path: {sys.path[:3]}...")  # Show first 3 entries

try:
    print("\n1. Testing direct import of product_management...")
    import product_management
    print("✓ product_management imported successfully")
    
    print("\n2. Testing app import from product_management...")
    from product_management import app
    print("✓ app imported successfully")
    print(f"App type: {type(app)}")
    
    print("\n3. Testing main module import...")
    import main
    print("✓ main module imported successfully")
    
    print("\n4. Testing app import from main...")
    from main import app as main_app
    print("✓ app imported from main successfully")
    print(f"Main app type: {type(main_app)}")
    
    print("\n=== All imports successful! ===")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Error type: {type(e)}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print(f"Error type: {type(e)}")
    sys.exit(1)