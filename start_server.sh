#!/bin/bash

echo "🔧 Product Management Server Startup Script"
echo "=========================================="

# Function to kill processes on port 8000
kill_port_8000() {
    echo "🔍 Checking for processes on port 8000..."
    PIDS=$(lsof -t -i:8000 2>/dev/null)
    if [ ! -z "$PIDS" ]; then
        echo "⚠️  Found processes using port 8000: $PIDS"
        echo "🛑 Killing processes..."
        kill -9 $PIDS
        sleep 2
        echo "✅ Port 8000 cleared"
    else
        echo "✅ Port 8000 is free"
    fi
}

# Function to start server with automatic port detection
start_server() {
    echo ""
    echo "🚀 Starting Product Management Server..."
    echo "📡 Using automatic port detection"
    echo ""
    
    # Use the enhanced run_server.py which handles port conflicts
    python run_server.py
}

# Main execution
echo ""
echo "Choose an option:"
echo "1) Clear port 8000 and start server"
echo "2) Start server with automatic port detection (recommended)"
echo "3) Start server on specific port"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        kill_port_8000
        echo "PORT=8000" > .env.local
        start_server
        ;;
    2)
        start_server
        ;;
    3)
        read -p "Enter port number: " custom_port
        echo "PORT=$custom_port" > .env.local
        start_server
        ;;
    *)
        echo "❌ Invalid choice. Using automatic port detection..."
        start_server
        ;;
esac