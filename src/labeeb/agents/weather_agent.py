"""
Weather agent for handling weather-related tasks.

---
description: Weather agent for handling weather queries and forecasts
endpoints: [weather_agent]
inputs: [city, query]
outputs: [weather_info]
dependencies: [requests, python-dotenv]
auth: none
alwaysApply: false
---
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

from labeeb.agents.base_agent import BaseAgent
from labeeb.tools.weather_tool import WeatherTool
from labeeb.utils.platform_utils import ensure_labeeb_directories

# Configure logging
logger = logging.getLogger(__name__)

class WeatherAgent(BaseAgent):
    """Weather agent for handling weather-related tasks."""
    
    def __init__(self):
        """Initialize the weather agent."""
        super().__init__()
        self.name = "weather_agent"
        self.description = "Handles weather queries and forecasts"
        self.version = "1.0.0"
        self.weather_tool = WeatherTool()
        self.cache = {}
        self.cache_duration = 1800  # 30 minutes
        
        # Load environment variables
        load_dotenv()
        
        # Ensure required directories exist
        ensure_labeeb_directories()
        
        # Initialize configuration
        self.config = {
            "api_key": os.getenv("WEATHER_API_KEY"),
            "units": "metric",
            "language": "en",
            "cache_enabled": True
        }
    
    def validate_config(self) -> bool:
        """Validate the agent configuration."""
        return bool(self.config.get("api_key"))
    
    def get_weather(self, city: str) -> Dict[str, Any]:
        """Get weather information for a city."""
        try:
            # Check cache first
            if self.config["cache_enabled"]:
                cached_data = self._get_cached_weather(city)
                if cached_data:
                    return cached_data
            
            # Get fresh data
            weather_data = self.weather_tool.get_weather_data(city)
            
            # Cache the result
            if self.config["cache_enabled"]:
                self._cache_weather(city, weather_data)
            
            return weather_data
            
        except Exception as e:
            logger.error(f"Error getting weather for {city}: {str(e)}")
            raise
    
    def process_query(self, query: str) -> str:
        """Process a natural language weather query."""
        try:
            # Extract city from query
            city = self._extract_city_from_query(query)
            if not city:
                return "I couldn't determine which city you're asking about."
            
            # Get weather data
            weather_data = self.get_weather(city)
            
            # Format response
            return self._format_weather_response(city, weather_data)
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return f"I encountered an error while processing your weather query: {str(e)}"
    
    def _extract_city_from_query(self, query: str) -> Optional[str]:
        """Extract city name from a natural language query."""
        # Simple implementation - can be enhanced with NLP
        query = query.lower()
        if "in" in query:
            parts = query.split("in")
            if len(parts) > 1:
                return parts[1].strip()
        return None
    
    def _format_weather_response(self, city: str, weather_data: Dict[str, Any]) -> str:
        """Format weather data into a human-readable response."""
        try:
            temp = weather_data["temperature"]
            conditions = weather_data["conditions"]
            humidity = weather_data["humidity"]
            wind_speed = weather_data["wind_speed"]
            
            return (
                f"Current weather in {city}:\n"
                f"Temperature: {temp}°C\n"
                f"Conditions: {conditions}\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} m/s"
            )
        except KeyError as e:
            logger.error(f"Missing weather data field: {str(e)}")
            return "I couldn't format the weather data properly."
    
    def _get_cached_weather(self, city: str) -> Optional[Dict[str, Any]]:
        """Get cached weather data for a city."""
        if city in self.cache:
            cache_entry = self.cache[city]
            if (datetime.now() - cache_entry["timestamp"]).total_seconds() < self.cache_duration:
                return cache_entry["data"]
        return None
    
    def _cache_weather(self, city: str, weather_data: Dict[str, Any]) -> None:
        """Cache weather data for a city."""
        self.cache[city] = {
            "data": weather_data,
            "timestamp": datetime.now()
        }
    
    def clear_cache(self) -> None:
        """Clear the weather cache."""
        self.cache.clear()
    
    def get_supported_cities(self) -> list:
        """Get list of supported cities."""
        # This could be enhanced with a database or API call
        return [
            "London", "New York", "Tokyo", "Paris", "Berlin",
            "Sydney", "Dubai", "Singapore", "Moscow", "Cairo"
        ]
    
    def get_weather_history(self, city: str, days: int = 7) -> list:
        """Get historical weather data for a city."""
        try:
            return self.weather_tool.get_weather_history(city, days)
        except Exception as e:
            logger.error(f"Error getting weather history: {str(e)}")
            raise
    
    def get_weather_forecast(self, city: str, days: int = 5) -> list:
        """Get weather forecast for a city."""
        try:
            return self.weather_tool.get_weather_forecast(city, days)
        except Exception as e:
            logger.error(f"Error getting weather forecast: {str(e)}")
            raise 