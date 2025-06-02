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

This workflow processes weather queries and provides weather information
for specified cities. It supports current weather, forecasts, historical data,
and weather alerts.

Features:
- Input validation and sanitization
- Error handling with retries
- Performance monitoring
- Structured logging with correlation IDs
- Caching support

Example:
    workflow = WeatherWorkflow()
    result = workflow.process_weather_query("What's the weather in London?")
    print(result)
    
Error Handling:
- Retries failed API calls up to 3 times
- Validates all inputs before processing
- Provides detailed error messages
- Logs all errors with context
    
Performance:
- Monitors response times
- Tracks cache hits/misses
- Logs performance metrics
"""

import os
import json
import logging
import time
import uuid
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from dotenv import load_dotenv

from labeeb.workflows.base_workflow import BaseWorkflow
from labeeb.agents.weather_agent import WeatherAgent
from labeeb.tools.weather_tool import WeatherTool
from labeeb.utils.platform_utils import ensure_labeeb_directories

# Configure logging with structured format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(correlation_id)s] - %(message)s'
)
logger = logging.getLogger(__name__)

class WeatherWorkflowError(Exception):
    """Base exception for weather workflow errors."""
    pass

class CityNotFoundError(WeatherWorkflowError):
    """Raised when a city cannot be found or determined."""
    pass

class InvalidQueryError(WeatherWorkflowError):
    """Raised when a query is invalid or unsupported."""
    pass

class WeatherAPIError(WeatherWorkflowError):
    """Raised when there's an error with the weather API."""
    pass

class InputValidationError(WeatherWorkflowError):
    """Raised when input validation fails."""
    pass

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
            ],
            "max_retries": 3,
            "retry_delay": 1,  # seconds
            "max_query_length": 200,
            "min_query_length": 3,
            "log_level": "INFO",
            "performance_metrics": True
        }
        
        # Initialize metrics
        self.metrics = {
            "total_queries": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "errors": 0,
            "avg_response_time": 0,
            "performance_data": []
        }
        
        # Set up logging
        self._setup_logging()
        
        logger.info(f"Initialized {self.name} workflow v{self.version}")
    
    def _setup_logging(self) -> None:
        """Set up structured logging with correlation IDs."""
        class CorrelationFilter(logging.Filter):
            def filter(self, record):
                record.correlation_id = getattr(record, 'correlation_id', 'N/A')
                return True
        
        # Add correlation filter to logger
        correlation_filter = CorrelationFilter()
        logger.addFilter(correlation_filter)
        
        # Set log level from config
        logger.setLevel(self.config["log_level"])
    
    def _generate_correlation_id(self) -> str:
        """Generate a unique correlation ID for request tracking."""
        return str(uuid.uuid4())
    
    def _validate_input(self, query: str, city: Optional[str] = None) -> None:
        """Validate input parameters.
        
        Args:
            query: The weather query string
            city: Optional city name
            
        Raises:
            InputValidationError: If validation fails
        """
        if not query or not isinstance(query, str):
            raise InputValidationError("Query must be a non-empty string")
        
        if len(query) < self.config["min_query_length"]:
            raise InputValidationError(f"Query must be at least {self.config['min_query_length']} characters")
        
        if len(query) > self.config["max_query_length"]:
            raise InputValidationError(f"Query must not exceed {self.config['max_query_length']} characters")
        
        if city and not isinstance(city, str):
            raise InputValidationError("City must be a string if provided")
    
    def _retry_with_backoff(self, func: callable, *args, **kwargs) -> Any:
        """Retry a function with exponential backoff.
        
        Args:
            func: The function to retry
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            The result of the function call
            
        Raises:
            WeatherAPIError: If all retries fail
        """
        last_error = None
        for attempt in range(self.config["max_retries"]):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < self.config["max_retries"] - 1:
                    delay = self.config["retry_delay"] * (2 ** attempt)
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {str(e)}")
                    time.sleep(delay)
        
        raise WeatherAPIError(f"All retry attempts failed: {str(last_error)}")
    
    def _update_metrics(self, start_time: float, cache_hit: bool = False) -> None:
        """Update performance metrics.
        
        Args:
            start_time: Start time of the operation
            cache_hit: Whether the result was from cache
        """
        self.metrics["total_queries"] += 1
        if cache_hit:
            self.metrics["cache_hits"] += 1
        else:
            self.metrics["cache_misses"] += 1
        
        response_time = time.time() - start_time
        self.metrics["avg_response_time"] = (
            (self.metrics["avg_response_time"] * (self.metrics["total_queries"] - 1) + response_time)
            / self.metrics["total_queries"]
        )
        
        if self.config["performance_metrics"]:
            self.metrics["performance_data"].append({
                "timestamp": datetime.now().isoformat(),
                "response_time": response_time,
                "cache_hit": cache_hit
            })
    
    def process_weather_query(self, query: str, city: Optional[str] = None) -> Dict[str, Any]:
        """Process a weather-related query.
        
        Args:
            query: The weather query string
            city: Optional city name. If not provided, will attempt to extract from query
            
        Returns:
            Dict containing weather information and status
            
        Raises:
            CityNotFoundError: If city cannot be determined
            InvalidQueryError: If query is invalid or unsupported
            WeatherAPIError: If there's an error with the weather API
            InputValidationError: If input validation fails
        """
        correlation_id = self._generate_correlation_id()
        logger.info(f"[{correlation_id}] Processing weather query: {query} for city: {city}")
        start_time = time.time()
        
        try:
            # Validate input
            self._validate_input(query, city)
            
            # Extract city if not provided
            if not city:
                city = self._extract_city_from_query(query)
                if not city:
                    raise CityNotFoundError("Could not determine city from query")
            
            # Determine query type
            query_type = self._determine_query_type(query)
            if query_type not in self.config["supported_queries"]:
                raise InvalidQueryError(f"Unsupported query type: {query_type}")
            
            # Process based on query type
            result = None
            if query_type == "current":
                result = self._handle_current_weather(city)
            elif query_type == "forecast":
                days = self._extract_days_from_query(query)
                result = self._handle_weather_forecast(city, days)
            elif query_type == "history":
                days = self._extract_days_from_query(query)
                result = self._handle_weather_history(city, days)
            elif query_type == "alerts":
                result = self._handle_weather_alerts(city)
            
            # Update metrics
            self._update_metrics(start_time)
            
            logger.info(f"[{correlation_id}] Successfully processed {query_type} query for {city}")
            return result
            
        except WeatherWorkflowError as e:
            self.metrics["errors"] += 1
            logger.error(f"[{correlation_id}] Weather workflow error: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "correlation_id": correlation_id
            }
        except Exception as e:
            self.metrics["errors"] += 1
            logger.error(f"[{correlation_id}] Unexpected error processing weather query: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to process weather query: {str(e)}",
                "correlation_id": correlation_id
            }
    
    def _extract_city_from_query(self, query: str) -> Optional[str]:
        """Extract city name from a natural language query.
        
        Args:
            query: The natural language query string
            
        Returns:
            Optional[str]: The extracted city name or None if not found
        """
        logger.debug(f"Extracting city from query: {query}")
        query = query.lower()
        if "in" in query:
            parts = query.split("in")
            if len(parts) > 1:
                city = parts[1].strip()
                logger.debug(f"Extracted city: {city}")
                return city
        logger.debug("No city found in query")
        return None
    
    def _determine_query_type(self, query: str) -> str:
        """Determine the type of weather query.
        
        Args:
            query: The weather query string
            
        Returns:
            str: The type of query (current, forecast, history, or alerts)
        """
        logger.debug(f"Determining query type for: {query}")
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
        """Extract number of days from query.
        
        Args:
            query: The weather query string
            
        Returns:
            int: Number of days to process
        """
        logger.debug(f"Extracting days from query: {query}")
        query = query.lower()
        if "week" in query:
            return 7
        elif "month" in query:
            return 30
        else:
            # Default to 3 days for forecast, 7 for history
            days = 3 if "forecast" in query else 7
            logger.debug(f"Using default days: {days}")
            return days
    
    def _handle_current_weather(self, city: str) -> Dict[str, Any]:
        """Handle current weather query.
        
        Args:
            city: The city to get weather for
            
        Returns:
            Dict containing current weather information
            
        Raises:
            WeatherAPIError: If there's an error getting weather data
        """
        logger.info(f"Getting current weather for {city}")
        try:
            weather_data = self._retry_with_backoff(self.weather_agent.get_weather, city)
            return {
                "status": "success",
                "type": "current",
                "city": city,
                "data": weather_data
            }
        except Exception as e:
            logger.error(f"Error getting current weather for {city}: {str(e)}")
            raise WeatherAPIError(f"Failed to get current weather: {str(e)}")
    
    def _handle_weather_forecast(self, city: str, days: int) -> Dict[str, Any]:
        """Handle weather forecast query.
        
        Args:
            city: The city to get forecast for
            days: Number of days to forecast
            
        Returns:
            Dict containing forecast information
            
        Raises:
            WeatherAPIError: If there's an error getting forecast data
        """
        logger.info(f"Getting {days}-day forecast for {city}")
        try:
            # Limit days to max_forecast_days
            days = min(days, self.config["max_forecast_days"])
            
            forecast_data = self._retry_with_backoff(
                self.weather_agent.get_weather_forecast,
                city,
                days
            )
            return {
                "status": "success",
                "type": "forecast",
                "city": city,
                "days": days,
                "data": forecast_data
            }
        except Exception as e:
            logger.error(f"Error getting weather forecast for {city}: {str(e)}")
            raise WeatherAPIError(f"Failed to get weather forecast: {str(e)}")
    
    def _handle_weather_history(self, city: str, days: int) -> Dict[str, Any]:
        """Handle weather history query.
        
        Args:
            city: The city to get history for
            days: Number of days of history to retrieve
            
        Returns:
            Dict containing historical weather information
            
        Raises:
            WeatherAPIError: If there's an error getting historical data
        """
        logger.info(f"Getting {days}-day weather history for {city}")
        try:
            # Limit days to max_history_days
            days = min(days, self.config["max_history_days"])
            
            history_data = self._retry_with_backoff(
                self.weather_agent.get_weather_history,
                city,
                days
            )
            return {
                "status": "success",
                "type": "history",
                "city": city,
                "days": days,
                "data": history_data
            }
        except Exception as e:
            logger.error(f"Error getting weather history for {city}: {str(e)}")
            raise WeatherAPIError(f"Failed to get weather history: {str(e)}")
    
    def _handle_weather_alerts(self, city: str) -> Dict[str, Any]:
        """Handle weather alerts query.
        
        Args:
            city: The city to get alerts for
            
        Returns:
            Dict containing weather alert information
            
        Raises:
            WeatherAPIError: If there's an error getting alert data
        """
        logger.info(f"Getting weather alerts for {city}")
        try:
            alerts_data = self._retry_with_backoff(
                self.weather_tool.get_weather_alerts,
                city
            )
            return {
                "status": "success",
                "type": "alerts",
                "city": city,
                "data": alerts_data
            }
        except Exception as e:
            logger.error(f"Error getting weather alerts for {city}: {str(e)}")
            raise WeatherAPIError(f"Failed to get weather alerts: {str(e)}")
    
    def get_supported_cities(self) -> List[str]:
        """Get list of supported cities.
        
        Returns:
            List[str]: List of supported city names
        """
        logger.debug("Getting list of supported cities")
        try:
            return self._retry_with_backoff(self.weather_agent.get_supported_cities)
        except Exception as e:
            logger.error(f"Error getting supported cities: {str(e)}")
            raise WeatherAPIError(f"Failed to get supported cities: {str(e)}")
    
    def get_supported_queries(self) -> List[str]:
        """Get list of supported query types.
        
        Returns:
            List[str]: List of supported query types
        """
        logger.debug("Getting list of supported queries")
        return self.config["supported_queries"]
    
    def clear_cache(self) -> None:
        """Clear the weather cache."""
        logger.info("Clearing weather cache")
        try:
            self._retry_with_backoff(self.weather_agent.clear_cache)
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            raise WeatherAPIError(f"Failed to clear cache: {str(e)}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics.
        
        Returns:
            Dict containing current metrics
        """
        return {
            "total_queries": self.metrics["total_queries"],
            "cache_hits": self.metrics["cache_hits"],
            "cache_misses": self.metrics["cache_misses"],
            "errors": self.metrics["errors"],
            "avg_response_time": self.metrics["avg_response_time"],
            "cache_hit_rate": (
                self.metrics["cache_hits"] / self.metrics["total_queries"]
                if self.metrics["total_queries"] > 0
                else 0
            ),
            "performance_data": self.metrics["performance_data"] if self.config["performance_metrics"] else None
        } 