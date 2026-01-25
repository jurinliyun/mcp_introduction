#!/bin/bash

# Weather MCP Server Setup Script

echo "================================"
echo "Weather MCP Server Setup"
echo "================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        echo "Please ensure python3-venv is installed"
        exit 1
    fi
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "Activating virtual environment..."

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "Error: Could not find activation script"
    exit 1
fi

echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "✗ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✓ Dependencies installed successfully"
echo ""

# Run tests
echo "Running tests..."
python test_server.py

if [ $? -eq 0 ]; then
    echo ""
    echo "================================"
    echo "✓ Setup completed successfully!"
    echo "================================"
    echo ""
    echo "To use the server:"
    echo "1. Keep the virtual environment activated"
    echo "2. Run: python weather_server.py"
    echo ""
    echo "Or add to Claude Desktop config:"
    echo "{"
    echo "  \"mcpServers\": {"
    echo "    \"weather\": {"
    echo "      \"command\": \"$(pwd)/venv/bin/python\","
    echo "      \"args\": [\"$(pwd)/weather_server.py\"]"
    echo "    }"
    echo "  }"
    echo "}"
else
    echo ""
    echo "⚠ Setup completed but some tests failed"
    echo "The server may still work - check errors above"
fi
