#!/usr/bin/env python3
"""
Quick fix script to remove unsupported database parameters
Run this on the server to fix the max_queries error
"""

import re

def fix_database_config():
    """Fix the database configuration in product_management.py"""
    
    # Read the current file
    with open('product_management.py', 'r') as f:
        content = f.read()
    
    # Find and replace the problematic database configuration
    old_config = r'''database = databases\.Database\(
    DATABASE_URL,
    min_size=1,\s*# Minimum connections in pool
    max_size=5,\s*# Maximum connections in pool
    max_queries=50,\s*# Maximum queries per connection
    max_inactive_connection_lifetime=300\s*# 5 minutes
\)'''
    
    new_config = '''database = databases.Database(
    DATABASE_URL,
    min_size=1,      # Minimum connections in pool
    max_size=5       # Maximum connections in pool
)'''
    
    # Replace the configuration
    if 'max_queries' in content:
        print("🔧 Found problematic database configuration...")
        
        # Simple replacement approach
        lines = content.split('\n')
        new_lines = []
        in_database_config = False
        
        for line in lines:
            if 'database = databases.Database(' in line:
                in_database_config = True
                new_lines.append('database = databases.Database(')
                new_lines.append('    DATABASE_URL,')
                new_lines.append('    min_size=1,      # Minimum connections in pool')
                new_lines.append('    max_size=5       # Maximum connections in pool')
                new_lines.append(')')
                continue
            elif in_database_config and line.strip() == ')':
                in_database_config = False
                continue
            elif in_database_config:
                # Skip lines that are part of the old database config
                continue
            else:
                new_lines.append(line)
        
        # Write the fixed content
        with open('product_management.py', 'w') as f:
            f.write('\n'.join(new_lines))
        
        print("✅ Database configuration fixed!")
        print("✅ Removed unsupported 'max_queries' parameter")
        print("✅ Removed unsupported 'max_inactive_connection_lifetime' parameter")
        print("🚀 Server should now start without errors")
        
    else:
        print("✅ Database configuration is already correct!")

if __name__ == "__main__":
    print("🔧 Fixing database configuration...")
    try:
        fix_database_config()
        print("\n🎉 Fix completed successfully!")
        print("Now run: uvicorn product_management:app --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check the file manually")