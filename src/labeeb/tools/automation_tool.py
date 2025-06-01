"""
Automation tool module for Labeeb.

This module provides functionality to automate UI interactions.
It uses pyautogui for mouse/keyboard control and window management.

---
description: Automate UI interactions
endpoints: [move_mouse, click, type_text, get_window_info, open_application]
inputs: [x, y, text, app_name]
outputs: [success]
dependencies: [pyautogui, psutil]
auth: none
alwaysApply: false
---
"""

import os
import time
import logging
import pyautogui
import psutil
from typing import Dict, Any, Optional, List, Tuple
from labeeb.core.config_manager import ConfigManager

logger = logging.getLogger(__name__)

class AutomationTool:
    """Tool for UI automation."""
    
    def __init__(self):
        """Initialize the automation tool."""
        self.config = ConfigManager()
        # Configure pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5  # Add delay between actions
        
    def move_mouse(self, x: int, y: int) -> bool:
        """
        Move mouse to specified coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if movement was successful
            
        Raises:
            Exception: If movement fails
        """
        try:
            pyautogui.moveTo(x, y, duration=0.5)
            return True
        except Exception as e:
            logger.error(f"Error moving mouse: {e}")
            raise
            
    def click(self, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """
        Click at current or specified position.
        
        Args:
            x: Optional X coordinate
            y: Optional Y coordinate
            
        Returns:
            True if click was successful
            
        Raises:
            Exception: If click fails
        """
        try:
            if x is not None and y is not None:
                pyautogui.click(x, y)
            else:
                pyautogui.click()
            return True
        except Exception as e:
            logger.error(f"Error clicking: {e}")
            raise
            
    def type_text(self, text: str) -> bool:
        """
        Type text at current position.
        
        Args:
            text: Text to type
            
        Returns:
            True if typing was successful
            
        Raises:
            Exception: If typing fails
        """
        try:
            pyautogui.write(text, interval=0.1)
            return True
        except Exception as e:
            logger.error(f"Error typing text: {e}")
            raise
            
    def get_window_info(self) -> List[Dict[str, Any]]:
        """
        Get information about open windows.
        
        Returns:
            List of window information dictionaries
            
        Raises:
            Exception: If getting window info fails
        """
        try:
            windows = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name']:
                        windows.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name']
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return windows
        except Exception as e:
            logger.error(f"Error getting window info: {e}")
            raise
            
    def open_application(self, app_name: str) -> bool:
        """
        Open an application.
        
        Args:
            app_name: Name of application to open
            
        Returns:
            True if application was opened successfully
            
        Raises:
            Exception: If opening application fails
        """
        try:
            # Map common app names to commands
            app_commands = {
                'notepad': 'notepad.exe',
                'textedit': 'open -a TextEdit',
                'calculator': 'calc.exe',
                'terminal': 'terminal.exe'
            }
            
            if app_name.lower() in app_commands:
                os.system(app_commands[app_name.lower()])
                time.sleep(1)  # Wait for app to open
                return True
            else:
                raise ValueError(f"Unknown application: {app_name}")
                
        except Exception as e:
            logger.error(f"Error opening application: {e}")
            raise
            
    def save_file(self, filename: str, folder: str) -> bool:
        """
        Save file in specified folder.
        
        Args:
            filename: Name of file to save
            folder: Folder to save in
            
        Returns:
            True if save was successful
            
        Raises:
            Exception: If save fails
        """
        try:
            # Type filename
            self.type_text(filename)
            
            # Press Tab to move to folder field
            pyautogui.press('tab')
            
            # Type folder path
            self.type_text(folder)
            
            # Press Enter to save
            pyautogui.press('enter')
            
            return True
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            raise 