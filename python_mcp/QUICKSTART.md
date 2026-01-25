# Weather MCP Server - Quick Start Guide

Get up and running in 5 minutes! ⚡

## Step 1: Setup (Choose One)

### Option A: Automated Setup (Easiest)

**macOS/Linux:**
```bash
cd python_mcp
chmod +x setup.sh
./setup.sh
```

**Windows:**
```bash
cd python_mcp
setup.bat
```

✅ Done! Skip to Step 3.

### Option B: Manual Setup

```bash
cd python_mcp

# Create virtual environment
python3 -m venv env

# Activate it
source env/bin/activate  # macOS/Linux
# OR
env\Scripts\activate     # Windows

# Install packages
pip install -r requirements.txt

# Test it
python test_server.py
```

## Step 2: Test the Server

While your virtual environment is activated:

```bash
python test_server.py
```

You should see all tests passing ✓

## Step 3: Configure Claude Desktop

1. Find your config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Get your absolute paths:
   ```bash
   # In the python_mcp directory:
   pwd                    # macOS/Linux
   cd                     # Windows
   ```

3. Add this to your config (replace with YOUR paths):

   **macOS/Linux:**
   ```json
   {
     "mcpServers": {
       "weather": {
         "command": "/your/path/to/python_mcp/env/bin/python",
         "args": ["/your/path/to/python_mcp/weather_server.py"]
       }
     }
   }
   ```

   **Windows:**
   ```json
   {
     "mcpServers": {
       "weather": {
         "command": "C:\\your\\path\\to\\python_mcp\\env\\Scripts\\python.exe",
         "args": ["C:\\your\\path\\to\\python_mcp\\weather_server.py"]
       }
     }
   }
   ```

4. Restart Claude Desktop

## Step 4: Test with MCP Inspector (Optional but Recommended)

MCP Inspector is a web-based tool for testing and debugging MCP servers. It's great for verifying your server works before using it with Claude Desktop or Cursor.

### Install MCP Inspector

**Option 1: Run directly with npx (no installation needed)**
```bash
npx @modelcontextprotocol/inspector
```

**Option 2: Install globally**
```bash
npm install -g @modelcontextprotocol/inspector
mcp-inspector
```

### Use MCP Inspector

1. **Start the Inspector:**
   ```bash
   npx @modelcontextprotocol/inspector
   ```
   This will open a web interface in your browser (usually at `http://localhost:5173`)

2. **Connect to your server:**
   - In the Inspector interface, look for the connection settings
   - Select **"stdio"** as the transport type
   - Enter the **command**: `/your/path/to/python_mcp/env/bin/python`
     - Replace with your actual absolute path!
   - Enter the **args**: `/your/path/to/python_mcp/weather_server.py`
   - Click **"Connect"** or **"Start Server"**

3. **Test your tools:**
   - Once connected, you'll see a list of available tools:
     - `get-current-weather`
     - `get-forecast`
   - Click on a tool to test it
   - Enter parameters in the form:
     - For `get-current-weather`: `{"location": "Tokyo"}`
     - For `get-forecast`: `{"location": "London", "days": 5}`
   - Click **"Call Tool"** to see the results

4. **Explore the interface:**
   - **Tools Tab**: Test all available tools
   - **Resources Tab**: View available resources (if any)
   - **Prompts Tab**: Test prompts (if any)
   - **Logs**: See raw JSON-RPC messages for debugging

✅ **Benefits of MCP Inspector:**
- Test tools without setting up Claude Desktop or Cursor
- Debug server issues easily
- See raw JSON-RPC messages
- Verify tool schemas and responses
- Great for development and troubleshooting

### Quick Test Example

1. Start inspector: `npx @modelcontextprotocol/inspector`
2. Connect with:
   - Command: `/Users/jurinliyun/MyWorkLocal/trainings/mcp/python_mcp/env/bin/python`
   - Args: `/Users/jurinliyun/MyWorkLocal/trainings/mcp/python_mcp/weather_server.py`
3. Test `get-current-weather` with `{"location": "Tokyo"}`
4. You should see the weather data returned! ✅

## Step 5: Try It Out!

### With Claude Desktop

Open Claude Desktop and ask:

- "What's the weather in Tokyo?"
- "Give me a 5-day forecast for London"
- "What's the temperature in Paris right now?"
- "Will it rain in New York tomorrow?"

### With Cursor MCP

If you're using Cursor, add the server to your MCP configuration:

```json
{
  "mcpServers": {
    "user-weather": {
      "command": "/your/path/to/python_mcp/env/bin/python",
      "args": ["/your/path/to/python_mcp/weather_server.py"]
    }
  }
}
```

Then you can use it in Cursor by referencing `@anysphere.cursor-mcp.MCP user-weather` in your prompts.

## Troubleshooting

### ❌ "EOF while parsing" error
✅ This is normal when running the server directly! It's waiting for JSON-RPC input. Use `test_server.py` instead.

### ❌ Server not responding in Claude/Cursor
✅ Check:
1. Are the paths in your config absolute and correct?
2. Did you use the Python from the env virtual environment?
3. Did you restart Claude Desktop/Cursor?
4. Test with MCP Inspector first to verify the server works

### ❌ "Location not found"
✅ Try:
- More specific: "London, UK" instead of "London"
- Use coordinates: "51.5074,-0.1278"

### ❌ Tests failing
✅ Check:
1. Is your virtual environment activated?
2. Are you connected to the internet?
3. Run `pip install -r requirements.txt` again

## What You Get

### Tool: get-current-weather
Get current conditions for any location.

**Example:**
```
User: "What's the weather in Paris?"
```

### Tool: get-forecast
Get multi-day forecasts (1-16 days).

**Example:**
```
User: "Give me a 3-day forecast for Tokyo"
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [weather_server.py](weather_server.py) to see how it works
- Modify the code to add more weather features!

## Need Help?

Common issues and solutions are in the main README.md file under "Troubleshooting".

---

**Happy weather checking! 🌤️**