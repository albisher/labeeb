"""
GUI Automation tool for controlling applications and UI elements.

This module provides functionality to automate GUI interactions using a workflow approach.
It uses pyautogui for mouse/keyboard control and pygetwindow for window management.

---
description: Automate GUI interactions
endpoints: [move_mouse, click, type_text, open_app, get_window]
inputs: [action, target, position]
outputs: [success]
dependencies: [pyautogui, pygetwindow]
auth: none
alwaysApply: false
---
"""

import os
import logging
import pygetwindow as gw
from typing import Dict, Any, Optional, Tuple
from labeeb.core.config_manager import ConfigManager
import time

logger = logging.getLogger(__name__)

class AutomationTool:
    """Tool for automating GUI interactions."""
    
    def __init__(self):
        """Initialize the automation tool."""
        self.config = ConfigManager()
        
        # Set up safety features
        try:
            import pyautogui
            pyautogui.FAILSAFE = True  # Move mouse to corner to abort
            pyautogui.PAUSE = 0.5      # Add delay between actions
        except ImportError:
            raise RuntimeError("pyautogui is required for this feature. Please install it.")
        except Exception as e:
            if 'DISPLAY' in str(e) or 'Xlib.error.DisplayConnectionError' in str(e):
                raise RuntimeError("GUI/display features are not available in this environment. Please run in a graphical session.")
            raise
        
        # Common application names
        self.app_names = {
            "calculator": {
                "mac": "Calculator",
                "win": "Calculator",
                "linux": "Calculator"
            },
            "textedit": {
                "mac": "TextEdit",
                "win": "Notepad",
                "linux": "gedit"
            }
        }
        
    def move_mouse(self, x: int, y: int) -> Dict[str, Any]:
        """
        Move mouse to specified coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Dict containing success status
            
        Raises:
            Exception: If mouse movement fails
        """
        try:
            import pyautogui
            pyautogui.moveTo(x, y, duration=0.5)
            return {"success": True}
        except Exception as e:
            error_msg = f"Error moving mouse: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
    def click(self, x: Optional[int] = None, y: Optional[int] = None) -> Dict[str, Any]:
        """
        Click at specified coordinates or current position.
        
        Args:
            x: X coordinate (optional)
            y: Y coordinate (optional)
            
        Returns:
            Dict containing success status
            
        Raises:
            Exception: If click fails
        """
        try:
            import pyautogui
            if x is not None and y is not None:
                pyautogui.click(x, y)
            else:
                pyautogui.click()
            return {"success": True}
        except Exception as e:
            error_msg = f"Error clicking: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
    def type_text(self, text: str) -> Dict[str, Any]:
        """
        Type text at current position.
        
        Args:
            text: Text to type
            
        Returns:
            Dict containing success status
            
        Raises:
            Exception: If typing fails
        """
        try:
            import pyautogui
            pyautogui.write(text)
            return {"success": True}
        except Exception as e:
            error_msg = f"Error typing text: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
    def open_app(self, app_name: str) -> Dict[str, Any]:
        """
        Open an application.
        
        Args:
            app_name: Name of application to open
            
        Returns:
            Dict containing success status
            
        Raises:
            Exception: If app opening fails
        """
        try:
            import pyautogui
            # Get platform-specific app name
            platform = pyautogui.platform()
            app = self.app_names.get(app_name.lower(), {}).get(platform)
            if not app:
                raise ValueError(f"Application {app_name} not supported on {platform}")
                
            # Open application
            os.system(f"open -a {app}" if platform == "mac" else f"start {app}")
            time.sleep(1)  # Wait for app to open
            
            return {"success": True}
        except Exception as e:
            error_msg = f"Error opening application: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
    def get_window(self, title: str) -> Dict[str, Any]:
        """
        Get window by title.
        
        Args:
            title: Window title
            
        Returns:
            Dict containing window info
            
        Raises:
            Exception: If window not found
        """
        try:
            import pyautogui
            window = gw.getWindowsWithTitle(title)
            if not window:
                raise ValueError(f"Window with title '{title}' not found")
                
            return {
                "title": window[0].title,
                "position": (window[0].left, window[0].top),
                "size": (window[0].width, window[0].height)
            }
        except Exception as e:
            error_msg = f"Error getting window: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
    def show_calculator(self) -> Dict[str, Any]:
        """
        Show calculator and position it.
        
        Returns:
            Dict containing success status
            
        Raises:
            Exception: If calculator operation fails
        """
        try:
            import pyautogui
            # Open calculator
            self.open_app("calculator")
            
            # Get calculator window
            calc = self.get_window("Calculator")
            
            # Move to center of screen
            screen_width, screen_height = pyautogui.size()
            x = (screen_width - calc["size"][0]) // 2
            y = (screen_height - calc["size"][1]) // 2
            
            # Move window
            import pygetwindow as gw
            window = gw.getWindowsWithTitle("Calculator")[0]
            window.moveTo(x, y)
            
            return {"success": True}
        except Exception as e:
            error_msg = f"Error showing calculator: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
    def type_expression(self, expression: str) -> Dict[str, Any]:
        """
        Type expression in calculator.
        
        Args:
            expression: Expression to type
            
        Returns:
            Dict containing success status
            
        Raises:
            Exception: If typing fails
        """
        try:
            import pyautogui
            # Type each character with a small delay
            for char in expression:
                if char == "*":
                    pyautogui.press("multiply")
                elif char == "/":
                    pyautogui.press("divide")
                elif char == "+":
                    pyautogui.press("add")
                elif char == "-":
                    pyautogui.press("subtract")
                else:
                    pyautogui.press(char)
                time.sleep(0.1)
                
            return {"success": True}
        except Exception as e:
            error_msg = f"Error typing expression: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
    def press_equals(self) -> Dict[str, Any]:
        """
        Press equals in calculator.
        
        Returns:
            Dict containing success status
            
        Raises:
            Exception: If operation fails
        """
        try:
            import pyautogui
            pyautogui.press("enter")
            return {"success": True}
        except Exception as e:
            error_msg = f"Error pressing equals: {e}"
            logger.error(error_msg)
            raise Exception(error_msg) 