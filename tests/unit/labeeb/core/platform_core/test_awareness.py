"""
Unit tests for platform awareness functionality.

---
description: Test platform awareness
endpoints: [test_awareness]
inputs: []
outputs: []
dependencies: [pytest]
auth: none
alwaysApply: false
---
"""

import os
import pytest
from labeeb.core.awareness.app_awareness import AppAwareness
from labeeb.core.awareness.device_awareness import DeviceAwareness
from labeeb.core.awareness.system_awareness import SystemAwareness
from labeeb.utils.platform_utils import ensure_labeeb_directories

@pytest.fixture
def app_awareness():
    """Create an app awareness instance."""
    return AppAwareness()

@pytest.fixture
def device_awareness():
    """Create a device awareness instance."""
    return DeviceAwareness()

@pytest.fixture
def system_awareness():
    """Create a system awareness instance."""
    return SystemAwareness()

def test_app_awareness_initialization(app_awareness):
    """Test app awareness initialization."""
    assert app_awareness is not None
    assert isinstance(app_awareness, AppAwareness)

def test_device_awareness_initialization(device_awareness):
    """Test device awareness initialization."""
    assert device_awareness is not None
    assert isinstance(device_awareness, DeviceAwareness)

def test_system_awareness_initialization(system_awareness):
    """Test system awareness initialization."""
    assert system_awareness is not None
    assert isinstance(system_awareness, SystemAwareness)

def test_app_awareness_detection(app_awareness):
    """Test app awareness detection."""
    # Test detecting running apps
    running_apps = app_awareness.get_running_apps()
    assert isinstance(running_apps, list)
    assert len(running_apps) > 0
    
    # Test detecting active app
    active_app = app_awareness.get_active_app()
    assert active_app is not None
    assert isinstance(active_app, str)

def test_device_awareness_detection(device_awareness):
    """Test device awareness detection."""
    # Test detecting connected devices
    connected_devices = device_awareness.get_connected_devices()
    assert isinstance(connected_devices, list)
    
    # Test detecting device type
    device_type = device_awareness.get_device_type()
    assert device_type is not None
    assert isinstance(device_type, str)

def test_system_awareness_detection(system_awareness):
    """Test system awareness detection."""
    # Test detecting system info
    system_info = system_awareness.get_system_info()
    assert isinstance(system_info, dict)
    assert "os" in system_info
    assert "version" in system_info
    
    # Test detecting system resources
    resources = system_awareness.get_system_resources()
    assert isinstance(resources, dict)
    assert "cpu" in resources
    assert "memory" in resources
    assert "disk" in resources

def test_app_awareness_error_handling(app_awareness):
    """Test app awareness error handling."""
    # Test with invalid app name
    result = app_awareness.get_app_info("invalid_app")
    assert result is None
    
    # Test with invalid process ID
    result = app_awareness.get_process_info(99999)
    assert result is None

def test_device_awareness_error_handling(device_awareness):
    """Test device awareness error handling."""
    # Test with invalid device ID
    result = device_awareness.get_device_info("invalid_device")
    assert result is None
    
    # Test with invalid device type
    result = device_awareness.get_devices_by_type("invalid_type")
    assert isinstance(result, list)
    assert len(result) == 0

def test_system_awareness_error_handling(system_awareness):
    """Test system awareness error handling."""
    # Test with invalid resource type
    result = system_awareness.get_resource_usage("invalid_resource")
    assert result is None
    
    # Test with invalid metric
    result = system_awareness.get_system_metric("invalid_metric")
    assert result is None

def test_app_awareness_performance(app_awareness):
    """Test app awareness performance."""
    import time
    
    # Test app detection performance
    start_time = time.time()
    app_awareness.get_running_apps()
    end_time = time.time()
    
    assert end_time - start_time < 1.0  # Should complete within 1 second

def test_device_awareness_performance(device_awareness):
    """Test device awareness performance."""
    import time
    
    # Test device detection performance
    start_time = time.time()
    device_awareness.get_connected_devices()
    end_time = time.time()
    
    assert end_time - start_time < 1.0  # Should complete within 1 second

def test_system_awareness_performance(system_awareness):
    """Test system awareness performance."""
    import time
    
    # Test system info detection performance
    start_time = time.time()
    system_awareness.get_system_info()
    end_time = time.time()
    
    assert end_time - start_time < 1.0  # Should complete within 1 second 