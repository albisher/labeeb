"""
Application handler for managing application lifecycle.

---
description: Handles application launch, termination, and status
endpoints: [app_handler]
inputs: [app_name, pid]
outputs: [status, pid]
dependencies: [psutil]
auth: none
alwaysApply: false
---
"""

import os
import sys
import logging
import psutil
from typing import Dict, Any, Optional, List
from pathlib import Path

from labeeb.core.handlers.base_handler import BaseHandler
from labeeb.utils.platform_utils import ensure_labeeb_directories

# Configure logging
logger = logging.getLogger(__name__)

class AppHandler(BaseHandler):
    """Handler for managing application lifecycle."""
    
    def __init__(self):
        """Initialize the app handler."""
        super().__init__()
        self.name = "app_handler"
        self.description = "Manages application lifecycle"
        self.version = "1.0.0"
        
        # Ensure required directories exist
        ensure_labeeb_directories()
        
        # Initialize configuration
        self.config = {
            "supported_apps": self._get_supported_apps(),
            "launch_timeout": 10,  # seconds
            "terminate_timeout": 5,  # seconds
            "check_interval": 1  # seconds
        }
    
    def _get_supported_apps(self) -> Dict[str, Dict[str, Any]]:
        """Get dictionary of supported applications."""
        return {
            "calculator": {
                "name": "Calculator",
                "path": self._get_app_path("calculator"),
                "args": [],
                "env": {}
            },
            "textedit": {
                "name": "TextEdit",
                "path": self._get_app_path("textedit"),
                "args": [],
                "env": {}
            },
            "terminal": {
                "name": "Terminal",
                "path": self._get_app_path("terminal"),
                "args": [],
                "env": {}
            }
        }
    
    def _get_app_path(self, app_name: str) -> str:
        """Get the path to an application."""
        if sys.platform == "darwin":
            return f"/Applications/{app_name.capitalize()}.app"
        elif sys.platform == "win32":
            return f"C:\\Program Files\\{app_name}\\{app_name}.exe"
        else:
            return f"/usr/bin/{app_name}"
    
    def launch_app(self, app_name: str, args: List[str] = None, env: Dict[str, str] = None) -> Dict[str, Any]:
        """Launch an application."""
        try:
            if app_name not in self.config["supported_apps"]:
                return {
                    "status": "error",
                    "message": f"Application {app_name} is not supported"
                }
            
            app_config = self.config["supported_apps"][app_name]
            app_path = app_config["path"]
            
            if not os.path.exists(app_path):
                return {
                    "status": "error",
                    "message": f"Application not found at {app_path}"
                }
            
            # Prepare launch arguments
            launch_args = app_config["args"] + (args or [])
            launch_env = {**app_config["env"], **(env or {})}
            
            # Launch the application
            process = psutil.Popen(
                [app_path] + launch_args,
                env=launch_env,
                start_new_session=True
            )
            
            # Wait for process to start
            try:
                process.wait(timeout=self.config["launch_timeout"])
            except psutil.TimeoutExpired:
                process.kill()
                return {
                    "status": "error",
                    "message": "Application launch timed out"
                }
            
            return {
                "status": "success",
                "pid": process.pid,
                "message": f"Application {app_name} launched successfully"
            }
            
        except Exception as e:
            logger.error(f"Error launching application {app_name}: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to launch application: {str(e)}"
            }
    
    def terminate_app(self, pid: int) -> Dict[str, Any]:
        """Terminate an application by PID."""
        try:
            process = psutil.Process(pid)
            process.terminate()
            
            # Wait for process to terminate
            try:
                process.wait(timeout=self.config["terminate_timeout"])
            except psutil.TimeoutExpired:
                process.kill()
                return {
                    "status": "error",
                    "message": "Application termination timed out"
                }
            
            return {
                "status": "success",
                "message": f"Application with PID {pid} terminated successfully"
            }
            
        except psutil.NoSuchProcess:
            return {
                "status": "error",
                "message": f"No process found with PID {pid}"
            }
        except Exception as e:
            logger.error(f"Error terminating process {pid}: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to terminate process: {str(e)}"
            }
    
    def get_app_info(self, pid: int) -> Optional[Dict[str, Any]]:
        """Get information about a running application."""
        try:
            process = psutil.Process(pid)
            return {
                "pid": pid,
                "name": process.name(),
                "path": process.exe(),
                "status": process.status(),
                "create_time": process.create_time(),
                "cpu_percent": process.cpu_percent(),
                "memory_percent": process.memory_percent()
            }
        except psutil.NoSuchProcess:
            return None
        except Exception as e:
            logger.error(f"Error getting app info for PID {pid}: {str(e)}")
            return None
    
    def get_running_apps(self) -> List[Dict[str, Any]]:
        """Get list of running applications."""
        try:
            running_apps = []
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    app_info = self.get_app_info(proc.info['pid'])
                    if app_info:
                        running_apps.append(app_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return running_apps
        except Exception as e:
            logger.error(f"Error getting running apps: {str(e)}")
            return []
    
    def is_app_running(self, app_name: str) -> bool:
        """Check if an application is running."""
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() == app_name.lower():
                    return True
            return False
        except Exception as e:
            logger.error(f"Error checking if app {app_name} is running: {str(e)}")
            return False
    
    def get_app_status(self, pid: int) -> Dict[str, Any]:
        """Get the status of an application."""
        try:
            process = psutil.Process(pid)
            return {
                "status": "success",
                "running": process.is_running(),
                "pid": pid,
                "name": process.name(),
                "cpu_percent": process.cpu_percent(),
                "memory_percent": process.memory_percent()
            }
        except psutil.NoSuchProcess:
            return {
                "status": "success",
                "running": False,
                "pid": pid
            }
        except Exception as e:
            logger.error(f"Error getting app status for PID {pid}: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get app status: {str(e)}"
            } 