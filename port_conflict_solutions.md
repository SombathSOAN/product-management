# Port 8000 Conflict Solutions

## Option 1: Find and Kill the Process Using Port 8000
Run these commands in your terminal:

```bash
# Find what's using port 8000
lsof -i :8000

# If you find a process, kill it using its PID
kill -9 <PID>

# Or kill all processes using port 8000
sudo lsof -t -i:8000 | xargs kill -9
```

## Option 2: Use a Different Port
Instead of port 8000, try a different port:

```bash
# Try port 8001
uvicorn product_management:app --host 0.0.0.0 --port 8001

# Or port 8080
uvicorn product_management:app --host 0.0.0.0 --port 8080

# Or port 3000
uvicorn product_management:app --host 0.0.0.0 --port 3000
```

## Option 3: Check for Background Processes
Sometimes processes run in the background. Check for any Python/uvicorn processes:

```bash
# Check for Python processes
ps aux | grep python

# Check for uvicorn processes
ps aux | grep uvicorn

# Kill specific processes if found
kill -9 <PID>
```

## Option 4: Restart Your System
If nothing else works, a system restart will clear all running processes.

## Option 5: Use the Run Server Script
Try using the existing run_server.py script which might handle port conflicts better:

```bash
python run_server.py