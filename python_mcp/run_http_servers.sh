#!/bin/bash
# Run both MCP HTTP servers

cd "$(dirname "$0")"

# Activate virtual environment
source env/bin/activate

echo "Starting MCP HTTP Servers..."
echo "================================"

# Start calculator server in background
python calculator_server_http.py &
CALC_PID=$!
echo "✓ Calculator Server started (PID: $CALC_PID)"
echo "  URL: http://localhost:8000/sse"

# Give it a moment to start
sleep 1

# Start weather server in background
python weather_server_http.py &
WEATHER_PID=$!
echo "✓ Weather Server started (PID: $WEATHER_PID)"
echo "  URL: http://localhost:8001/sse"

echo "================================"
echo "Both servers are running!"
echo ""
echo "To configure Claude Desktop, copy the content from:"
echo "  http_config.json"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $CALC_PID 2>/dev/null
    kill $WEATHER_PID 2>/dev/null
    echo "Servers stopped"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT TERM

# Wait for both processes
wait
