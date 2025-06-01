"""
Screenshot tool for capturing screen images.

This module provides functionality to take screenshots of the screen.
"""

import os
import logging
import subprocess
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class ScreenshotTool:
    """Tool for taking screenshots."""
    
    def __init__(self):
        """Initialize the screenshot tool."""
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "output", "screenshots")
        os.makedirs(self.output_dir, exist_ok=True)
        
    def take_screenshot(self, filename: str = None) -> str:
        """
        Take a screenshot of the screen.
        
        Args:
            filename: Optional filename to save the screenshot. If not provided,
                     a timestamp-based name will be generated.
                     
        Returns:
            str: Path to the saved screenshot file.
            
        Raises:
            Exception: If the screenshot capture fails.
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                
            # Ensure filename is in the output directory
            if not os.path.isabs(filename):
                filename = os.path.join(self.output_dir, filename)
                
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Take screenshot using screencapture command
            subprocess.run(["screencapture", "-x", filename], check=True)
            
            logger.info(f"Screenshot saved to: {filename}")
            return filename
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to take screenshot: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Error taking screenshot: {e}"
            logger.error(error_msg)
            raise Exception(error_msg) 