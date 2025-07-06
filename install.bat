@echo off
REM 🚀 Product Management API - Windows Installation Script
REM This script automates the setup process for Windows systems

setlocal enabledelayedexpansion

REM Colors for output (Windows 10+)
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM Function to print colored output
:print_status
echo %GREEN%[INFO]%NC% %~1
goto :eof

:print_error
echo %RED%[ERROR]%NC% %~1
goto :eof

:print_warning
echo %YELLOW%[WARNING]%NC% %~1
goto :eof

:print_header
echo %BLUE%================================%NC%
echo %BLUE%%~1%NC%
echo %BLUE%================================%NC%
goto :eof

REM Main installation function
:main
if "%~1"=="" goto show_usage
if "%~1"=="help" goto show_usage
if "%~1"=="--help" goto show_usage
if "%~1"=="-h" goto show_usage
if "%~1"=="full-install" goto full_install
if "%~1"=="install" goto install_deps
if "%~1"=="test" goto run_tests
if "%~1"=="start" goto start_server
if "%~1"=="setup-local" goto setup_local
goto unknown_command

:check_python
call :print_header "Checking Python Installation"
python --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Python is not installed or not in PATH"
    call :print_error "Please install Python 3.9+ from https://www.python.org/downloads/"
    call :print_error "Make sure to check 'Add Python to PATH' during installation"
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
call :print_status "Found Python %python_version%"

REM Check if Python version is 3.9+
for /f "tokens=1,2 delims=." %%a in ("%python_version%") do (
    set major=%%a
    set minor=%%b
)

if %major% LSS 3 (
    call :print_error "Python 3.9+ is required. Found: %python_version%"
    exit /b 1
)

if %major% EQU 3 if %minor% LSS 9 (
    call :print_error "Python 3.9+ is required. Found: %python_version%"
    exit /b 1
)

call :print_status "✅ Python version check passed"
goto :eof

:setup_venv
call :print_header "Setting Up Virtual Environment"

if exist ".venv" (
    call :print_warning "Virtual environment already exists. Removing old one..."
    rmdir /s /q .venv
)

call :print_status "Creating virtual environment..."
python -m venv .venv

call :print_status "Activating virtual environment..."
call .venv\Scripts\activate.bat

call :print_status "Upgrading pip..."
python -m pip install --upgrade pip

call :print_status "✅ Virtual environment setup complete"
goto :eof

:install_deps
call :print_header "Installing Python Dependencies"

if not exist "requirements.txt" (
    call :print_error "requirements.txt not found!"
    exit /b 1
)

call .venv\Scripts\activate.bat

call :print_status "Installing requirements..."
pip install -r requirements.txt

call :print_status "Installing additional dependencies..."
pip install aiosqlite gunicorn

call :print_status "✅ Dependencies installed successfully"
goto :eof

:setup_local
call :print_header "Setting Up Local Environment"

call :print_status "Creating local development environment..."
(
echo DATABASE_URL=sqlite:///./local_products.db
echo DEBUG=true
echo ENVIRONMENT=development
echo HOST=0.0.0.0
echo PORT=8000
) > .env

call :print_status "✅ Environment configuration created"
goto :eof

:run_tests
call :print_header "Running Tests"

call .venv\Scripts\activate.bat

call :print_status "Testing imports..."
python test_import_only.py
if errorlevel 1 (
    call :print_error "❌ Import test failed"
    exit /b 1
)
call :print_status "✅ Import test passed"

call :print_status "Testing optimizations..."
python test_optimizations.py
if errorlevel 1 (
    call :print_error "❌ Optimization test failed"
    exit /b 1
)
call :print_status "✅ Optimization test passed"

call :print_status "Testing local setup..."
python test_local_simple.py
if errorlevel 1 (
    call :print_error "❌ Local setup test failed"
    exit /b 1
)
call :print_status "✅ Local setup test passed"

call :print_status "✅ All tests passed"
goto :eof

:start_server
call :print_header "Starting Development Server"

call .venv\Scripts\activate.bat

call :print_status "Starting development server with auto-reload..."
call :print_status "Server will be available at: http://localhost:8000"
call :print_status "API documentation at: http://localhost:8000/docs"
call :print_status "Press Ctrl+C to stop the server"

uvicorn product_management:app --host 0.0.0.0 --port 8000 --reload
goto :eof

:full_install
call :check_python
if errorlevel 1 exit /b 1

call :setup_venv
if errorlevel 1 exit /b 1

call :install_deps
if errorlevel 1 exit /b 1

call :setup_local
if errorlevel 1 exit /b 1

call :run_tests
if errorlevel 1 exit /b 1

call :print_header "Installation Complete!"
call :print_status "To start the server, run: install.bat start"
call :print_status "Or manually activate environment and run:"
call :print_status ".venv\Scripts\activate.bat"
call :print_status "uvicorn product_management:app --host 0.0.0.0 --port 8000 --reload"
goto :eof

:show_usage
echo Usage: %~nx0 [OPTION]
echo.
echo Options:
echo   full-install     Complete installation (install + setup + test)
echo   install          Install dependencies only
echo   setup-local      Setup local development environment
echo   test             Run all tests
echo   start            Start development server
echo   help             Show this help message
echo.
echo Examples:
echo   %~nx0 full-install    # Complete local setup
echo   %~nx0 start           # Start development server
goto :eof

:unknown_command
call :print_error "Unknown command: %~1"
call :show_usage
exit /b 1

REM Call main function with arguments
call :main %*