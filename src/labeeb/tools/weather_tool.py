"""
Weather tool for making weather API calls.

---
description: Tool for making weather API calls and processing weather data
endpoints: [weather_tool]
inputs: [city, query_type]
outputs: [weather_data]
dependencies: [requests, python-dotenv]
auth: api_key
alwaysApply: false
---
"""

import os
import json
import logging
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dotenv import load_dotenv

from labeeb.tools.base_tool import BaseTool
from labeeb.utils.platform_utils import ensure_labeeb_directories

# Configure logging
logger = logging.getLogger(__name__)

class WeatherTool(BaseTool):
    """Tool for making weather API calls and processing weather data."""
    
    def __init__(self):
        """Initialize the weather tool."""
        super().__init__()
        self.name = "weather_tool"
        self.description = "Makes weather API calls and processes weather data"
        self.version = "1.0.0"
        
        # Load environment variables
        load_dotenv()
        
        # Ensure required directories exist
        ensure_labeeb_directories()
        
        # Initialize configuration
        self.config = {
            "api_key": os.getenv("WEATHER_API_KEY"),
            "api_base_url": "https://api.weatherapi.com/v1",
            "units": "metric",
            "language": "en",
            "timeout": 10,  # seconds
            "max_retries": 3
        }
    
    def get_weather_data(self, city: str) -> Dict[str, Any]:
        """Get current weather data for a city."""
        try:
            url = f"{self.config['api_base_url']}/current.json"
            params = {
                "key": self.config["api_key"],
                "q": city,
                "units": self.config["units"],
                "lang": self.config["language"]
            }
            
            response = self._make_api_request(url, params)
            return self._process_current_weather(response)
            
        except Exception as e:
            logger.error(f"Error getting weather data for {city}: {str(e)}")
            raise
    
    def get_weather_forecast(self, city: str, days: int = 3) -> List[Dict[str, Any]]:
        """Get weather forecast for a city."""
        try:
            url = f"{self.config['api_base_url']}/forecast.json"
            params = {
                "key": self.config["api_key"],
                "q": city,
                "days": days,
                "units": self.config["units"],
                "lang": self.config["language"]
            }
            
            response = self._make_api_request(url, params)
            return self._process_forecast(response)
            
        except Exception as e:
            logger.error(f"Error getting weather forecast for {city}: {str(e)}")
            raise
    
    def get_weather_history(self, city: str, days: int = 7) -> List[Dict[str, Any]]:
        """Get historical weather data for a city."""
        try:
            history_data = []
            for i in range(days):
                date = (datetime.now() - timedelta(days=i+1)).strftime("%Y-%m-%d")
                url = f"{self.config['api_base_url']}/history.json"
                params = {
                    "key": self.config["api_key"],
                    "q": city,
                    "dt": date,
                    "units": self.config["units"],
                    "lang": self.config["language"]
                }
                
                response = self._make_api_request(url, params)
                history_data.append(self._process_history(response))
            
            return history_data
            
        except Exception as e:
            logger.error(f"Error getting weather history for {city}: {str(e)}")
            raise
    
    def get_weather_alerts(self, city: str) -> List[Dict[str, Any]]:
        """Get weather alerts for a city."""
        try:
            url = f"{self.config['api_base_url']}/alerts.json"
            params = {
                "key": self.config["api_key"],
                "q": city,
                "lang": self.config["language"]
            }
            
            response = self._make_api_request(url, params)
            return self._process_alerts(response)
            
        except Exception as e:
            logger.error(f"Error getting weather alerts for {city}: {str(e)}")
            raise
    
    def _make_api_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make an API request with retries."""
        for attempt in range(self.config["max_retries"]):
            try:
                response = requests.get(
                    url,
                    params=params,
                    timeout=self.config["timeout"]
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == self.config["max_retries"] - 1:
                    raise
                logger.warning(f"API request failed (attempt {attempt + 1}): {str(e)}")
                continue
    
    def _process_current_weather(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process current weather data."""
        try:
            current = data["current"]
            location = data["location"]
            
            return {
                "temperature": current["temp_c"],
                "feels_like": current["feelslike_c"],
                "conditions": current["condition"]["text"],
                "humidity": current["humidity"],
                "wind_speed": current["wind_kph"],
                "wind_direction": current["wind_dir"],
                "pressure": current["pressure_mb"],
                "precipitation": current["precip_mm"],
                "cloud_cover": current["cloud"],
                "uv_index": current["uv"],
                "location": {
                    "name": location["name"],
                    "region": location["region"],
                    "country": location["country"],
                    "lat": location["lat"],
                    "lon": location["lon"],
                    "timezone": location["tz_id"]
                },
                "last_updated": current["last_updated"]
            }
        except KeyError as e:
            logger.error(f"Missing field in current weather data: {str(e)}")
            raise
    
    def _process_forecast(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process forecast data."""
        try:
            forecast = []
            for day in data["forecast"]["forecastday"]:
                forecast.append({
                    "date": day["date"],
                    "max_temp": day["day"]["maxtemp_c"],
                    "min_temp": day["day"]["mintemp_c"],
                    "avg_temp": day["day"]["avgtemp_c"],
                    "conditions": day["day"]["condition"]["text"],
                    "humidity": day["day"]["avghumidity"],
                    "precipitation": day["day"]["totalprecip_mm"],
                    "chance_of_rain": day["day"]["daily_chance_of_rain"],
                    "chance_of_snow": day["day"]["daily_chance_of_snow"],
                    "uv_index": day["day"]["uv"],
                    "sunrise": day["astro"]["sunrise"],
                    "sunset": day["astro"]["sunset"],
                    "moonrise": day["astro"]["moonrise"],
                    "moonset": day["astro"]["moonset"],
                    "moon_phase": day["astro"]["moon_phase"]
                })
            return forecast
        except KeyError as e:
            logger.error(f"Missing field in forecast data: {str(e)}")
            raise
    
    def _process_history(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process historical weather data."""
        try:
            day = data["forecast"]["forecastday"][0]["day"]
            return {
                "date": data["forecast"]["forecastday"][0]["date"],
                "max_temp": day["maxtemp_c"],
                "min_temp": day["mintemp_c"],
                "avg_temp": day["avgtemp_c"],
                "conditions": day["condition"]["text"],
                "humidity": day["avghumidity"],
                "precipitation": day["totalprecip_mm"],
                "uv_index": day["uv"]
            }
        except KeyError as e:
            logger.error(f"Missing field in history data: {str(e)}")
            raise
    
    def _process_alerts(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process weather alerts data."""
        try:
            alerts = []
            if "alerts" in data and "alert" in data["alerts"]:
                for alert in data["alerts"]["alert"]:
                    alerts.append({
                        "headline": alert["headline"],
                        "msgtype": alert["msgtype"],
                        "severity": alert["severity"],
                        "urgency": alert["urgency"],
                        "areas": alert["areas"],
                        "category": alert["category"],
                        "certainty": alert["certainty"],
                        "event": alert["event"],
                        "note": alert["note"],
                        "effective": alert["effective"],
                        "expires": alert["expires"],
                        "desc": alert["desc"],
                        "instruction": alert["instruction"]
                    })
            return alerts
        except KeyError as e:
            logger.error(f"Missing field in alerts data: {str(e)}")
            raise 