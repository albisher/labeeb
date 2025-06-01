import os
import sys
import subprocess
import logging
from datetime import datetime
from typing import Optional
from labeeb.core.config_manager import ConfigManager

logger = logging.getLogger(__name__)

class ScreenshotTool:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.file_config = self.config_manager.get("file_operation_settings")

    def take_screenshot(self, filename: Optional[str] = None) -> str:
        """
        Take a screenshot and save it to the screenshots directory.

        Args:
            filename: Optional filename for the screenshot. If not provided,
                     a timestamp-based name will be generated.

        Returns:
            str: Path to the saved screenshot file
        """
        try:
            # Get screenshots directory from config
            screenshots_dir = self.file_config.get_full_path(self.file_config.screenshots_dir)
            os.makedirs(screenshots_dir, exist_ok=True)

            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"

            # Ensure filename has .png extension
            if not filename.lower().endswith('.png'):
                filename += '.png'

            # Full path for the screenshot
            filepath = os.path.join(screenshots_dir, filename)

            # Take screenshot based on platform
            if sys.platform == "darwin":  # macOS
                subprocess.run(["screencapture", filepath])
            elif sys.platform == "linux":
                subprocess.run(["gnome-screenshot", "-f", filepath])
            elif sys.platform == "win32":
                import pyautogui
                screenshot = pyautogui.screenshot()
                screenshot.save(filepath)
            else:
                raise OSError(f"Unsupported platform: {sys.platform}")

            return filepath

        except Exception as e:
            logger.error(f"Error taking screenshot: {str(e)}")
            raise 