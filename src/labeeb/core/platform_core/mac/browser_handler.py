"""
macOS Browser Handler for Labeeb.

This handler provides browser control and content retrieval functionality for macOS platforms.
Compliant with handler-architecture.mdc: single responsibility, clear input/output, robust error handling, and logging.
"""

import logging
import subprocess
from typing import Dict, Any, Optional, List
from labeeb.core.platform_core.handlers.base_handler import BaseHandler

logger = logging.getLogger(__name__)

class MacBrowserHandler(BaseHandler):
    """macOS-specific browser handler implementation."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the macOS browser handler.

        Args:
            config: Optional configuration dictionary
        """
        super().__init__(config)
        self._initialized = False
        self._supported_browsers = {
            "safari": "/Applications/Safari.app",
            "chrome": "/Applications/Google Chrome.app",
            "firefox": "/Applications/Firefox.app",
            "edge": "/Applications/Microsoft Edge.app"
        }

    def initialize(self) -> bool:
        """Initialize the handler.

        Returns:
            bool: True if initialization was successful
        """
        try:
            # Check if at least one supported browser is available
            for browser_path in self._supported_browsers.values():
                if subprocess.run(["test", "-d", browser_path], capture_output=True).returncode == 0:
                    self._initialized = True
                    logger.info("MacBrowserHandler initialized successfully.")
                    return True
            
            logger.warning("No supported browsers found")
            return False
        except Exception as e:
            logger.error(f"Error initializing MacBrowserHandler: {str(e)}")
            return False

    def cleanup(self) -> None:
        """Clean up resources."""
        self._initialized = False
        logger.info("MacBrowserHandler cleaned up.")

    def get_supported_browsers(self) -> List[str]:
        """Get list of supported browsers.

        Returns:
            List of supported browser names
        """
        return list(self._supported_browsers.keys())

    def is_browser_available(self, browser_name: str) -> bool:
        """Check if a specific browser is available.

        Args:
            browser_name: Name of the browser to check

        Returns:
            bool: True if the browser is available
        """
        if not self._initialized:
            return False

        browser_path = self._supported_browsers.get(browser_name.lower())
        if not browser_path:
            return False

        try:
            result = subprocess.run(["test", "-d", browser_path], capture_output=True)
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Error checking browser availability: {str(e)}")
            return False

    def get_browser_content(self, browser_name: Optional[str] = None) -> Dict[str, Any]:
        """Get content from the specified browser.

        Args:
            browser_name: Optional name of the browser to get content from.
                        If None, tries to get content from the active browser.

        Returns:
            Dict containing browser content information
        """
        if not self._initialized:
            return {"error": "Handler not initialized"}

        try:
            # Use AppleScript to get browser content
            script = """
            tell application "System Events"
                set frontApp to name of first application process whose frontmost is true
            end tell
            """
            
            result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
            active_app = result.stdout.strip().lower()

            if browser_name:
                if not self.is_browser_available(browser_name):
                    return {"error": f"Browser {browser_name} not available"}
                target_browser = browser_name
            else:
                # Try to determine the active browser
                for browser in self._supported_browsers:
                    if browser in active_app:
                        target_browser = browser
                        break
                else:
                    return {"error": "No active browser detected"}

            # Get content from the target browser
            # Note: This is a basic implementation. More sophisticated content retrieval
            # would require browser-specific extensions or APIs.
            return {
                "browser": target_browser,
                "active": True,
                "content": "Browser content retrieval not implemented"
            }

        except Exception as e:
            logger.error(f"Error getting browser content: {str(e)}")
            return {"error": str(e)}

    def is_available(self) -> bool:
        """Check if the browser handler is available.

        Returns:
            bool: True if the handler is available and initialized
        """
        return self._initialized 