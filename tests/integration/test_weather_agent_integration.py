"""
Integration tests for weather agent functionality.

---
description: Test weather agent integration
endpoints: [test_weather_agent]
inputs: []
outputs: []
dependencies: [pytest]
auth: none
alwaysApply: false
---
"""

import os
import pytest
from labeeb.agents.weather_agent import WeatherAgent
from labeeb.tools.weather_tool import WeatherTool
from labeeb.utils.platform_utils import ensure_labeeb_directories

@pytest.fixture
def weather_agent():
    """Create a weather agent instance."""
    return WeatherAgent()

@pytest.fixture
def weather_tool():
    """Create a weather tool instance."""
    return WeatherTool()

def test_weather_agent_initialization(weather_agent):
    """Test weather agent initialization."""
    assert weather_agent is not None
    assert isinstance(weather_agent, WeatherAgent)

def test_weather_tool_initialization(weather_tool):
    """Test weather tool initialization."""
    assert weather_tool is not None
    assert isinstance(weather_tool, WeatherTool)

def test_get_weather(weather_agent, weather_tool):
    """Test getting weather information."""
    # Test with a known city
    weather_info = weather_agent.get_weather("Cairo")
    assert weather_info is not None
    assert "temperature" in weather_info
    assert "conditions" in weather_info

def test_weather_agent_workflow(weather_agent):
    """Test complete weather agent workflow."""
    # Test weather query
    response = weather_agent.process_query("What's the weather in London?")
    assert response is not None
    assert isinstance(response, str)
    assert "temperature" in response.lower() or "weather" in response.lower()

def test_weather_tool_integration(weather_agent, weather_tool):
    """Test integration between weather agent and tool."""
    # Test tool usage through agent
    weather_info = weather_agent.get_weather("Paris")
    assert weather_info is not None
    
    # Verify tool was used
    assert weather_tool.last_query is not None
    assert "Paris" in weather_tool.last_query

def test_error_handling(weather_agent):
    """Test error handling in weather agent."""
    # Test with invalid city
    with pytest.raises(Exception):
        weather_agent.get_weather("InvalidCity123")

def test_weather_data_format(weather_agent):
    """Test weather data format."""
    weather_info = weather_agent.get_weather("Tokyo")
    assert isinstance(weather_info, dict)
    assert all(key in weather_info for key in ["temperature", "conditions", "humidity", "wind_speed"])

def test_weather_agent_configuration(weather_agent):
    """Test weather agent configuration."""
    assert weather_agent.config is not None
    assert "api_key" in weather_agent.config
    assert "units" in weather_agent.config

def test_weather_tool_configuration(weather_tool):
    """Test weather tool configuration."""
    assert weather_tool.config is not None
    assert "api_key" in weather_tool.config
    assert "units" in weather_tool.config

def test_weather_agent_caching(weather_agent):
    """Test weather data caching."""
    # First request
    weather1 = weather_agent.get_weather("Berlin")
    # Second request (should use cache)
    weather2 = weather_agent.get_weather("Berlin")
    assert weather1 == weather2

def test_weather_agent_multiple_cities(weather_agent):
    """Test handling multiple cities."""
    cities = ["New York", "London", "Tokyo", "Paris"]
    for city in cities:
        weather = weather_agent.get_weather(city)
        assert weather is not None
        assert isinstance(weather, dict)

def test_weather_agent_performance(weather_agent):
    """Test weather agent performance."""
    import time
    start_time = time.time()
    weather_agent.get_weather("Sydney")
    end_time = time.time()
    assert end_time - start_time < 5.0  # Should complete within 5 seconds

def test_weather_agent_error_recovery(weather_agent):
    """Test weather agent error recovery."""
    # Test with invalid city
    with pytest.raises(Exception):
        weather_agent.get_weather("InvalidCity123")
    
    # Should still work after error
    weather = weather_agent.get_weather("Dubai")
    assert weather is not None

def test_weather_agent_concurrent_requests(weather_agent):
    """Test concurrent weather requests."""
    import concurrent.futures
    cities = ["Rome", "Madrid", "Amsterdam", "Vienna"]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(weather_agent.get_weather, city) for city in cities]
        results = [future.result() for future in futures]
    
    assert len(results) == len(cities)
    assert all(isinstance(result, dict) for result in results)

def test_weather_agent_data_validation(weather_agent):
    """Test weather data validation."""
    weather = weather_agent.get_weather("Singapore")
    assert isinstance(weather["temperature"], (int, float))
    assert isinstance(weather["humidity"], (int, float))
    assert isinstance(weather["wind_speed"], (int, float))
    assert isinstance(weather["conditions"], str)

def test_weather_agent_config_validation(weather_agent):
    """Test weather agent configuration validation."""
    assert weather_agent.validate_config() is True
    
    # Test with invalid config
    weather_agent.config["api_key"] = None
    assert weather_agent.validate_config() is False

def test_weather_tool_error_handling(weather_tool):
    """Test weather tool error handling."""
    with pytest.raises(Exception):
        weather_tool.get_weather_data("InvalidCity123")
    
    # Should still work after error
    weather = weather_tool.get_weather_data("Moscow")
    assert weather is not None

def test_weather_agent_workflow_with_tool(weather_agent, weather_tool):
    """Test complete workflow with weather tool."""
    # Test weather query
    response = weather_agent.process_query("What's the weather in Istanbul?")
    assert response is not None
    
    # Verify tool was used
    assert weather_tool.last_query is not None
    assert "Istanbul" in weather_tool.last_query
    
    # Verify response format
    assert isinstance(response, str)
    assert any(keyword in response.lower() for keyword in ["temperature", "weather", "conditions"]) 