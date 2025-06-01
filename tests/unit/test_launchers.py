#!/usr/bin/env python3
"""
Unit tests for launcher functionality.

---
description: Test launcher functionality
endpoints: [test_launchers]
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
import asyncio
from pathlib import Path
from tkinter import Tk

# Add src to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))

from scripts.launch import LabeebCLI
from scripts.launch_gui import LabeebGUI, LabeebApp
from labeeb.launchers.app_launcher import AppLauncher
from labeeb.launchers.service_launcher import ServiceLauncher
from labeeb.utils.platform_utils import ensure_labeeb_directories

@pytest.fixture
def cli_agent():
    """Create a CLI agent instance."""
    return LabeebCLI()

@pytest.fixture
def gui_agent():
    """Create a GUI agent instance."""
    return LabeebGUI()

@pytest.fixture
def root():
    """Create a tkinter root window."""
    root = Tk()
    yield root
    root.destroy()

@pytest.fixture
def app(root):
    """Create a LabeebApp instance."""
    return LabeebApp(root)

@pytest.fixture
def app_launcher():
    """Create an app launcher instance."""
    return AppLauncher()

@pytest.fixture
def service_launcher():
    """Create a service launcher instance."""
    return ServiceLauncher()

@pytest.mark.asyncio
async def test_cli_agent_execute_command(cli_agent):
    """Test CLI agent command execution."""
    result = await cli_agent.execute("execute_command", {"command": "echo 'test'"})
    assert result["success"]
    assert "test" in result["stdout"]

@pytest.mark.asyncio
async def test_cli_agent_process_input(cli_agent):
    """Test CLI agent input processing."""
    result = await cli_agent.execute("process_input", {"input": "test message"})
    assert "response" in result

@pytest.mark.asyncio
async def test_gui_agent_execute_command(gui_agent):
    """Test GUI agent command execution."""
    result = await gui_agent.execute("execute_command", {"command": "echo 'test'"})
    assert result["success"]
    assert "test" in result["stdout"]

@pytest.mark.asyncio
async def test_gui_agent_process_input(gui_agent):
    """Test GUI agent input processing."""
    result = await gui_agent.execute("process_input", {"input": "test message"})
    assert "response" in result

def test_gui_app_creation(app):
    """Test GUI app creation."""
    assert app.agent is not None
    assert app.output_text is not None
    assert app.input_field is not None
    assert app.send_button is not None
    assert app.status_label is not None

def test_gui_app_input_handling(app):
    """Test GUI app input handling."""
    # Set test input
    app.input_field.insert(0, "test message")
    
    # Trigger input handling
    app.on_input()
    
    # Verify input field is cleared
    assert app.input_field.get() == ""
    
    # Verify output contains user message
    output_text = app.output_text.get("1.0", tk.END)
    assert "You: test message" in output_text 

def create_cli():
    """Create a LabeebCLI instance."""
    return LabeebCLI()

def create_gui():
    """Create a LabeebGUI instance."""
    return LabeebGUI()

def create_app():
    """Create a LabeebApp instance."""
    root = Tk()
    return LabeebApp(root)

def test_app_launcher_initialization(app_launcher):
    """Test app launcher initialization."""
    assert app_launcher is not None
    assert isinstance(app_launcher, AppLauncher)

def test_service_launcher_initialization(service_launcher):
    """Test service launcher initialization."""
    assert service_launcher is not None
    assert isinstance(service_launcher, ServiceLauncher)

def test_app_launch(app_launcher):
    """Test launching an application."""
    # Test launching a valid app
    result = app_launcher.launch("calculator")
    assert result["status"] == "success"
    assert result["pid"] is not None
    
    # Test launching an invalid app
    result = app_launcher.launch("invalid_app")
    assert result["status"] == "error"
    assert "Application not found" in result["message"]

def test_service_launch(service_launcher):
    """Test launching a service."""
    # Test launching a valid service
    result = service_launcher.launch("weather_service")
    assert result["status"] == "success"
    assert result["pid"] is not None
    
    # Test launching an invalid service
    result = service_launcher.launch("invalid_service")
    assert result["status"] == "error"
    assert "Service not found" in result["message"]

def test_app_termination(app_launcher):
    """Test terminating an application."""
    # Launch an app first
    launch_result = app_launcher.launch("calculator")
    assert launch_result["status"] == "success"
    
    # Test terminating the app
    result = app_launcher.terminate(launch_result["pid"])
    assert result["status"] == "success"
    
    # Test terminating non-existent app
    result = app_launcher.terminate(99999)
    assert result["status"] == "error"
    assert "Process not found" in result["message"]

def test_service_termination(service_launcher):
    """Test terminating a service."""
    # Launch a service first
    launch_result = service_launcher.launch("weather_service")
    assert launch_result["status"] == "success"
    
    # Test terminating the service
    result = service_launcher.terminate(launch_result["pid"])
    assert result["status"] == "success"
    
    # Test terminating non-existent service
    result = service_launcher.terminate(99999)
    assert result["status"] == "error"
    assert "Process not found" in result["message"]

def test_app_status(app_launcher):
    """Test checking application status."""
    # Launch an app first
    launch_result = app_launcher.launch("calculator")
    assert launch_result["status"] == "success"
    
    # Test checking status
    result = app_launcher.get_status(launch_result["pid"])
    assert result["status"] == "success"
    assert result["running"] is True
    
    # Terminate the app
    app_launcher.terminate(launch_result["pid"])
    
    # Test checking status of terminated app
    result = app_launcher.get_status(launch_result["pid"])
    assert result["status"] == "success"
    assert result["running"] is False

def test_service_status(service_launcher):
    """Test checking service status."""
    # Launch a service first
    launch_result = service_launcher.launch("weather_service")
    assert launch_result["status"] == "success"
    
    # Test checking status
    result = service_launcher.get_status(launch_result["pid"])
    assert result["status"] == "success"
    assert result["running"] is True
    
    # Terminate the service
    service_launcher.terminate(launch_result["pid"])
    
    # Test checking status of terminated service
    result = service_launcher.get_status(launch_result["pid"])
    assert result["status"] == "success"
    assert result["running"] is False

def test_app_launcher_error_handling(app_launcher):
    """Test app launcher error handling."""
    # Test launching with invalid parameters
    result = app_launcher.launch("calculator", {"invalid": "param"})
    assert result["status"] == "error"
    assert "Invalid parameters" in result["message"]
    
    # Test launching with insufficient permissions
    app_launcher.permissions = False
    result = app_launcher.launch("calculator")
    assert result["status"] == "error"
    assert "Insufficient permissions" in result["message"]

def test_service_launcher_error_handling(service_launcher):
    """Test service launcher error handling."""
    # Test launching with invalid parameters
    result = service_launcher.launch("weather_service", {"invalid": "param"})
    assert result["status"] == "error"
    assert "Invalid parameters" in result["message"]
    
    # Test launching with insufficient permissions
    service_launcher.permissions = False
    result = service_launcher.launch("weather_service")
    assert result["status"] == "error"
    assert "Insufficient permissions" in result["message"]

def test_app_launcher_performance(app_launcher):
    """Test app launcher performance."""
    import time
    
    # Test launch performance
    start_time = time.time()
    result = app_launcher.launch("calculator")
    end_time = time.time()
    
    assert result["status"] == "success"
    assert end_time - start_time < 2.0  # Should launch within 2 seconds
    
    # Clean up
    app_launcher.terminate(result["pid"])

def test_service_launcher_performance(service_launcher):
    """Test service launcher performance."""
    import time
    
    # Test launch performance
    start_time = time.time()
    result = service_launcher.launch("weather_service")
    end_time = time.time()
    
    assert result["status"] == "success"
    assert end_time - start_time < 2.0  # Should launch within 2 seconds
    
    # Clean up
    service_launcher.terminate(result["pid"]) 