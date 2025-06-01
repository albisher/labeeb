"""
Unit tests for platform handlers functionality.

---
description: Test platform handlers
endpoints: [test_platform_handlers]
inputs: []
outputs: []
dependencies: [pytest]
auth: none
alwaysApply: false
---
"""

import os
import pytest
from labeeb.core.handlers.app_handler import AppHandler
from labeeb.core.handlers.device_handler import DeviceHandler
from labeeb.core.handlers.system_handler import SystemHandler
from labeeb.utils.platform_utils import ensure_labeeb_directories

@pytest.fixture
def app_handler():
    """Create an app handler instance."""
    return AppHandler()

@pytest.fixture
def device_handler():
    """Create a device handler instance."""
    return DeviceHandler()

@pytest.fixture
def system_handler():
    """Create a system handler instance."""
    return SystemHandler()

def test_app_handler_initialization(app_handler):
    """Test app handler initialization."""
    assert app_handler is not None
    assert isinstance(app_handler, AppHandler)

def test_device_handler_initialization(device_handler):
    """Test device handler initialization."""
    assert device_handler is not None
    assert isinstance(device_handler, DeviceHandler)

def test_system_handler_initialization(system_handler):
    """Test system handler initialization."""
    assert system_handler is not None
    assert isinstance(system_handler, SystemHandler)

def test_app_handler_operations(app_handler):
    """Test app handler operations."""
    # Test launching an app
    result = app_handler.launch_app("calculator")
    assert result["status"] == "success"
    assert result["pid"] is not None
    
    # Test getting app info
    app_info = app_handler.get_app_info(result["pid"])
    assert app_info is not None
    assert "name" in app_info
    assert "path" in app_info
    
    # Test terminating the app
    terminate_result = app_handler.terminate_app(result["pid"])
    assert terminate_result["status"] == "success"

def test_device_handler_operations(device_handler):
    """Test device handler operations."""
    # Test getting connected devices
    devices = device_handler.get_connected_devices()
    assert isinstance(devices, list)
    
    # Test getting device info
    if devices:
        device_info = device_handler.get_device_info(devices[0])
        assert device_info is not None
        assert "id" in device_info
        assert "type" in device_info
    
    # Test device operations
    result = device_handler.perform_device_operation("scan")
    assert result["status"] == "success"

def test_system_handler_operations(system_handler):
    """Test system handler operations."""
    # Test getting system info
    system_info = system_handler.get_system_info()
    assert isinstance(system_info, dict)
    assert "os" in system_info
    assert "version" in system_info
    
    # Test getting system resources
    resources = system_handler.get_system_resources()
    assert isinstance(resources, dict)
    assert "cpu" in resources
    assert "memory" in resources
    assert "disk" in resources
    
    # Test system operations
    result = system_handler.perform_system_operation("cleanup")
    assert result["status"] == "success"

def test_app_handler_error_handling(app_handler):
    """Test app handler error handling."""
    # Test launching invalid app
    result = app_handler.launch_app("invalid_app")
    assert result["status"] == "error"
    assert "App not found" in result["message"]
    
    # Test getting info for invalid PID
    app_info = app_handler.get_app_info(99999)
    assert app_info is None
    
    # Test terminating invalid app
    result = app_handler.terminate_app(99999)
    assert result["status"] == "error"
    assert "Process not found" in result["message"]

def test_device_handler_error_handling(device_handler):
    """Test device handler error handling."""
    # Test getting info for invalid device
    device_info = device_handler.get_device_info("invalid_device")
    assert device_info is None
    
    # Test invalid device operation
    result = device_handler.perform_device_operation("invalid_operation")
    assert result["status"] == "error"
    assert "Invalid operation" in result["message"]

def test_system_handler_error_handling(system_handler):
    """Test system handler error handling."""
    # Test invalid system operation
    result = system_handler.perform_system_operation("invalid_operation")
    assert result["status"] == "error"
    assert "Invalid operation" in result["message"]
    
    # Test getting invalid resource
    resource = system_handler.get_resource_usage("invalid_resource")
    assert resource is None

def test_app_handler_performance(app_handler):
    """Test app handler performance."""
    import time
    
    # Test app launch performance
    start_time = time.time()
    result = app_handler.launch_app("calculator")
    end_time = time.time()
    
    assert result["status"] == "success"
    assert end_time - start_time < 2.0  # Should launch within 2 seconds
    
    # Clean up
    app_handler.terminate_app(result["pid"])

def test_device_handler_performance(device_handler):
    """Test device handler performance."""
    import time
    
    # Test device scan performance
    start_time = time.time()
    device_handler.perform_device_operation("scan")
    end_time = time.time()
    
    assert end_time - start_time < 2.0  # Should complete within 2 seconds

def test_system_handler_performance(system_handler):
    """Test system handler performance."""
    import time
    
    # Test system info retrieval performance
    start_time = time.time()
    system_handler.get_system_info()
    end_time = time.time()
    
    assert end_time - start_time < 1.0  # Should complete within 1 second 