# Weather MCP Server

A Model Context Protocol (MCP) server that provides weather information using the Open-Meteo API. This server allows AI assistants to fetch current weather conditions and forecasts for any location worldwide.

Built with [FastMCP](https://github.com/jlowin/fastmcp) for a clean, maintainable implementation with minimal boilerplate.

## Features

- **Current Weather**: Get real-time weather conditions including temperature, humidity, wind speed, and precipitation
- **Weather Forecasts**: Get up to 16 days of weather forecasts
- **Geocoding**: Support for city names, addresses, and direct coordinates
- **No API Key Required**: Uses the free Open-Meteo API

## Quick Start (Recommended)

### Using the Setup Script

**On macOS/Linux:**
```bash
cd python_mcp
chmod +x setup.sh
./setup.sh
```

**On Windows:**
```bash
cd python_mcp
setup.bat
```

The setup script will:
- Create a virtual environment
- Install all dependencies
- Run tests to verify everything works

### Manual Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd python_mcp
   ```

2. **Create and activate a virtual environment:**
   
   **On macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   
   **On Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Testing

Before using the server with an MCP client, you can verify it works correctly:

```bash
python test_server.py
```

This will run a series of tests to verify:
- Server module can be imported
- Geocoding works correctly
- Weather API is accessible
- Data formatting is correct
- FastMCP tools are properly registered

## Usage

### Running the Server Standalone

You can run the server directly for testing:

```bash
python weather_server.py
```

The server will start and listen for MCP protocol messages on stdin/stdout. Note that it won't produce any output until it receives valid JSON-RPC messages.

### Configuring with Claude Desktop

To use this server with Claude Desktop, add it to your Claude configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

**If using a virtual environment (recommended):**

```json
{
  "mcpServers": {
    "weather": {
      "command": "/absolute/path/to/python_mcp/env/bin/python",
      "args": ["/absolute/path/to/python_mcp/weather_server.py"]
    }
  }
}
```

**On Windows with virtual environment:**

```json
{
  "mcpServers": {
    "weather": {
      "command": "C:\\absolute\\path\\to\\python_mcp\\env\\Scripts\\python.exe",
      "args": ["C:\\absolute\\path\\to\\python_mcp\\weather_server.py"]
    }
  }
}
```

**Without virtual environment:**

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/Users/jurinliyun/MyWorkLocal/trainings/mcp/python_mcp/weather_server.py"]
    }
  }
}
```

**Important:** Replace the paths with your actual absolute paths. You can get the absolute path by running `pwd` (macOS/Linux) or `cd` (Windows) in the `python_mcp` directory.

### Using with Other MCP Clients

This server follows the standard MCP protocol and can be used with any MCP-compatible client. Connect to it via stdio transport.

## Available Tools

### 1. get-current-weather

Get current weather conditions for a location.

**Parameters:**
- `location` (required): City name, address, or coordinates
  - Examples: `"London"`, `"New York, USA"`, `"51.5074,-0.1278"`

**Example:**
```json
{
  "name": "get-current-weather",
  "arguments": {
    "location": "Paris, France"
  }
}
```

### 2. get-forecast

Get weather forecast for a location.

**Parameters:**
- `location` (required): City name, address, or coordinates
- `days` (optional): Number of forecast days (1-16, default: 7)

**Example:**
```json
{
  "name": "get-forecast",
  "arguments": {
    "location": "Tokyo",
    "days": 5
  }
}
```

## Example Interactions

Once configured with an MCP client like Claude Desktop, you can ask:

- "What's the weather in London?"
- "Give me a 5-day forecast for New York"
- "What's the current temperature in Tokyo?"
- "Will it rain in Paris tomorrow?"

## API Information

This server uses the [Open-Meteo API](https://open-meteo.com/), which provides:
- Free access with no API key required
- Global weather data
- Current conditions and forecasts
- High accuracy and reliability

## Weather Codes

The server translates WMO weather codes into human-readable descriptions:
- Clear sky, partly cloudy, overcast
- Various precipitation types (drizzle, rain, snow)
- Fog conditions
- Thunderstorms

## Technical Details

- **Protocol**: Model Context Protocol (MCP)
- **Framework**: FastMCP - A high-level framework for building MCP servers with minimal boilerplate
- **Transport**: stdio
- **Language**: Python 3.8+
- **Async**: Built with asyncio for efficient I/O operations
- **Architecture**: Decorator-based tool registration using `@app.tool()` for clean, maintainable code

## Dependencies

- `fastmcp`: FastMCP framework for MCP server implementation (provides decorator-based tool registration)
- `mcp`: MCP Python SDK (required by FastMCP)
- `httpx`: Async HTTP client for API requests
- `geopy`: Geocoding library for location lookups
- `certifi`: SSL certificate bundle for secure connections

## Troubleshooting

### Installation Issues

**Dependencies won't install:**
- Ensure you're using Python 3.8 or higher: `python --version`
- Try upgrading pip: `pip install --upgrade pip`
- Use a virtual environment to avoid conflicts

### Server Issues

**"EOF while parsing a value" error:**
- This is normal when testing the server directly - it's waiting for JSON-RPC input
- The server is working correctly; this error appears when stdin is closed
- To properly test, use the `test_server.py` script or connect via an MCP client

**Server doesn't start:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Run the test script to diagnose: `python test_server.py`
- Check for import errors or missing packages

**No response from server in Claude Desktop:**
- Check the Claude Desktop logs for error messages
- Verify the path in your configuration file is correct and absolute
- Make sure Python is in your system PATH
- Try using the full path to your Python interpreter in the config

### Data Issues

**Location not found:**
- Try using a more specific location name (e.g., "London, UK" instead of "London")
- Use coordinates directly in the format "latitude,longitude"
- Check your internet connection (required for geocoding)

**Weather data errors:**
- Verify you have internet access
- The Open-Meteo API might be temporarily unavailable
- Check the server logs for specific error messages

## License

This project is provided as-is for educational and practical use.

## Contributing

Feel free to submit issues or pull requests to improve the server!
