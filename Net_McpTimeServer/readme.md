
# .NET MCP Time Server

A Model Context Protocol (MCP) server implementation in .NET that provides time-related tools and resources.

## Overview

This is a .NET implementation of an MCP server that demonstrates how to build MCP servers using C#. The server provides tools for getting current time in different timezones and formats.

## Features

- **Time Tools**: Get current time with timezone support
- **MCP Protocol**: Full implementation of the Model Context Protocol
- **Async/Await**: Modern async programming patterns
- **Cross-platform**: Runs on Windows, Linux, and macOS

## Prerequisites

- .NET 6.0 or higher
- Visual Studio 2022, VS Code, or JetBrains Rider

## Installation

1. Clone the repository:
git clone <repository-url>
cd Net_McpTimeServer

2. Restore dependencies:
dotnet restore

3. Build the project:
dotnet build

## Usage

### Running the Server

dotnet run

The server will start and listen for MCP protocol messages via standard input/output.

### Available Tools

#### `get_current_time`
Gets the current time with optional timezone and format parameters.

**Parameters:**
- `timezone` (optional): IANA timezone identifier (e.g., "America/New_York", "Asia/Tokyo")
- `format` (optional): Time format string (e.g., "HH:mm:ss", "yyyy-MM-dd HH:mm:ss")

**Example:**
{
  "timezone": "UTC",
  "format": "yyyy-MM-dd HH:mm:ss"
}

## Integration with Claude Desktop

Add the following configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

{
  "mcpServers": {
    "dotnet-time-server": {
      "command": "dotnet",
      "args": ["run", "--project", "/path/to/Net_McpTimeServer"]
    }
  }
}

## Project Structure

Net_McpTimeServer/
├── Program.cs              # Main entry point
├── McpServer.cs           # MCP server implementation
├── Tools/                 # Tool implementations
│   └── TimeTools.cs      # Time-related tools
├── Net_McpTimeServer.csproj
└── readme.md

## Development

### Adding New Tools

1. Create a new tool class in the `Tools` folder
2. Implement the tool interface
3. Register the tool in `McpServer.cs`

### Testing

dotnet test

## MCP Protocol Support

This server implements the following MCP capabilities:

- ✅ Tool listing
- ✅ Tool execution
- ✅ Error handling
- ✅ Async operations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Your License Here]

## References

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [.NET Documentation](https://docs.microsoft.com/dotnet)
