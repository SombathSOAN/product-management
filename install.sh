#!/bin/bash

# 🚀 Product Management API - Complete Installation Script
# This script automates the entire setup process for local and server deployment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Function to install system dependencies
install_system_deps() {
    local os=$(detect_os)
    
    print_header "Installing System Dependencies"
    
    case $os in
        "linux")
            print_status "Detected Linux system"
            if command_exists apt-get; then
                sudo apt-get update
                sudo apt-get install -y python3 python3-pip python3-venv build-essential libssl-dev libffi-dev python3-dev curl
            elif command_exists yum; then
                sudo yum update -y
                sudo yum install -y python3 python3-pip python3-venv gcc openssl-devel libffi-devel python3-devel curl
            elif command_exists dnf; then
                sudo dnf update -y
                sudo dnf install -y python3 python3-pip python3-venv gcc openssl-devel libffi-devel python3-devel curl
            else
                print_error "Unsupported Linux distribution"
                exit 1
            fi
            ;;
        "macos")
            print_status "Detected macOS system"
            if ! command_exists brew; then
                print_status "Installing Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew install python3 curl
            ;;
        "windows")
            print_warning "Windows detected. Please ensure Python 3.9+ is installed manually."
            print_warning "Download from: https://www.python.org/downloads/"
            ;;
        *)
            print_error "Unsupported operating system: $os"
            exit 1
            ;;
    esac
}

# Function to check Python version
check_python() {
    print_header "Checking Python Installation"
    
    if ! command_exists python3; then
        print_error "Python 3 is not installed"
        return 1
    fi
    
    local python_version=$(python3 --version | cut -d' ' -f2)
    local major_version=$(echo $python_version | cut -d'.' -f1)
    local minor_version=$(echo $python_version | cut -d'.' -f2)
    
    print_status "Found Python $python_version"
    
    if [ "$major_version" -lt 3 ] || ([ "$major_version" -eq 3 ] && [ "$minor_version" -lt 9 ]); then
        print_error "Python 3.9+ is required. Found: $python_version"
        return 1
    fi
    
    print_status "✅ Python version check passed"
    return 0
}

# Function to setup virtual environment
setup_venv() {
    print_header "Setting Up Virtual Environment"
    
    if [ -d ".venv" ]; then
        print_warning "Virtual environment already exists. Removing old one..."
        rm -rf .venv
    fi
    
    print_status "Creating virtual environment..."
    python3 -m venv .venv
    
    print_status "Activating virtual environment..."
    source .venv/bin/activate
    
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    print_status "✅ Virtual environment setup complete"
}

# Function to install Python dependencies
install_dependencies() {
    print_header "Installing Python Dependencies"
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found!"
        exit 1
    fi
    
    print_status "Installing requirements..."
    pip install -r requirements.txt
    
    print_status "Installing additional dependencies..."
    pip install aiosqlite gunicorn
    
    print_status "✅ Dependencies installed successfully"
}

# Function to setup environment configuration
setup_environment() {
    print_header "Setting Up Environment Configuration"
    
    local env_type=${1:-"local"}
    
    case $env_type in
        "local")
            print_status "Creating local development environment..."
            cat > .env << EOF
DATABASE_URL=sqlite:///./local_products.db
DEBUG=true
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
EOF
            ;;
        "production")
            print_status "Creating production environment template..."
            cat > .env << EOF
DATABASE_URL=sqlite:///./production.db
DEBUG=false
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000
# Add your production database URL here:
# DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/dbname
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
EOF
            ;;
    esac
    
    print_status "✅ Environment configuration created"
}

# Function to run tests
run_tests() {
    print_header "Running Tests"
    
    print_status "Testing imports..."
    if python test_import_only.py; then
        print_status "✅ Import test passed"
    else
        print_error "❌ Import test failed"
        return 1
    fi
    
    print_status "Testing optimizations..."
    if python test_optimizations.py; then
        print_status "✅ Optimization test passed"
    else
        print_error "❌ Optimization test failed"
        return 1
    fi
    
    print_status "Testing local setup..."
    if python test_local_simple.py; then
        print_status "✅ Local setup test passed"
    else
        print_error "❌ Local setup test failed"
        return 1
    fi
    
    print_status "✅ All tests passed"
}

# Function to start server
start_server() {
    print_header "Starting Server"
    
    local mode=${1:-"development"}
    
    case $mode in
        "development")
            print_status "Starting development server with auto-reload..."
            print_status "Server will be available at: http://localhost:8000"
            print_status "API documentation at: http://localhost:8000/docs"
            print_status "Press Ctrl+C to stop the server"
            uvicorn product_management:app --host 0.0.0.0 --port 8000 --reload
            ;;
        "production")
            print_status "Starting production server with Gunicorn..."
            gunicorn product_management:app -c gunicorn.conf.py
            ;;
    esac
}

# Function to test API endpoints
test_api() {
    print_header "Testing API Endpoints"
    
    local base_url=${1:-"http://localhost:8000"}
    
    print_status "Testing health endpoint..."
    if curl -s "$base_url/" | grep -q "Product Management API"; then
        print_status "✅ Health endpoint working"
    else
        print_error "❌ Health endpoint failed"
        return 1
    fi
    
    print_status "Testing products endpoint..."
    if curl -s "$base_url/products" >/dev/null; then
        print_status "✅ Products endpoint working"
    else
        print_error "❌ Products endpoint failed"
        return 1
    fi
    
    print_status "Running comprehensive tests..."
    if python test_everything.py "$base_url"; then
        print_status "✅ All API tests passed"
    else
        print_error "❌ Some API tests failed"
        return 1
    fi
}

# Function to setup production server
setup_production() {
    print_header "Setting Up Production Server"
    
    print_status "Installing system dependencies for production..."
    install_system_deps
    
    print_status "Setting up production environment..."
    setup_environment "production"
    
    print_status "Creating systemd service..."
    local service_file="/etc/systemd/system/product-management.service"
    local project_dir=$(pwd)
    
    sudo tee "$service_file" > /dev/null << EOF
[Unit]
Description=Product Management API
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=$project_dir
Environment=PATH=$project_dir/.venv/bin
ExecStart=$project_dir/.venv/bin/gunicorn product_management:app -c gunicorn.conf.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
    
    print_status "Enabling and starting service..."
    sudo systemctl daemon-reload
    sudo systemctl enable product-management
    sudo systemctl start product-management
    
    print_status "✅ Production setup complete"
    print_status "Service status:"
    sudo systemctl status product-management --no-pager
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  install           Install dependencies and setup local environment"
    echo "  install-system    Install system dependencies only"
    echo "  setup-local       Setup local development environment"
    echo "  setup-production  Setup production environment"
    echo "  test             Run all tests"
    echo "  start            Start development server"
    echo "  start-prod       Start production server"
    echo "  test-api         Test API endpoints"
    echo "  full-install     Complete installation (install + setup + test)"
    echo "  production       Full production setup"
    echo "  help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 full-install    # Complete local setup"
    echo "  $0 production      # Complete production setup"
    echo "  $0 start           # Start development server"
}

# Main function
main() {
    local command=${1:-"help"}
    
    case $command in
        "install-system")
            install_system_deps
            ;;
        "install")
            check_python || (install_system_deps && check_python)
            setup_venv
            install_dependencies
            ;;
        "setup-local")
            setup_environment "local"
            ;;
        "setup-production")
            setup_environment "production"
            ;;
        "test")
            source .venv/bin/activate 2>/dev/null || true
            run_tests
            ;;
        "start")
            source .venv/bin/activate
            start_server "development"
            ;;
        "start-prod")
            source .venv/bin/activate
            start_server "production"
            ;;
        "test-api")
            source .venv/bin/activate 2>/dev/null || true
            test_api
            ;;
        "full-install")
            check_python || (install_system_deps && check_python)
            setup_venv
            install_dependencies
            setup_environment "local"
            run_tests
            print_header "Installation Complete!"
            print_status "To start the server, run: $0 start"
            print_status "Or manually: source .venv/bin/activate && uvicorn product_management:app --host 0.0.0.0 --port 8000 --reload"
            ;;
        "production")
            setup_production
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