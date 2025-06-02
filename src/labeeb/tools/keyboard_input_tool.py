"""
KeyboardInputTool: Simulates keyboard input for the Labeeb agent, enabling automation of typing and keyboard shortcuts.

This tool provides keyboard input functionality while following:
- A2A (Agent-to-Agent) protocol for agent collaboration
- MCP (Multi-Channel Protocol) for unified channel support
- SmolAgents pattern for minimal, efficient implementation
"""

import logging
from typing import Dict, Any, List, Optional, Union

logger = logging.getLogger(__name__)


class KeyboardInputTool:
    """Tool for simulating keyboard input with platform-specific optimizations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the keyboard input tool.

        Args:
            config: Optional configuration dictionary
        """
        if config is None:
            config = {}
        self._typing_speed = config.get("typing_speed", 0.1)  # seconds between keystrokes
        self._key_press_delay = config.get("key_press_delay", 0.1)  # seconds to hold key
        self._last_key = None

    async def initialize(self) -> bool:
        """Initialize the tool.

        Returns:
            bool: True if initialization was successful, False otherwise
        """
        try:
            # Configure PyAutoGUI
            try:
                import pyautogui
            except ImportError:
                raise RuntimeError("pyautogui is required for this feature. Please install it.")
            except Exception as e:
                if 'DISPLAY' in str(e) or 'Xlib.error.DisplayConnectionError' in str(e):
                    raise RuntimeError("GUI/display features are not available in this environment. Please run in a graphical session.")
                raise
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.1
            return True
        except Exception as e:
            logger.error(f"Failed to initialize KeyboardInputTool: {e}")
            return False

    async def cleanup(self) -> None:
        """Clean up resources used by the tool."""
        try:
            self._last_key = None
        except Exception as e:
            logger.error(f"Error cleaning up KeyboardInputTool: {e}")

    def get_capabilities(self) -> Dict[str, bool]:
        """Get the capabilities of this tool.

        Returns:
            Dict[str, bool]: Dictionary of capability names and their availability
        """
        return {
            "type_text": True,
            "press_key": True,
            "hold_key": True,
            "release_key": True,
            "hotkey": True,
        }

    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the tool.

        Returns:
            Dict[str, Any]: Dictionary containing status information
        """
        return {
            "typing_speed": self._typing_speed,
            "key_press_delay": self._key_press_delay,
            "last_key": self._last_key,
        }

    async def _execute_command(
        self, command: str, args: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a specific command.

        Args:
            command: Command to execute
            args: Optional arguments for the command

        Returns:
            Dict[str, Any]: Result of the command execution
        """
        if command == "type":
            return await self._type_text(args)
        elif command == "press":
            return await self._press_key(args)
        elif command == "hold":
            return await self._hold_key(args)
        elif command == "release":
            return await self._release_key(args)
        elif command == "hotkey":
            return await self._press_hotkey(args)
        else:
            return {"error": f"Unknown command: {command}"}

    async def _type_text(self, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Type text at the current cursor position.

        Args:
            args: Text typing arguments

        Returns:
            Dict[str, Any]: Result of text typing
        """
        try:
            if not args or "text" not in args:
                return {"error": "Missing text parameter"}

            text = args["text"]
            interval = args.get("interval", self._typing_speed)

            try:
                import pyautogui
            except ImportError:
                raise RuntimeError("pyautogui is required for this feature. Please install it.")
            except Exception as e:
                if 'DISPLAY' in str(e) or 'Xlib.error.DisplayConnectionError' in str(e):
                    raise RuntimeError("GUI/display features are not available in this environment. Please run in a graphical session.")
                raise
            pyautogui.write(text, interval=interval)

            return {"status": "success", "action": "type", "text": text}
        except Exception as e:
            logger.error(f"Error typing text: {e}")
            return {"error": str(e)}

    async def _press_key(self, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Press and release a key.

        Args:
            args: Key press arguments

        Returns:
            Dict[str, Any]: Result of key press
        """
        try:
            if not args or "key" not in args:
                return {"error": "Missing key parameter"}

            key = args["key"]
            self._last_key = key

            try:
                import pyautogui
            except ImportError:
                raise RuntimeError("pyautogui is required for this feature. Please install it.")
            except Exception as e:
                if 'DISPLAY' in str(e) or 'Xlib.error.DisplayConnectionError' in str(e):
                    raise RuntimeError("GUI/display features are not available in this environment. Please run in a graphical session.")
                raise
            pyautogui.press(key)

            return {"status": "success", "action": "press", "key": key}
        except Exception as e:
            logger.error(f"Error pressing key: {e}")
            return {"error": str(e)}

    async def _hold_key(self, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Hold down a key.

        Args:
            args: Key hold arguments

        Returns:
            Dict[str, Any]: Result of key hold
        """
        try:
            if not args or "key" not in args:
                return {"error": "Missing key parameter"}

            key = args["key"]
            self._last_key = key

            try:
                import pyautogui
            except ImportError:
                raise RuntimeError("pyautogui is required for this feature. Please install it.")
            except Exception as e:
                if 'DISPLAY' in str(e) or 'Xlib.error.DisplayConnectionError' in str(e):
                    raise RuntimeError("GUI/display features are not available in this environment. Please run in a graphical session.")
                raise
            pyautogui.keyDown(key)

            return {"status": "success", "action": "hold", "key": key}
        except Exception as e:
            logger.error(f"Error holding key: {e}")
            return {"error": str(e)}

    async def _release_key(self, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Release a held key.

        Args:
            args: Key release arguments

        Returns:
            Dict[str, Any]: Result of key release
        """
        try:
            if not args or "key" not in args:
                return {"error": "Missing key parameter"}

            key = args["key"]
            self._last_key = None

            try:
                import pyautogui
            except ImportError:
                raise RuntimeError("pyautogui is required for this feature. Please install it.")
            except Exception as e:
                if 'DISPLAY' in str(e) or 'Xlib.error.DisplayConnectionError' in str(e):
                    raise RuntimeError("GUI/display features are not available in this environment. Please run in a graphical session.")
                raise
            pyautogui.keyUp(key)

            return {"status": "success", "action": "release", "key": key}
        except Exception as e:
            logger.error(f"Error releasing key: {e}")
            return {"error": str(e)}

    async def _press_hotkey(self, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Press a combination of keys.

        Args:
            args: Hotkey arguments

        Returns:
            Dict[str, Any]: Result of hotkey press
        """
        try:
            if not args or "keys" not in args:
                return {"error": "Missing keys parameter"}

            keys = args["keys"]
            if not isinstance(keys, (list, tuple)):
                keys = [keys]

            try:
                import pyautogui
            except ImportError:
                raise RuntimeError("pyautogui is required for this feature. Please install it.")
            except Exception as e:
                if 'DISPLAY' in str(e) or 'Xlib.error.DisplayConnectionError' in str(e):
                    raise RuntimeError("GUI/display features are not available in this environment. Please run in a graphical session.")
                raise
            pyautogui.hotkey(*keys)

            return {"status": "success", "action": "hotkey", "keys": keys}
        except Exception as e:
            logger.error(f"Error pressing hotkey: {e}")
            return {"error": str(e)}
