import os
import requests
from langchain_core.tools import tool


@tool
def get_current_weather(location: str) -> str:
    """
    Get current weather information for a location in Celsius and metric units.

    Args:
            location: The city or location to get weather for (e.g., "New York", "London")

    Returns:
            A string with current weather information for the location
    """
    api_key = os.environ.get("WEATHERSTACK_API_KEY")
    if not api_key:
        return "Error: WEATHERSTACK_API_KEY environment variable not found. Please set your API key."
    try:
        url = "http://api.weatherstack.com/current"
        params = {
            "access_key": api_key,
            "query": location,
            "units": "m",  # metric units (Celsius)
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data.get("success", True):
            error = data.get("error", {})
            return f"API Error: {error.get('info', 'Unknown error')}"
        current = data.get("current", {})
        location_info = data.get("location", {})
        if not current:
            return f"Error: No weather data found for {location}"
        temp_unit = "°C"
        wind_unit = "km/h"
        weather_info = f"Weather in {location_info.get('name', location)}, {location_info.get('country', 'Unknown')}:\n"
        weather_info += f"Temperature: {current.get('temperature', 'N/A')}{temp_unit}\n"
        weather_info += f"Feels like: {current.get('feelslike', 'N/A')}{temp_unit}\n"
        weather_info += f"Humidity: {current.get('humidity', 'N/A')}%\n"
        weather_info += f"Wind: {current.get('wind_speed', 'N/A')} {wind_unit} {current.get('wind_dir', '')}\n"
        weather_info += (
            f"Condition: {current.get('weather_descriptions', ['N/A'])[0]}\n"
        )
        weather_info += f"Pressure: {current.get('pressure', 'N/A')} mb\n"
        weather_info += f"Visibility: {current.get('visibility', 'N/A')} km\n"
        weather_info += f"UV Index: {current.get('uv_index', 'N/A')}\n"
        weather_info += f"Observation time: {current.get('observation_time', 'N/A')}"
        return weather_info

    except requests.exceptions.RequestException as e:
        return f"Error making API request: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"
