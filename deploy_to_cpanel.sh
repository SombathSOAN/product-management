#!/bin/bash

echo "🚀 Deploying Product Management API to cPanel Shared Hosting"
echo "============================================================"

# Configuration
REMOTE_HOST="192.250.235.86"
REMOTE_USER="aeconlin"
REMOTE_PATH="/home/aeconlin/public_html/api"
LOCAL_PATH="."

echo "📋 Deployment Configuration:"
echo "   Remote Host: $REMOTE_HOST"
echo "   Remote User: $REMOTE_USER"
echo "   Remote Path: $REMOTE_PATH"
echo "   Local Path: $LOCAL_PATH"
echo ""

# Function to upload files via SCP
upload_files() {
    echo "📤 Uploading files to shared hosting..."
    
    # Create remote directory if it doesn't exist
    ssh $REMOTE_USER@$REMOTE_HOST "mkdir -p $REMOTE_PATH"
    
    # Upload Python files
    echo "   📄 Uploading Python application files..."
    scp product_management.py $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/
    scp wsgi.py $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/
    scp requirements.txt $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/
    scp .htaccess $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/
    
    # Upload configuration files
    echo "   ⚙️  Uploading configuration files..."
    scp .env.example $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/
    
    # Upload any additional Python modules
    if [ -f "__init__.py" ]; then
        scp __init__.py $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/
    fi
    
    echo "✅ File upload completed!"
}

# Function to set up remote environment
setup_remote() {
    echo "🔧 Setting up remote environment..."
    
    ssh $REMOTE_USER@$REMOTE_HOST << 'EOF'
        cd /home/aeconlin/public_html/api
        
        # Set proper permissions
        chmod 755 wsgi.py
        chmod 644 product_management.py
        chmod 644 .htaccess
        chmod 644 requirements.txt
        
        # Create environment file if it doesn't exist
        if [ ! -f .env ]; then
            cp .env.example .env
            echo "DATABASE_URL=sqlite:///./product_management.db" >> .env
            echo "ENVIRONMENT=production" >> .env
        fi
        
        # Test Python import
        echo "🧪 Testing Python imports..."
        python3 -c "
import sys
print('Python version:', sys.version)
try:
    import fastapi
    print('✅ FastAPI available')
except ImportError:
    print('❌ FastAPI not available - may need to install')
try:
    import sqlite3
    print('✅ SQLite available')
except ImportError:
    print('❌ SQLite not available')
"
        
        echo "✅ Remote setup completed!"
EOF
}

# Function to test deployment
test_deployment() {
    echo "🧪 Testing deployment..."
    
    # Test WSGI file directly
    echo "   📋 Testing WSGI application..."
    ssh $REMOTE_USER@$REMOTE_HOST "cd /home/aeconlin/public_html/api && python3 wsgi.py"
    
    # Test web access (if curl is available)
    echo "   🌐 Testing web access..."
    if command -v curl &> /dev/null; then
        echo "   Trying: http://aeconlineshop.com/api/health"
        curl -s -o /dev/null -w "%{http_code}" http://aeconlineshop.com/api/health
        echo ""
    fi
}

# Main deployment process
main() {
    echo "🚀 Starting deployment process..."
    echo ""
    
    # Skip SSH key check for password-based authentication
    echo "🔐 Using password-based SSH authentication"
    echo "💡 You'll be prompted for your password during file transfers"
    
    echo ""
    upload_files
    echo ""
    setup_remote
    echo ""
    test_deployment
    
    echo ""
    echo "🎉 Deployment completed!"
    echo ""
    echo "📋 Next Steps:"
    echo "   1. Visit: http://aeconlineshop.com/api/docs"
    echo "   2. Test: http://aeconlineshop.com/api/health"
    echo "   3. Check cPanel error logs if issues occur"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "   - Check cPanel Error Logs"
    echo "   - Verify Python modules are installed"
    echo "   - Ensure file permissions are correct"
    echo ""
}

# Run deployment
main