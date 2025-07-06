#!/bin/bash

# 🚀 One-Click Deployment Script for Product Management API
# This script automates the entire deployment process on your server

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/home/aeconlin/product-management"
VENV_PATH="/home/aeconlin/virtualenv/product-management/3.9"
SERVICE_NAME="product-management"
NGINX_SITE="e-catalog.dahoughengenterprise.com"
PORT="8010"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Function to check if running as correct user
check_user() {
    if [ "$USER" != "aeconlin" ]; then
        print_error "This script should be run as user 'aeconlin'"
        print_error "Current user: $USER"
        exit 1
    fi
}

# Function to pull latest code
pull_code() {
    print_header "Pulling Latest Code from Git"
    
    cd "$PROJECT_DIR"
    
    print_status "Current directory: $(pwd)"
    print_status "Pulling from origin main..."
    
    git pull origin main
    
    print_status "Latest commits:"
    git log --oneline -3
    
    print_status "✅ Code updated successfully"
}

# Function to update dependencies
update_dependencies() {
    print_header "Updating Dependencies"
    
    cd "$PROJECT_DIR"
    
    print_status "Activating virtual environment..."
    source "$VENV_PATH/bin/activate"
    
    print_status "Current Python: $(which python)"
    print_status "Current pip: $(which pip)"
    
    print_status "Installing/updating requirements..."
    pip install -r requirements.txt
    
    print_status "Installing production dependencies..."
    pip install gunicorn uvicorn[standard]
    
    print_status "✅ Dependencies updated successfully"
}

# Function to test the application
test_application() {
    print_header "Testing Application"
    
    cd "$PROJECT_DIR"
    source "$VENV_PATH/bin/activate"
    
    print_status "Testing imports..."
    if python -c "from product_management import app; print('✅ Import successful')"; then
        print_status "✅ Application imports successfully"
    else
        print_error "❌ Application import failed"
        return 1
    fi
    
    print_status "Testing database connection..."
    if python -c "
import os
from dotenv import load_dotenv
load_dotenv()
db_url = os.getenv('DATABASE_URL', 'sqlite:///./products.db')
print(f'Database URL: {db_url}')
print('✅ Database configuration loaded')
"; then
        print_status "✅ Database configuration valid"
    else
        print_error "❌ Database configuration failed"
        return 1
    fi
}

# Function to restart the service
restart_service() {
    print_header "Restarting Service"
    
    # Check if systemd service exists
    if systemctl list-unit-files | grep -q "$SERVICE_NAME.service"; then
        print_status "Restarting systemd service..."
        sudo systemctl restart "$SERVICE_NAME"
        sleep 3
        
        if sudo systemctl is-active --quiet "$SERVICE_NAME"; then
            print_status "✅ Service restarted successfully"
            sudo systemctl status "$SERVICE_NAME" --no-pager -l
        else
            print_error "❌ Service failed to start"
            sudo systemctl status "$SERVICE_NAME" --no-pager -l
            return 1
        fi
    else
        print_warning "Systemd service not found. Starting manually..."
        
        # Kill existing processes
        print_status "Stopping existing Gunicorn processes..."
        pkill -f gunicorn || true
        sleep 2
        
        # Start new process
        print_status "Starting Gunicorn..."
        cd "$PROJECT_DIR"
        source "$VENV_PATH/bin/activate"
        
        nohup gunicorn product_management:app \
            -w 4 \
            -k uvicorn.workers.UvicornWorker \
            --bind "0.0.0.0:$PORT" \
            --access-logfile gunicorn-access.log \
            --error-logfile gunicorn-error.log \
            > gunicorn.log 2>&1 &
        
        sleep 3
        print_status "✅ Gunicorn started manually"
    fi
}

# Function to test deployment
test_deployment() {
    print_header "Testing Deployment"
    
    print_status "Testing local endpoint..."
    if curl -s "http://localhost:$PORT/" | grep -q "Product Management API"; then
        print_status "✅ Local endpoint responding"
    else
        print_error "❌ Local endpoint not responding"
        return 1
    fi
    
    print_status "Testing domain endpoint..."
    if curl -s "http://$NGINX_SITE/" | grep -q "Product Management API"; then
        print_status "✅ Domain endpoint responding"
    else
        print_warning "⚠️ Domain endpoint not responding (check Nginx configuration)"
    fi
    
    print_status "Testing API endpoints..."
    local base_url="http://localhost:$PORT"
    
    # Test products endpoint
    if curl -s "$base_url/products" >/dev/null; then
        print_status "✅ Products endpoint working"
    else
        print_error "❌ Products endpoint failed"
    fi
    
    # Test health endpoint
    if curl -s "$base_url/health" >/dev/null; then
        print_status "✅ Health endpoint working"
    else
        print_error "❌ Health endpoint failed"
    fi
}

# Function to show deployment status
show_status() {
    print_header "Deployment Status"
    
    print_status "Service Status:"
    if systemctl list-unit-files | grep -q "$SERVICE_NAME.service"; then
        sudo systemctl status "$SERVICE_NAME" --no-pager -l
    else
        print_warning "No systemd service configured"
        print_status "Checking manual processes:"
        ps aux | grep gunicorn | grep -v grep || print_warning "No Gunicorn processes found"
    fi
    
    print_status "Port Status:"
    if lsof -i ":$PORT" >/dev/null 2>&1; then
        print_status "✅ Port $PORT is in use"
        lsof -i ":$PORT"
    else
        print_error "❌ Port $PORT is not in use"
    fi
    
    print_status "Recent Logs:"
    if systemctl list-unit-files | grep -q "$SERVICE_NAME.service"; then
        sudo journalctl -u "$SERVICE_NAME" --since "5 minutes ago" --no-pager -l
    else
        if [ -f "$PROJECT_DIR/gunicorn.log" ]; then
            tail -20 "$PROJECT_DIR/gunicorn.log"
        fi
    fi
}

# Function to setup systemd service
setup_systemd() {
    print_header "Setting Up Systemd Service"
    
    if [ ! -f "$PROJECT_DIR/product-management.service" ]; then
        print_error "Service file not found: $PROJECT_DIR/product-management.service"
        return 1
    fi
    
    print_status "Copying service file..."
    sudo cp "$PROJECT_DIR/product-management.service" "/etc/systemd/system/"
    
    print_status "Reloading systemd daemon..."
    sudo systemctl daemon-reload
    
    print_status "Enabling service..."
    sudo systemctl enable "$SERVICE_NAME"
    
    print_status "Starting service..."
    sudo systemctl start "$SERVICE_NAME"
    
    print_status "✅ Systemd service configured"
}

# Function to setup nginx
setup_nginx() {
    print_header "Setting Up Nginx Configuration"
    
    if [ ! -f "$PROJECT_DIR/nginx-site.conf" ]; then
        print_error "Nginx config file not found: $PROJECT_DIR/nginx-site.conf"
        return 1
    fi
    
    print_status "Copying Nginx configuration..."
    sudo cp "$PROJECT_DIR/nginx-site.conf" "/etc/nginx/sites-available/$NGINX_SITE"
    
    print_status "Enabling site..."
    sudo ln -sf "/etc/nginx/sites-available/$NGINX_SITE" "/etc/nginx/sites-enabled/"
    
    print_status "Testing Nginx configuration..."
    if sudo nginx -t; then
        print_status "✅ Nginx configuration valid"
        
        print_status "Restarting Nginx..."
        sudo systemctl restart nginx
        print_status "✅ Nginx restarted"
    else
        print_error "❌ Nginx configuration invalid"
        return 1
    fi
}

# Main deployment function
deploy() {
    print_header "🚀 Starting Deployment Process"
    
    check_user
    pull_code
    update_dependencies
    test_application
    restart_service
    test_deployment
    
    print_header "🎉 Deployment Complete!"
    print_status "Your API is now live at:"
    print_status "- Local: http://localhost:$PORT"
    print_status "- Domain: http://$NGINX_SITE"
    print_status "- API Docs: http://$NGINX_SITE/docs"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy          Full deployment (pull, install, restart, test)"
    echo "  pull            Pull latest code from git"
    echo "  install         Install/update dependencies"
    echo "  test            Test application"
    echo "  restart         Restart the service"
    echo "  status          Show deployment status"
    echo "  setup-systemd   Setup systemd service"
    echo "  setup-nginx     Setup Nginx configuration"
    echo "  logs            Show recent logs"
    echo "  help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 deploy       # Full deployment"
    echo "  $0 restart      # Just restart the service"
    echo "  $0 status       # Check current status"
}

# Function to show logs
show_logs() {
    print_header "Recent Logs"
    
    if systemctl list-unit-files | grep -q "$SERVICE_NAME.service"; then
        print_status "Systemd service logs:"
        sudo journalctl -u "$SERVICE_NAME" --since "10 minutes ago" --no-pager -l
    else
        print_status "Manual process logs:"
        if [ -f "$PROJECT_DIR/gunicorn.log" ]; then
            tail -50 "$PROJECT_DIR/gunicorn.log"
        fi
        if [ -f "$PROJECT_DIR/gunicorn-error.log" ]; then
            echo -e "\n${YELLOW}Error logs:${NC}"
            tail -20 "$PROJECT_DIR/gunicorn-error.log"
        fi
    fi
}

# Main function
main() {
    local command=${1:-"help"}
    
    case $command in
        "deploy")
            deploy
            ;;
        "pull")
            check_user
            pull_code
            ;;
        "install")
            check_user
            update_dependencies
            ;;
        "test")
            check_user
            test_application
            ;;
        "restart")
            check_user
            restart_service
            ;;
        "status")
            show_status
            ;;
        "setup-systemd")
            check_user
            setup_systemd
            ;;
        "setup-nginx")
            setup_nginx
            ;;
        "logs")
            show_logs
            ;;
        "help"|"--help"|"-h")
            show_usage
            ;;
        *)
            print_error "Unknown command: $command"
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"