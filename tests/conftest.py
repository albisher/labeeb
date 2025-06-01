"""
Test configuration and fixtures for Labeeb tests.

This module provides test configuration and fixtures used across all tests.

---
description: Test configuration and fixtures
endpoints: [pytest_configure, pytest_collection_modifyitems]
inputs: []
outputs: []
dependencies: [pytest]
auth: none
alwaysApply: false
---
"""

import os
import sys
import pytest
import logging
from pathlib import Path

# Add src to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, src_path)

from labeeb.utils.platform_utils import ensure_labeeb_directories
from labeeb.tools.tts_tool import TTSTool
from labeeb.tools.stt_tool import STTTool
from labeeb.tools.calculator_tool import CalculatorTool
from labeeb.tools.weather_tool import WeatherTool

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/test.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def base_dir():
    """Return the base directory for test files."""
    return ensure_labeeb_directories()

@pytest.fixture(scope="session")
def test_files_dir(base_dir):
    """Return the directory for test files."""
    test_dir = os.path.join(base_dir, "tests", "test_files")
    os.makedirs(test_dir, exist_ok=True)
    return test_dir

@pytest.fixture(scope="session")
def results_dir(base_dir):
    """Return the directory for test results."""
    results_dir = os.path.join(base_dir, "tests", "results")
    os.makedirs(results_dir, exist_ok=True)
    return results_dir

@pytest.fixture(scope="session")
def tts_tool():
    """Return a TTSTool instance."""
    return TTSTool()

@pytest.fixture(scope="session")
def stt_tool():
    """Return an STTTool instance."""
    return STTTool()

@pytest.fixture(scope="session")
def calculator_tool():
    """Return a CalculatorTool instance."""
    return CalculatorTool()

@pytest.fixture(scope="session")
def weather_tool():
    """Return a WeatherTool instance."""
    return WeatherTool()

def pytest_configure(config):
    """Configure pytest."""
    # Add custom markers
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "e2e: mark test as end-to-end test")
    config.addinivalue_line("markers", "unit: mark test as unit test")
    
    # Create necessary directories
    base_dir = ensure_labeeb_directories()
    for dir_name in ["logs", "output", "tests/results", "tests/test_files"]:
        os.makedirs(os.path.join(base_dir, dir_name), exist_ok=True)

def pytest_collection_modifyitems(items):
    """Modify test items after collection."""
    # Sort tests by type (unit, integration, e2e)
    unit_tests = []
    integration_tests = []
    e2e_tests = []
    other_tests = []
    
    for item in items:
        if "unit" in item.keywords:
            unit_tests.append(item)
        elif "integration" in item.keywords:
            integration_tests.append(item)
        elif "e2e" in item.keywords:
            e2e_tests.append(item)
        else:
            other_tests.append(item)
            
    # Reorder items
    items[:] = unit_tests + integration_tests + e2e_tests + other_tests 