"""
Mac Browser Handler for managing browser operations.

---
description: Handles browser operations on macOS
endpoints: [mac_browser_handler]
inputs: [browser_command]
outputs: [browser_result]
dependencies: [subprocess, logging]
auth: none
alwaysApply: true
---

- Detect installed browsers
- Control browser operations
- Handle browser navigation
- Manage browser windows
- Support browser automation
"""

import logging
import subprocess
from typing import Dict, Any, Optional, List
import os

logger = logging.getLogger(__name__)

class MacBrowserHandler:
    """Handles browser operations on macOS."""

    def __init__(self):
        """Initialize the Mac browser handler."""
        self._browsers = self._detect_browsers()
        logger.info(f"Detected browsers: {list(self._browsers.keys())}")

    def _detect_browsers(self) -> Dict[str, str]:
        """
        Detect installed browsers.

        Returns:
            Dict[str, str]: Map of browser names to paths
        """
        browsers = {}
        browser_paths = {
            "chrome": "/Applications/Google Chrome.app",
            "firefox": "/Applications/Firefox.app",
            "safari": "/Applications/Safari.app",
            "edge": "/Applications/Microsoft Edge.app"
        }

        for name, path in browser_paths.items():
            if os.path.exists(path):
                browsers[name] = path
                logger.info(f"Detected browser: {name} at {path}")

        return browsers

    def open_browser(self, browser_name: str, url: Optional[str] = None) -> bool:
        """
        Open a browser.

        Args:
            browser_name: Name of the browser to open
            url: Optional URL to open

        Returns:
            bool: True if successful
        """
        if browser_name not in self._browsers:
            logger.error(f"Browser not found: {browser_name}")
            return False

        try:
            browser_path = self._browsers[browser_name]
            if url:
                subprocess.Popen(["open", "-a", browser_path, url])
                logger.info(f"Opened {browser_name} with URL: {url}")
            else:
                subprocess.Popen(["open", "-a", browser_path])
                logger.info(f"Opened {browser_name}")
            return True
        except Exception as e:
            logger.error(f"Error opening browser {browser_name}: {str(e)}")
            return False

    def get_installed_browsers(self) -> List[str]:
        """
        Get list of installed browsers.

        Returns:
            List[str]: List of browser names
        """
        return list(self._browsers.keys())

    def is_browser_installed(self, browser_name: str) -> bool:
        """
        Check if a browser is installed.

        Args:
            browser_name: Name of the browser to check

        Returns:
            bool: True if browser is installed
        """
        return browser_name in self._browsers

    def get_browser_path(self, browser_name: str) -> Optional[str]:
        """
        Get the path of an installed browser.

        Args:
            browser_name: Name of the browser

        Returns:
            Optional[str]: Browser path if installed
        """
        return self._browsers.get(browser_name) 