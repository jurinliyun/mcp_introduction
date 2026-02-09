#!/usr/bin/env python3
"""
Weather MCP Server - HTTP Version

An MCP server that provides weather information via HTTP/SSE transport.
Run with: python weather_server_http.py
Access at: http://localhost:8001
"""

import asyncio
import logging
import ssl
from typing import Any

import certifi
import httpx
from fastmcp import FastMCP
from geopy.geocoders import Nominatim

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather-server-http")

# Initialize FastMCP server
app = FastMCP("weather-server")

# Create SSL context with certifi certificates
try:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
except (PermissionError, OSError):
    # Fallback to default SSL context if certifi path has permission issues
    logger.warning("Could not use certifi certificates, using default SSL context")
    ssl_context = ssl.create_default_context()

# Initialize geocoder for location lookups with SSL context
geolocator = Nominatim(user_agent="mcp-weather-server", ssl_context=ssl_context)


async def get_coordinates(location: str) -> tuple[float, float] | None:
    """Convert a location name to coordinates using geocoding."""
    try:
        # Run geocoding in thread pool since it's synchronous
        loop = asyncio.get_event_loop()
        geo_location = await loop.run_in_executor(None, geolocator.geocode, location)

        if geo_location:
            return (geo_location.latitude, geo_location.longitude)
        return None
    except Exception as e:
        logger.error(f"Geocoding error: {e}")
        return None


async def fetch_weather(
    latitude: float, longitude: float, forecast_days: int = 1
) -> dict[str, Any]:
    """Fetch weather data from Open-Meteo API."""
    base_url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code,wind_speed_10m_max",
        "timezone": "auto",
        "forecast_days": forecast_days,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
        response.raise_for_status()
        return response.json()


def weather_code_to_description(code: int) -> str:
    """Convert WMO weather code to human-readable description."""
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }
    return weather_codes.get(code, f"Unknown (code: {code})")


def format_weather_response(data: dict[str, Any], location: str) -> str:
    """Format weather data into a readable string."""
    current = data.get("current", {})
    daily = data.get("daily", {})

    # Current weather
    result = [
        f"Weather for {location}",
        f"\n=== Current Weather ===",
        f"Temperature: {current.get('temperature_2m', 'N/A')}°C",
        f"Feels like: {current.get('apparent_temperature', 'N/A')}°C",
        f"Humidity: {current.get('relative_humidity_2m', 'N/A')}%",
        f"Precipitation: {current.get('precipitation', 'N/A')} mm",
        f"Wind Speed: {current.get('wind_speed_10m', 'N/A')} km/h",
        f"Wind Direction: {current.get('wind_direction_10m', 'N/A')}°",
        f"Conditions: {weather_code_to_description(current.get('weather_code', 0))}",
    ]

    # Daily forecast
    if daily and len(daily.get("time", [])) > 0:
        result.append("\n=== Forecast ===")
        for i in range(len(daily.get("time", []))):
            date = daily["time"][i]
            temp_max = daily["temperature_2m_max"][i]
            temp_min = daily["temperature_2m_min"][i]
            precip = daily["precipitation_sum"][i]
            conditions = weather_code_to_description(daily["weather_code"][i])

            result.append(
                f"\n{date}:\n"
                f"  High: {temp_max}°C, Low: {temp_min}°C\n"
                f"  Precipitation: {precip} mm\n"
                f"  Conditions: {conditions}"
            )

    return "\n".join(result)


def parse_location(location: str) -> tuple[tuple[float, float], str] | None:
    """
    Parse location string to coordinates and display name.
    Returns (coordinates, display_location) or None if invalid.
    """
    # Check if location is coordinates
    if "," in location and all(
        part.strip().replace(".", "").replace("-", "").isdigit()
        for part in location.split(",")
    ):
        try:
            lat, lon = map(float, location.split(","))
            return ((lat, lon), f"coordinates {lat}, {lon}")
        except ValueError:
            return None
    return None


@app.tool(
    name="get-current-weather",
    description="Get the current weather for a location. Provide a city name, address, or 'latitude,longitude' coordinates.",
)
async def get_current_weather(
    location: str = "City name, address, or coordinates (e.g., 'London', 'New York, USA', or '51.5074,-0.1278')"
) -> str:
    """Get the current weather for a location."""
    if not location:
        return "Error: Location is required"

    # Try to parse as coordinates first
    parsed = parse_location(location)
    if parsed:
        coordinates, display_location = parsed
    else:
        # Geocode the location
        coordinates = await get_coordinates(location)
        if not coordinates:
            return f"Error: Could not find location '{location}'"
        display_location = location

    try:
        weather_data = await fetch_weather(
            coordinates[0], coordinates[1], forecast_days=1
        )
        return format_weather_response(weather_data, display_location)
    except Exception as e:
        logger.error(f"Weather fetch error: {e}", exc_info=True)
        return f"Error fetching weather data: {str(e)}"


@app.tool(
    name="get-forecast",
    description="Get weather forecast for a location. Provide a city name, address, or coordinates, and number of days (1-16).",
)
async def get_forecast(
    location: str = "City name, address, or coordinates (e.g., 'London', 'New York, USA', or '51.5074,-0.1278')",
    days: int = 7,
) -> str:
    """Get weather forecast for a location."""
    if not location:
        return "Error: Location is required"

    # Validate days
    if not isinstance(days, (int, float)) or days < 1 or days > 16:
        return "Error: Days must be between 1 and 16"

    days = int(days)

    # Try to parse as coordinates first
    parsed = parse_location(location)
    if parsed:
        coordinates, display_location = parsed
    else:
        # Geocode the location
        coordinates = await get_coordinates(location)
        if not coordinates:
            return f"Error: Could not find location '{location}'"
        display_location = location

    try:
        weather_data = await fetch_weather(
            coordinates[0], coordinates[1], forecast_days=days
        )
        return format_weather_response(weather_data, display_location)
    except Exception as e:
        logger.error(f"Weather fetch error: {e}", exc_info=True)
        return f"Error fetching weather data: {str(e)}"


if __name__ == "__main__":
    try:
        logger.info("Starting Weather MCP Server with HTTP/SSE transport...")
        logger.info("Server will be available at: http://localhost:8001")
        logger.info("SSE endpoint: http://localhost:8001/sse")
        
        # Run with HTTP transport instead of stdio (using port 8001 to avoid conflict)
        app.run(transport="sse", port=8001, host="127.0.0.1")
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise
