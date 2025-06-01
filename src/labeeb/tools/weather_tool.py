"""
Weather tool for getting weather information.

This module provides functionality to get weather information using a workflow approach.
It uses web scraping to get weather data from public weather websites.

---
description: Get weather information
endpoints: [get_weather]
inputs: [location]
outputs: [temperature, conditions, humidity]
dependencies: [requests, beautifulsoup4]
auth: none
alwaysApply: false
---
"""

import os
import logging
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
from labeeb.core.config_manager import ConfigManager
import webbrowser
import time

logger = logging.getLogger(__name__)

class WeatherTool:
    """Tool for getting weather information."""
    
    def __init__(self):
        """Initialize the weather tool."""
        self.config = ConfigManager()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def get_weather(self, location: str) -> Dict[str, Any]:
        """
        Get weather information for a location using a workflow approach.
        
        Args:
            location: The location to get weather for.
            
        Returns:
            Dict containing weather information.
            
        Raises:
            Exception: If weather information cannot be retrieved.
        """
        try:
            # Step 1: Use OpenMeteo API (no API key required)
            # For Arabic locations, use the English name for geocoding
            search_location = location
            if any(ord(c) > 128 for c in location):  # Arabic location
                # Map common Arabic city names to English
                arabic_to_english = {
                    "الرياض": "Riyadh",
                    "الكويت": "Kuwait City",
                    "القاهرة": "Cairo",
                    "دبي": "Dubai",
                    "أبوظبي": "Abu Dhabi",
                    "جدة": "Jeddah",
                    "المنامة": "Manama",
                    "مسقط": "Muscat",
                    "الدوحة": "Doha",
                    "بيروت": "Beirut",
                    "عمان": "Amman",
                    "بغداد": "Baghdad",
                    "دمشق": "Damascus",
                    "طرابلس": "Tripoli",
                    "تونس": "Tunis",
                    "الجزائر": "Algiers",
                    "الرباط": "Rabat",
                    "الدار البيضاء": "Casablanca",
                    "الخرطوم": "Khartoum",
                    "صنعاء": "Sanaa"
                }
                search_location = arabic_to_english.get(location, location)
            
            url = f"https://geocoding-api.open-meteo.com/v1/search?name={search_location}&count=1"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Step 2: Get coordinates
            data = response.json()
            if not data.get("results"):
                raise Exception(f"Location not found: {location}")
                
            result = data["results"][0]
            lat = result["latitude"]
            lon = result["longitude"]
            
            # Step 3: Get weather data
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Step 4: Parse weather data
            data = response.json()
            current = data["current"]
            
            # Step 5: Map weather codes to descriptions
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
                99: "Thunderstorm with heavy hail"
            }
            
            # Step 6: Create weather info with language-specific conditions
            weather_info = {
                "temperature": current["temperature_2m"],
                "humidity": current["relative_humidity_2m"],
                "location": location
            }
            
            # Add conditions in the appropriate language
            conditions = weather_codes.get(current["weather_code"], "Unknown")
            if any(ord(c) > 128 for c in location):  # Arabic location
                # Map English conditions to Arabic
                english_to_arabic = {
                    "Clear sky": "سماء صافية",
                    "Mainly clear": "سماء صافية في الغالب",
                    "Partly cloudy": "غائم جزئياً",
                    "Overcast": "غائم",
                    "Foggy": "ضبابي",
                    "Depositing rime fog": "ضباب متجمد",
                    "Light drizzle": "رذاذ خفيف",
                    "Moderate drizzle": "رذاذ متوسط",
                    "Dense drizzle": "رذاذ كثيف",
                    "Slight rain": "مطر خفيف",
                    "Moderate rain": "مطر متوسط",
                    "Heavy rain": "مطر غزير",
                    "Slight snow": "ثلج خفيف",
                    "Moderate snow": "ثلج متوسط",
                    "Heavy snow": "ثلج كثيف",
                    "Snow grains": "حبيبات ثلج",
                    "Slight rain showers": "زخات مطر خفيفة",
                    "Moderate rain showers": "زخات مطر متوسطة",
                    "Violent rain showers": "زخات مطر شديدة",
                    "Slight snow showers": "زخات ثلج خفيفة",
                    "Heavy snow showers": "زخات ثلج شديدة",
                    "Thunderstorm": "عاصفة رعدية",
                    "Thunderstorm with slight hail": "عاصفة رعدية مع برد خفيف",
                    "Thunderstorm with heavy hail": "عاصفة رعدية مع برد شديد",
                    "Unknown": "غير معروف"
                }
                weather_info["conditions"] = english_to_arabic.get(conditions, "غير معروف")
            else:
                weather_info["conditions"] = conditions
            
            # Step 7: Log the result
            logger.info(f"Weather information retrieved for {location}: {weather_info}")
            
            return weather_info
            
        except Exception as e:
            error_msg = f"Error getting weather information: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)

    def _is_arabic(self, text: str) -> bool:
        """Check if text contains Arabic characters."""
        return any(ord(c) > 128 for c in text)
        
    def show_in_browser(self, location: str) -> None:
        """Show weather information in browser."""
        try:
            # Convert Arabic location to English for URL
            if self._is_arabic(location):
                # Map common Arabic city names to English
                arabic_to_english = {
                    "الرياض": "Riyadh",
                    "الكويت": "Kuwait City",
                    "القاهرة": "Cairo",
                    "دبي": "Dubai",
                    "أبوظبي": "Abu Dhabi",
                    "جدة": "Jeddah",
                    "المنامة": "Manama",
                    "مسقط": "Muscat",
                    "الدوحة": "Doha",
                    "بيروت": "Beirut",
                    "عمان": "Amman",
                    "بغداد": "Baghdad",
                    "دمشق": "Damascus",
                    "طرابلس": "Tripoli",
                    "تونس": "Tunis",
                    "الجزائر": "Algiers",
                    "الرباط": "Rabat",
                    "الدار البيضاء": "Casablanca",
                    "الخرطوم": "Khartoum",
                    "صنعاء": "Sanaa"
                }
                location = arabic_to_english.get(location, location)
            
            # Open weather.com in browser
            url = f"https://weather.com/weather/today/l/{location}"
            webbrowser.open(url)
            
            # Wait for browser to open
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"Error showing weather in browser: {e}")
            raise 