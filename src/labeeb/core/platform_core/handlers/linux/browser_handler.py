"""
Linux browser handler for Labeeb.

Provides platform-specific browser control for Linux, including opening URLs, performing searches, and (future) tab management.

WARNING: Do NOT import platform_manager at the module level. Always import it inside methods to avoid circular import issues.

---
description: Linux browser handler
inputs: [action, url, tab_index, query, wait_time, actions]
outputs: [success, error, content, status]
dependencies: [webbrowser, pyautogui (optional)]
alwaysApply: true
---
"""

import logging
from typing import Optional, Dict, Any, List
from labeeb.core.platform_core.handlers.base_handler import BaseHandler

logger = logging.getLogger(__name__)

class LinuxBrowserHandler(BaseHandler):
    """Handler for Linux browser control."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._initialized = True
        self._supported_browsers = ["firefox", "chrome", "chromium", "brave", "opera"]
        self._rtl_support = False
        self._text_direction = "ltr"

    def initialize(self) -> bool:
        self._initialized = True
        return True

    def cleanup(self) -> None:
        self._initialized = False

    def open_url(self, url: str, browser: Optional[str] = None) -> Dict[str, Any]:
        """Open a URL in the default or specified browser."""
        try:
            import webbrowser
            if browser and browser in self._supported_browsers:
                webbrowser.get(using=browser).open(url)
            else:
                webbrowser.open(url)
            return {"success": True, "error": None}
        except Exception as e:
            logger.error(f"Failed to open URL: {e}")
            return {"success": False, "error": str(e)}

    def get_content(self, browser_name: Optional[str] = None) -> str:
        """Get content from browser tabs (not supported on Linux without browser automation)."""
        return "Getting browser tab content is not supported on Linux without browser automation (e.g., Selenium)."

    def perform_search(self, url: str, query: str, wait_time: float = 2.0) -> str:
        """Open a browser, navigate to a URL, and perform a search (best effort)."""
        try:
            import webbrowser
            webbrowser.open(url)
            import time
            time.sleep(wait_time)
            try:
                import pyautogui
                pyautogui.typewrite(query)
                pyautogui.press('enter')
                return f"Search for '{query}' performed in browser."
            except ImportError:
                return f"Opened {url} in browser. (pyautogui not available for typing search)"
        except Exception as e:
            logger.error(f"Failed to perform search: {e}")
            return f"Error performing search: {str(e)}"

    def execute_actions(self, browser: str, url: str, actions: List[Dict[str, Any]]) -> str:
        """Execute a series of browser automation actions (best effort, limited on Linux)."""
        try:
            import webbrowser
            webbrowser.open(url)
            import time
            time.sleep(2)
            try:
                import pyautogui
                for action in actions:
                    action_type = action.get("type")
                    if action_type == "click":
                        x, y = action.get("x"), action.get("y")
                        if x is not None and y is not None:
                            pyautogui.click(x, y)
                    elif action_type == "type":
                        text = action.get("text", "")
                        if text:
                            pyautogui.typewrite(text)
                    elif action_type == "key":
                        key = action.get("key")
                        if key:
                            pyautogui.press(key)
                return f"Successfully executed {len(actions)} actions in {browser}"
            except ImportError:
                return f"Opened {url} in browser. (pyautogui not available for automation)"
        except Exception as e:
            logger.error(f"Failed to execute browser actions: {e}")
            return f"Error executing browser actions: {str(e)}"

    def is_browser_available(self, browser_id: str) -> bool:
        """Check if a browser is available (best effort)."""
        import shutil
        return shutil.which(browser_id) is not None

    def get_available_browsers(self) -> List[str]:
        """Return a list of supported browsers that are installed."""
        import shutil
        return [b for b in self._supported_browsers if shutil.which(b)]

    def _initialize_rtl_support(self) -> None:
        self._rtl_support = False
        self._text_direction = "ltr"

    # Placeholder for tab management and close functionality
    # Real implementation would require selenium or browser-specific APIs 