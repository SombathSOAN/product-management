# 🚨 GIT CONFLICT RESOLUTION - EXACT COMMANDS

## Current Situation
You're stuck in a git merge conflict. Let's resolve it step by step.

## EXACT COMMANDS TO RUN:

### Step 1: Check Current Status
```bash
git status
```

### Step 2: Resolve the Conflict by Keeping Clean Version
```bash
# Remove the conflicted passenger_wsgi.py and use the clean one
git checkout --ours passenger_wsgi.py
```

### Step 3: Add the Resolved File
```bash
git add passenger_wsgi.py
```

### Step 4: Complete the Merge
```bash
git commit -m "Resolve merge conflict: keep clean passenger_wsgi.py"
```

### Step 5: Test the Fixed File
```bash
python3 passenger_wsgi.py
```
**Expected**: Should run quietly without any output (that's success!)

### Step 6: Restart Your Application
```bash
touch tmp/restart.txt
```

### Step 7: Test Your API
```bash
curl -I http://aeconlineshop.com/api/health
```

## Alternative: If Above Doesn't Work

### Nuclear Option - Reset and Use Clean File
```bash
# Abort the current merge
git merge --abort

# Pull fresh from main
git pull origin main

# Test the file
python3 passenger_wsgi.py

# Restart app
touch tmp/restart.txt
```

## What Should Happen
1. `python3 passenger_wsgi.py` runs quietly (no output = success)
2. Your API becomes accessible at http://aeconlineshop.com/api/
3. No more port 8000 conflicts

Run these commands in order and let me know what happens!