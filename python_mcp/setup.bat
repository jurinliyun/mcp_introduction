@echo off
REM Weather MCP Server Setup Script for Windows

echo ================================
echo Weather MCP Server Setup
echo ================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        echo Please ensure Python is installed correctly
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

echo.
echo Activating virtual environment...

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
) else (
    echo Error: Could not find activation script
    exit /b 1
)

echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies
    exit /b 1
)

echo.
echo [OK] Dependencies installed successfully
echo.

REM Run tests
echo Running tests...
python test_server.py

if errorlevel 0 (
    echo.
    echo ================================
    echo [OK] Setup completed successfully!
    echo ================================
    echo.
    echo To use the server:
    echo 1. Keep the virtual environment activated
    echo 2. Run: python weather_server.py
    echo.
    echo Or add to Claude Desktop config:
    echo {
    echo   "mcpServers": {
    echo     "weather": {
    echo       "command": "%CD%\venv\Scripts\python.exe",
    echo       "args": ["%CD%\weather_server.py"]
    echo     }
    echo   }
    echo }
) else (
    echo.
    echo [WARNING] Setup completed but some tests failed
    echo The server may still work - check errors above
)

pause
