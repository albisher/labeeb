"""
Weather tool module for Labeeb.

This module provides functionality to get weather information for a given location.
It uses the OpenWeatherMap API to fetch weather data.

---
description: Get weather information for a location
endpoints: [get_weather]
inputs: [location]
outputs: [weather_data]
dependencies: [requests]
auth: required
alwaysApply: false
---
"""

import os
import logging
import requests
from typing import Dict, Any, Optional
from labeeb.core.config_manager import ConfigManager

logger = logging.getLogger(__name__)

class WeatherTool:
    """Tool for getting weather information."""
    
    def __init__(self):
        """Initialize the weather tool."""
        self.config = ConfigManager()
        self.api_key = self.config.get("openweathermap_api_key")
        if not self.api_key:
            logger.warning("OpenWeatherMap API key not set")
            
    def get_weather(self, location: str) -> Dict[str, Any]:
        """
        Get weather information for a location.
        
        Args:
            location: The location to get weather for
            
        Returns:
            Dict containing weather information
            
        Raises:
            ValueError: If API key is not set
            requests.RequestException: If API request fails
        """
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key not set")
            
        try:
            # Get coordinates for location
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct"
            geo_params = {
                "q": location,
                "limit": 1,
                "appid": self.api_key
            }
            geo_response = requests.get(geo_url, params=geo_params)
            geo_response.raise_for_status()
            
            if not geo_response.json():
                raise ValueError(f"Location not found: {location}")
                
            lat = geo_response.json()[0]["lat"]
            lon = geo_response.json()[0]["lon"]
            
            # Get weather data
            weather_url = "https://api.openweathermap.org/data/2.5/weather"
            weather_params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            weather_response = requests.get(weather_url, params=weather_params)
            weather_response.raise_for_status()
            
            weather_data = weather_response.json()
            
            # Format response
            return {
                "location": location,
                "temperature": weather_data["main"]["temp"],
                "feels_like": weather_data["main"]["feels_like"],
                "humidity": weather_data["main"]["humidity"],
                "description": weather_data["weather"][0]["description"],
                "wind_speed": weather_data["wind"]["speed"],
                "clouds": weather_data["clouds"]["all"]
            }
            
        except requests.RequestException as e:
            logger.error(f"Error getting weather data: {e}")
            raise 