# Manual Fix for Database Configuration Error

## Problem
The server is failing to start with this error:
```
TypeError: connect() got an unexpected keyword argument 'max_queries'
```

## Quick Fix (Copy and Paste on Server)

**Step 1**: Navigate to your project and activate environment
```bash
cd product-management
source /home/aeconlin/virtualenv/product-management/3.9/bin/activate
```

**Step 2**: Edit the product_management.py file
```bash
nano product_management.py
```

**Step 3**: Find this section (around line 50-57):
```python
database = databases.Database(
    DATABASE_URL,
    min_size=1,      # Minimum connections in pool
    max_size=5,      # Maximum connections in pool
    max_queries=50,  # Maximum queries per connection
    max_inactive_connection_lifetime=300  # 5 minutes
)
```

**Step 4**: Replace it with this:
```python
database = databases.Database(
    DATABASE_URL,
    min_size=1,      # Minimum connections in pool
    max_size=5       # Maximum connections in pool
)
```

**Step 5**: Save and exit nano
- Press `Ctrl + X`
- Press `Y` to confirm
- Press `Enter` to save

**Step 6**: Test the server
```bash
uvicorn product_management:app --host 0.0.0.0 --port 8000
```

## Alternative: One-Line Fix

If you prefer a command-line approach:

```bash
sed -i '/max_queries=50/d' product_management.py
sed -i '/max_inactive_connection_lifetime=300/d' product_management.py
```

## What This Fixes

- ✅ Removes unsupported `max_queries` parameter
- ✅ Removes unsupported `max_inactive_connection_lifetime` parameter  
- ✅ Keeps the essential connection pool optimization (min_size=1, max_size=5)
- ✅ Maintains all thread optimization settings

After this fix, your server should start successfully! 🚀