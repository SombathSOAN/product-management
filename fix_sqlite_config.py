#!/usr/bin/env python3
"""
Fix SQLite database configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local_products.db")

print(f"Current DATABASE_URL: {DATABASE_URL}")

if DATABASE_URL.startswith("sqlite"):
    print("✅ Using SQLite - creating simple database configuration")
    
    # Create a simple SQLite-compatible version
    with open("product_management_sqlite.py", "w") as f:
        with open("product_management.py", "r") as original:
            content = original.read()
            
            # Replace the database configuration for SQLite
            old_config = '''database = databases.Database(
    DATABASE_URL,
    min_size=1,      # Minimum connections in pool
    max_size=5       # Maximum connections in pool
)'''
            
            new_config = '''# SQLite doesn't support connection pooling parameters
if DATABASE_URL.startswith("sqlite"):
    database = databases.Database(DATABASE_URL)
else:
    database = databases.Database(
        DATABASE_URL,
        min_size=1,      # Minimum connections in pool
        max_size=5       # Maximum connections in pool
    )'''
            
            content = content.replace(old_config, new_config)
            f.write(content)
    
    print("✅ Created product_management_sqlite.py with SQLite support")
    print("🚀 Now you can run: uvicorn product_management_sqlite:app --host 127.0.0.1 --port 8001")
else:
    print("ℹ️  Not using SQLite, no changes needed")