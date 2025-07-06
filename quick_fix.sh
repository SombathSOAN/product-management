#!/bin/bash

echo "🚨 QUICK FIX: Port 8000 Conflict"
echo "================================"

# Kill any process using port 8000
echo "🔍 Finding processes on port 8000..."
PIDS=$(lsof -t -i:8000 2>/dev/null)

if [ ! -z "$PIDS" ]; then
    echo "⚠️  Found processes using port 8000: $PIDS"
    echo "🛑 Killing processes..."
    kill -9 $PIDS 2>/dev/null
    sleep 2
    echo "✅ Port 8000 cleared!"
else
    echo "ℹ️  No processes found on port 8000"
fi

echo ""
echo "🚀 Now you can run:"
echo "   uvicorn product_management:app --host 0.0.0.0 --port 8000"
echo ""
echo "Or use the enhanced server:"
echo "   python run_server.py"