"""
Weather tool for getting weather information.

This module provides functionality to get weather information by scraping weather websites.

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
        Get weather information for a location.
        
        Args:
            location: The location to get weather for.
            
        Returns:
            Dict containing weather information.
            
        Raises:
            Exception: If weather information cannot be retrieved.
        """
        try:
            # Use wttr.in for both English and Arabic locations
            url = f"https://wttr.in/{location}?format=j1"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            current = data["current_condition"][0]
            
            return {
                "temperature": current["temp_C"],
                "conditions": current["lang_ar"][0]["value"] if any(ord(c) > 128 for c in location) else current["lang_en"][0]["value"],
                "humidity": current["humidity"],
                "location": location
            }
            
        except Exception as e:
            error_msg = f"Error getting weather information: {e}"
            logger.error(error_msg)
            raise Exception(error_msg) 