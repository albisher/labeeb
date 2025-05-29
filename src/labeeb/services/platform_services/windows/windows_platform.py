"""
Windows Platform Implementation

This module provides the Windows-specific implementation of the platform interface.
"""
import os
import sys
import platform
import subprocess
from typing import Dict, Any
from ..common.platform_interface import PlatformInterface

class WindowsPlatform(PlatformInterface):
    """Windows-specific platform implementation."""
    
    def __init__(self):
        """Initialize the Windows platform implementation."""
        self._initialized = False
        self._platform_info = None
    
    def initialize(self) -> None:
        """Initialize platform-specific components."""
        if not self._initialized:
            self._platform_info = self._get_platform_info()
            self._initialized = True
    
    def cleanup(self) -> None:
        """Clean up platform-specific resources."""
        self._initialized = False
        self._platform_info = None
    
    def get_platform_info(self) -> Dict[str, Any]:
        """Get platform-specific information."""
        if not self._platform_info:
            self._platform_info = self._get_platform_info()
        return self._platform_info
    
    def is_platform_supported(self) -> bool:
        """Check if the current platform is supported."""
        return sys.platform == 'win32'
    
    def get_system_resources(self) -> Dict[str, Any]:
        """Get system resource information."""
        return {
            'cpu_count': os.cpu_count(),
            'memory': self._get_memory_info(),
            'disk': self._get_disk_info()
        }
    
    def get_system_locale(self) -> Dict[str, Any]:
        """Get system locale information."""
        return {
            'language': os.environ.get('LANG', ''),
            'lc_all': os.environ.get('LC_ALL', ''),
            'lc_messages': os.environ.get('LC_MESSAGES', '')
        }
    
    def get_environment_variables(self) -> Dict[str, str]:
        """Get environment variables."""
        return dict(os.environ)
    
    def get_system_paths(self) -> Dict[str, str]:
        """Get system-specific paths."""
        return {
            'home': os.path.expanduser('~'),
            'temp': os.environ.get('TEMP', ''),
            'app_data': os.environ.get('APPDATA', ''),
            'local_app_data': os.environ.get('LOCALAPPDATA', '')
        }
    
    def _get_platform_info(self) -> Dict[str, Any]:
        """Get detailed platform information."""
        return {
            'system': platform.system(),
            'node': platform.node(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor()
        }
    
    def _get_memory_info(self) -> Dict[str, Any]:
        """Get memory information."""
        try:
            result = subprocess.run(['wmic', 'OS', 'get', 'FreePhysicalMemory,TotalVisibleMemorySize', '/Value'],
                                 capture_output=True, text=True)
            return {'memory_info': result.stdout}
        except Exception as e:
            return {'error': str(e)}
    
    def _get_disk_info(self) -> Dict[str, Any]:
        """Get disk information."""
        try:
            result = subprocess.run(['wmic', 'logicaldisk', 'get', 'size,freespace,caption'],
                                 capture_output=True, text=True)
            return {'disk_info': result.stdout}
        except Exception as e:
            return {'error': str(e)} 