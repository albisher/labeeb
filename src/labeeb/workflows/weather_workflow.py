"""
Weather workflow for handling weather-related tasks.

---
description: Workflow for handling weather queries and forecasts
endpoints: [weather_workflow]
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
from typing import Dict, Any, Optional, List
from datetime import datetime
from dotenv import load_dotenv

from labeeb.workflows.base_workflow import BaseWorkflow
from labeeb.agents.weather_agent import WeatherAgent
from labeeb.tools.weather_tool import WeatherTool
from labeeb.utils.platform_utils import ensure_labeeb_directories

# Configure logging
logger = logging.getLogger(__name__)

class WeatherWorkflow(BaseWorkflow):
    """Workflow for handling weather-related tasks."""
    
    def __init__(self):
        """Initialize the weather workflow."""
        super().__init__()
        self.name = "weather_workflow"
        self.description = "Handles weather queries and forecasts"
        self.version = "1.0.0"
        
        # Initialize components
        self.weather_agent = WeatherAgent()
        self.weather_tool = WeatherTool()
        
        # Load environment variables
        load_dotenv()
        
        # Ensure required directories exist
        ensure_labeeb_directories()
        
        # Initialize configuration
        self.config = {
            "cache_enabled": True,
            "cache_duration": 1800,  # 30 minutes
            "max_forecast_days": 7,
            "max_history_days": 30,
            "supported_queries": [
                "current",
                "forecast",
                "history",
                "alerts"
            ]
        }
    
    def process_weather_query(self, query: str, city: Optional[str] = None) -> Dict[str, Any]:
        """Process a weather-related query."""
        try:
            # Extract city if not provided
            if not city:
                city = self._extract_city_from_query(query)
                if not city:
                    return {
                        "status": "error",
                        "message": "Could not determine city from query"
                    }
            
            # Determine query type
            query_type = self._determine_query_type(query)
            
            # Process based on query type
            if query_type == "current":
                return self._handle_current_weather(city)
            elif query_type == "forecast":
                days = self._extract_days_from_query(query)
                return self._handle_weather_forecast(city, days)
            elif query_type == "history":
                days = self._extract_days_from_query(query)
                return self._handle_weather_history(city, days)
            elif query_type == "alerts":
                return self._handle_weather_alerts(city)
            else:
                return {
                    "status": "error",
                    "message": f"Unsupported query type: {query_type}"
                }
            
        except Exception as e:
            logger.error(f"Error processing weather query: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to process weather query: {str(e)}"
            }
    
    def _extract_city_from_query(self, query: str) -> Optional[str]:
        """Extract city name from a natural language query."""
        # Simple implementation - can be enhanced with NLP
        query = query.lower()
        if "in" in query:
            parts = query.split("in")
            if len(parts) > 1:
                return parts[1].strip()
        return None
    
    def _determine_query_type(self, query: str) -> str:
        """Determine the type of weather query."""
        query = query.lower()
        if "forecast" in query:
            return "forecast"
        elif "history" in query or "past" in query:
            return "history"
        elif "alert" in query or "warning" in query:
            return "alerts"
        else:
            return "current"
    
    def _extract_days_from_query(self, query: str) -> int:
        """Extract number of days from query."""
        query = query.lower()
        if "week" in query:
            return 7
        elif "month" in query:
            return 30
        else:
            # Default to 3 days for forecast, 7 for history
            return 3 if "forecast" in query else 7
    
    def _handle_current_weather(self, city: str) -> Dict[str, Any]:
        """Handle current weather query."""
        try:
            weather_data = self.weather_agent.get_weather(city)
            return {
                "status": "success",
                "type": "current",
                "city": city,
                "data": weather_data
            }
        except Exception as e:
            logger.error(f"Error getting current weather for {city}: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get current weather: {str(e)}"
            }
    
    def _handle_weather_forecast(self, city: str, days: int) -> Dict[str, Any]:
        """Handle weather forecast query."""
        try:
            # Limit days to max_forecast_days
            days = min(days, self.config["max_forecast_days"])
            
            forecast_data = self.weather_agent.get_weather_forecast(city, days)
            return {
                "status": "success",
                "type": "forecast",
                "city": city,
                "days": days,
                "data": forecast_data
            }
        except Exception as e:
            logger.error(f"Error getting weather forecast for {city}: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get weather forecast: {str(e)}"
            }
    
    def _handle_weather_history(self, city: str, days: int) -> Dict[str, Any]:
        """Handle weather history query."""
        try:
            # Limit days to max_history_days
            days = min(days, self.config["max_history_days"])
            
            history_data = self.weather_agent.get_weather_history(city, days)
            return {
                "status": "success",
                "type": "history",
                "city": city,
                "days": days,
                "data": history_data
            }
        except Exception as e:
            logger.error(f"Error getting weather history for {city}: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get weather history: {str(e)}"
            }
    
    def _handle_weather_alerts(self, city: str) -> Dict[str, Any]:
        """Handle weather alerts query."""
        try:
            alerts_data = self.weather_tool.get_weather_alerts(city)
            return {
                "status": "success",
                "type": "alerts",
                "city": city,
                "data": alerts_data
            }
        except Exception as e:
            logger.error(f"Error getting weather alerts for {city}: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get weather alerts: {str(e)}"
            }
    
    def get_supported_cities(self) -> List[str]:
        """Get list of supported cities."""
        return self.weather_agent.get_supported_cities()
    
    def get_supported_queries(self) -> List[str]:
        """Get list of supported query types."""
        return self.config["supported_queries"]
    
    def clear_cache(self) -> None:
        """Clear the weather cache."""
        self.weather_agent.clear_cache() 