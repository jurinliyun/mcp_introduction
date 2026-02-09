@echo off
REM Run both MCP HTTP servers on Windows

cd /d "%~dp0"

echo Starting MCP HTTP Servers...
echo ================================

REM Activate virtual environment
call env\Scripts\activate.bat

REM Start calculator server in new window
start "Calculator MCP Server" python calculator_server_http.py
echo Started Calculator Server
echo   URL: http://localhost:8000/sse

REM Give it a moment to start
timeout /t 2 /nobreak >nul

REM Start weather server in new window
start "Weather MCP Server" python weather_server_http.py
echo Started Weather Server
echo   URL: http://localhost:8001/sse

echo ================================
echo Both servers are running in separate windows!
echo.
echo To configure Claude Desktop, copy the content from:
echo   http_config.json
echo.
echo Close the server windows to stop them.
echo.
pause
