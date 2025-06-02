"""
Platform utilities for Labeeb.

This module provides platform-specific utilities and constants.
Following service-architecture.mdc rules.

---
description: Provides platform-specific utilities and constants
endpoints: [get_platform_name, get_os_identifier, is_windows, is_mac, is_linux]
inputs: []
outputs: [platform_name, os_identifier, platform_checks]
dependencies: []
auth: none
alwaysApply: true
---
"""

import os
import platform
import logging
from typing import Dict, Optional, Any, List

from .platform_factory import PlatformFactory

logger = logging.getLogger(__name__)

# Platform mapping from OS identifiers to canonical names
PLATFORM_MAP: Dict[str, str] = {
    "darwin": "macos",
    "win32": "windows",
    "linux": "linux"
}

def get_os_identifier() -> str:
    """Get the OS identifier.
    
    Returns:
        str: OS identifier (e.g., 'darwin', 'win32', 'linux').
    """
    return platform.system().lower()

def get_platform_name() -> str:
    """Get the canonical platform name.
    
    Returns:
        str: Canonical platform name (e.g., 'macos', 'windows', 'linux').
    """
    os_id = get_os_identifier()
    return PLATFORM_MAP.get(os_id, os_id)

def is_windows() -> bool:
    """Check if the current platform is Windows.
    
    Returns:
        bool: True if the platform is Windows, False otherwise.
    """
    return get_platform_name() == "windows"

def is_mac() -> bool:
    """Check if the current platform is macOS.
    
    Returns:
        bool: True if the platform is macOS, False otherwise.
    """
    return get_platform_name() == "macos"

def is_linux() -> bool:
    """Check if the current platform is Linux.
    
    Returns:
        bool: True if the platform is Linux, False otherwise.
    """
    return get_platform_name() == "linux"

def get_platform_info() -> Dict[str, str]:
    """Get detailed platform information.
    
    Returns:
        Dict[str, str]: Dictionary containing platform information.
    """
    return {
        "os_identifier": get_os_identifier(),
        "platform_name": get_platform_name(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }

def get_system_info() -> Dict[str, Any]:
    """Get system information."""
    return PlatformFactory.get_platform().get_system_info()


def execute_command(command: str) -> Dict[str, Any]:
    """Execute a system command."""
    return PlatformFactory.get_platform().execute_command(command)


def get_file_path(path: str) -> str:
    """Get platform-specific file path."""
    return PlatformFactory.get_platform().get_file_path(path)


def get_environment_variable(name: str) -> Optional[str]:
    """Get environment variable value."""
    return PlatformFactory.get_platform().get_environment_variable(name)


def set_environment_variable(name: str, value: str) -> bool:
    """Set environment variable value."""
    return PlatformFactory.get_platform().set_environment_variable(name, value)


def get_process_list() -> List[Dict[str, Any]]:
    """Get list of running processes."""
    return PlatformFactory.get_platform().get_process_list()


def get_network_info() -> Dict[str, Any]:
    """Get network information."""
    return PlatformFactory.get_platform().get_network_info()


def get_display_info() -> Dict[str, Any]:
    """Get display information."""
    return PlatformFactory.get_platform().get_display_info()


def get_audio_info() -> Dict[str, Any]:
    """Get audio device information."""
    return PlatformFactory.get_platform().get_audio_info()


def get_input_devices() -> Dict[str, Any]:
    """Get input device information."""
    return PlatformFactory.get_platform().get_input_devices()


def get_usb_devices() -> List[Dict[str, Any]]:
    """Get USB device information."""
    return PlatformFactory.get_platform().get_usb_devices()


def get_bluetooth_devices() -> List[Dict[str, Any]]:
    """Get Bluetooth device information."""
    return PlatformFactory.get_platform().get_bluetooth_devices()
