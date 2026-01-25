#!/usr/bin/env python3
"""
Test script for the Weather MCP Server.
This script helps verify that the server can start and respond to requests.
"""

import asyncio
import json
import sys
from io import StringIO


async def test_server_import():
    """Test that we can import the server module."""
    print("Testing server import...")
    try:
        import weather_server

        print("✓ Server module imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import server: {e}")
        return False


async def test_geocoding():
    """Test the geocoding functionality."""
    print("\nTesting geocoding...")
    try:
        from weather_server import get_coordinates

        # Test with a known location
        coords = await get_coordinates("London, UK")
        if coords:
            print(f"✓ Geocoding works: London -> {coords[0]:.4f}, {coords[1]:.4f}")
            return True
        else:
            print("✗ Geocoding returned None")
            return False
    except Exception as e:
        print(f"✗ Geocoding failed: {e}")
        return False


async def test_weather_api():
    """Test the weather API call."""
    print("\nTesting weather API...")
    try:
        from weather_server import fetch_weather

        # Test with London coordinates
        lat, lon = 51.5074, -0.1278
        weather_data = await fetch_weather(lat, lon, forecast_days=1)

        if weather_data and "current" in weather_data:
            temp = weather_data["current"].get("temperature_2m", "N/A")
            print(f"✓ Weather API works: Current temp in London is {temp}°C")
            return True
        else:
            print("✗ Weather API returned invalid data")
            return False
    except Exception as e:
        print(f"✗ Weather API failed: {e}")
        return False


async def test_weather_formatting():
    """Test the weather formatting function."""
    print("\nTesting weather formatting...")
    try:
        from weather_server import format_weather_response, weather_code_to_description

        # Test weather code conversion
        description = weather_code_to_description(0)
        if description == "Clear sky":
            print(f"✓ Weather code conversion works: 0 -> '{description}'")
        else:
            print(f"✗ Unexpected description: {description}")
            return False

        # Test formatting with sample data
        sample_data = {
            "current": {
                "temperature_2m": 20.0,
                "apparent_temperature": 18.0,
                "relative_humidity_2m": 65,
                "precipitation": 0.0,
                "weather_code": 1,
                "wind_speed_10m": 10.5,
                "wind_direction_10m": 180,
            },
            "daily": {
                "time": ["2024-01-01"],
                "temperature_2m_max": [22.0],
                "temperature_2m_min": [15.0],
                "precipitation_sum": [0.0],
                "weather_code": [1],
            },
        }

        formatted = format_weather_response(sample_data, "Test Location")
        if "Test Location" in formatted and "20.0°C" in formatted:
            print("✓ Weather formatting works")
            return True
        else:
            print("✗ Weather formatting failed")
            return False

    except Exception as e:
        print(f"✗ Weather formatting failed: {e}")
        return False


async def test_mcp_tools():
    """Test that MCP tools are properly defined."""
    print("\nTesting MCP tools...")
    try:
        # Import the app and check tools are registered
        from weather_server import app

        # FastMCP stores tools in a registry, we can check them
        expected_tools = ["get-current-weather", "get-forecast"]
        
        # Get all registered tools
        tools = await app.get_tools()
        tool_names = list(tools.keys())
        
        # Check that expected tools are registered
        for tool_name in expected_tools:
            if tool_name not in tool_names:
                print(f"✗ Tool '{tool_name}' not found in registered tools")
                print(f"  Registered tools: {tool_names}")
                return False
        
        print(f"✓ FastMCP server initialized with tools: {tool_names}")
        return True

    except Exception as e:
        print(f"✗ MCP tools test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Weather MCP Server Test Suite")
    print("=" * 60)

    results = []

    # Run tests in order
    results.append(await test_server_import())
    results.append(await test_geocoding())
    results.append(await test_weather_api())
    results.append(await test_weather_formatting())
    results.append(await test_mcp_tools())

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
