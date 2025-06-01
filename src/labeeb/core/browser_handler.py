"""
Browser integration for Labeeb.
This version uses the platform-specific browser handler from platform_core.
Following handler-architecture.mdc: single responsibility, clear interfaces, and proper error handling.
"""

import logging
from typing import Optional, Dict, Any, List
from labeeb.core.platform_core.platform_manager import platform_manager

logger = logging.getLogger(__name__)


class BrowserHandler:
    """Handler for browser interactions.
    
    This handler provides a unified interface for browser operations across platforms.
    Following handler-architecture.mdc: single responsibility, clear interfaces, and proper error handling.
    """

    def __init__(self, shell_handler=None):
        """Initialize the browser handler.

        Args:
            shell_handler: Optional shell handler instance for executing commands
        """
        # Get platform-specific browser handler from singleton instance
        self._platform_handler = platform_manager.get_handler("browser")

        if self._platform_handler is None:
            error_msg = f"No browser handler available for platform {platform_manager.get_platform()}"
            logger.error(error_msg)
            raise NotImplementedError(error_msg)

        # Initialize platform handler with our settings
        self._platform_handler.shell_handler = shell_handler
        logger.info(f"Browser handler initialized for platform {platform_manager.get_platform()}")

    def get_content(self, browser_name: Optional[str] = None) -> str:
        """Get content from browser tabs (titles and URLs).

        Args:
            browser_name: Specific browser to target ("chrome", "firefox", "safari", "edge")

        Returns:
            Formatted browser content or error message
        """
        try:
            return self._platform_handler.get_content(browser_name)
        except Exception as e:
            error_msg = f"Error getting browser content: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def perform_search(self, url: str, query: str, wait_time: float = 2.0) -> str:
        """Open the default browser, navigate to a URL, and perform a search.

        Args:
            url: The URL to open (e.g., 'https://www.google.com')
            query: The search query to type
            wait_time: Seconds to wait for the browser to load

        Returns:
            Status message
        """
        try:
            return self._platform_handler.perform_search(url, query, wait_time)
        except Exception as e:
            error_msg = f"Error performing search: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def execute_actions(self, browser: str, url: str, actions: List[Dict[str, Any]]) -> str:
        """Execute a series of browser automation actions.

        Args:
            browser: Browser to use
            url: URL to navigate to
            actions: List of actions to perform

        Returns:
            Status message
        """
        try:
            return self._platform_handler.execute_actions(browser, url, actions)
        except Exception as e:
            error_msg = f"Error executing browser actions: {str(e)}"
            logger.error(error_msg)
            return error_msg
