#!/usr/bin/env python3
"""
Test script to verify that the main module can be imported without database connection.
"""

import os
import sys

# Temporarily set a dummy DATABASE_URL to avoid connection errors during import
os.environ['DATABASE_URL'] = 'postgresql://dummy:dummy@localhost:5432/dummy'

try:
    # Add current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Test import
    import main
    print("✅ Successfully imported main module")
    print(f"✅ App object exists: {hasattr(main, 'app')}")
    print(f"✅ App type: {type(main.app)}")
    
    # Test the app object
    if hasattr(main, 'app'):
        print(f"✅ App title: {main.app.title}")
        print("✅ Import test passed - ready for deployment")
    else:
        print("❌ App object not found in main module")
        sys.exit(1)
        
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Other error: {e}")
    sys.exit(1)