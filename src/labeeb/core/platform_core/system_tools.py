"""
DEPRECATED: SystemTools logic is now handled by PlatformManager (see platform_core/platform_manager.py).
"""

# Deprecated stub for backward compatibility
from platform_core.platform_manager import PlatformManager
from labeeb.services.platform_services.common.platform_utils import get_platform_name, is_mac

import os
import platform
import subprocess
try:
    import pyautogui
except ImportError:
    raise RuntimeError("pyautogui is required for this feature. Please install it.")
except Exception as e:
    if 'DISPLAY' in str(e) or 'Xlib.error.DisplayConnectionError' in str(e):
        raise RuntimeError("GUI/display features are not available in this environment. Please run in a graphical session.")
    raise
import psutil
from datetime import datetime
from typing import Dict, Any


class SystemTools:
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get basic system information without external APIs"""
        return {
            "os": get_platform_name(),
            "os_version": platform.version(),
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage("/").percent,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    @staticmethod
    def get_weather_info() -> Dict[str, Any]:
        """Get weather information from macOS widget"""
        try:
            # On macOS, we can use the Weather widget
            if is_mac():
                # Open Weather widget
                pyautogui.hotkey("command", "space")
                pyautogui.write("weather")
                pyautogui.press("enter")

                # Wait for widget to load
                pyautogui.sleep(2)

                # Take screenshot of weather widget
                screenshot = pyautogui.screenshot(region=(100, 100, 300, 200))

                # TODO: Use OCR to extract weather information from screenshot
                # For now, return placeholder
                return {
                    "source": "macOS Weather Widget",
                    "status": "available",
                    "note": "Weather information available through macOS widget",
                }
            else:
                return {"status": "unavailable", "note": "Weather widget only available on macOS"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    @staticmethod
    def execute_command(command: str) -> Dict[str, Any]:
        """Execute a system command"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def take_screenshot(region: tuple = None) -> Dict[str, Any]:
        """Take a screenshot of the screen or a specific region"""
        try:
            screenshot = pyautogui.screenshot(region=region)
            return {"success": True, "image": screenshot}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def move_mouse(x: int, y: int) -> Dict[str, Any]:
        """Move mouse to specific coordinates"""
        try:
            pyautogui.moveTo(x, y)
            return {"success": True, "position": (x, y)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def click(x: int = None, y: int = None) -> Dict[str, Any]:
        """Click at current position or specific coordinates"""
        try:
            if x is not None and y is not None:
                pyautogui.click(x, y)
            else:
                pyautogui.click()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def type_text(text: str) -> Dict[str, Any]:
        """Type text at current position"""
        try:
            pyautogui.write(text)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
