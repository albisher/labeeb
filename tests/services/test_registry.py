"""
Tests for the service registry.

---
description: Tests service registration and discovery
endpoints: [test_registry]
inputs: [test_services]
outputs: [test_results]
dependencies: [pytest]
auth: none
alwaysApply: false
---

- Test service registration
- Test service discovery
- Test health checks
- Test service metadata
- Test service lifecycle
"""

import pytest
from datetime import datetime
from labeeb.services.registry import ServiceRegistry

class MockService:
    """Mock service for testing."""
    def __init__(self, name: str):
        self.name = name
        self.initialized = False

    def initialize(self) -> bool:
        self.initialized = True
        return True

    def shutdown(self) -> None:
        self.initialized = False

@pytest.fixture
def registry():
    """Create a service registry for testing."""
    return ServiceRegistry()

@pytest.fixture
def mock_service():
    """Create a mock service for testing."""
    return MockService("test_service")

def test_register_service(registry, mock_service):
    """Test service registration."""
    registry.register_service("test_service", mock_service)
    assert "test_service" in registry.get_all_services()
    assert registry.get_service("test_service") == mock_service

def test_register_service_with_metadata(registry, mock_service):
    """Test service registration with metadata."""
    metadata = {"version": "1.0", "description": "Test service"}
    registry.register_service("test_service", mock_service, metadata)
    assert registry.get_service_metadata("test_service") == metadata

def test_get_nonexistent_service(registry):
    """Test getting a nonexistent service."""
    assert registry.get_service("nonexistent") is None
    assert registry.get_service_metadata("nonexistent") is None

def test_register_health_check(registry, mock_service):
    """Test health check registration."""
    def health_check(service):
        return service.initialized

    registry.register_service("test_service", mock_service)
    registry.register_health_check("test_service", health_check)
    assert not registry.check_service_health("test_service")
    mock_service.initialize()
    assert registry.check_service_health("test_service")

def test_unregister_service(registry, mock_service):
    """Test service unregistration."""
    registry.register_service("test_service", mock_service)
    registry.unregister_service("test_service")
    assert "test_service" not in registry.get_all_services()
    assert registry.get_service("test_service") is None

def test_service_status(registry, mock_service):
    """Test service status tracking."""
    registry.register_service("test_service", mock_service)
    assert registry.get_service_status("test_service") == "unknown"
    mock_service.initialize()
    registry.check_service_health("test_service")
    assert registry.get_service_status("test_service") == "healthy"

def test_health_check_error(registry, mock_service):
    """Test health check error handling."""
    def failing_health_check(service):
        raise Exception("Health check failed")

    registry.register_service("test_service", mock_service)
    registry.register_health_check("test_service", failing_health_check)
    assert not registry.check_service_health("test_service")
    assert registry.get_service_status("test_service") == "error" 