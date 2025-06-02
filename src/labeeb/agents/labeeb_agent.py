"""
Labeeb Agent Implementation

This module implements the main Labeeb agent class.
"""

import logging
from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent
from labeeb.tools.base_tool import BaseAgentTool
from ..platform_core.ui_interface import UIInterface
from ..platform_core.net_interface import NetInterface
from ..platform_core.fs_interface import FSInterface
from ..platform_core.audio_interface import AudioInterface

logger = logging.getLogger(__name__)


class LabeebAgent(BaseAgent):
    """Labeeb agent implementation that follows A2A, MCP, and SmolAgents patterns."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Labeeb agent.

        Args:
            config: Optional configuration dictionary
        """
        super().__init__(config)
        self._ui_interface = None
        self._net_interface = None
        self._fs_interface = None
        self._audio_interface = None

    def initialize(self) -> bool:
        """Initialize the Labeeb agent.

        Returns:
            bool: True if initialization was successful, False otherwise
        """
        try:
            # Initialize platform interfaces
            self._ui_interface = UIInterface(self._config.get("ui", {}))
            self._net_interface = NetInterface(self._config.get("net", {}))
            self._fs_interface = FSInterface(self._config.get("fs", {}))
            self._audio_interface = AudioInterface(self._config.get("audio", {}))

            # Initialize base agent
            if not super().initialize():
                return False

            return True
        except Exception as e:
            logger.error(f"Failed to initialize Labeeb agent: {e}")
            return False

    def cleanup(self) -> None:
        """Clean up Labeeb agent resources."""
        try:
            # Clean up platform interfaces
            if self._ui_interface:
                self._ui_interface.cleanup()
            if self._net_interface:
                self._net_interface.cleanup()
            if self._fs_interface:
                self._fs_interface.cleanup()
            if self._audio_interface:
                self._audio_interface.cleanup()

            # Clean up base agent
            super().cleanup()
        except Exception as e:
            logger.error(f"Error cleaning up Labeeb agent: {e}")

    def _register_tools(self) -> None:
        """Register default tools for the Labeeb agent."""
        # Register platform-specific tools
        self._register_platform_tools()

        # Register agent-specific tools
        self._register_agent_tools()

    def _register_platform_tools(self) -> None:
        """Register platform-specific tools."""
        # UI tools
        self.register_tool(UITool, {"interface": self._ui_interface})

        # Network tools
        self.register_tool(NetworkTool, {"interface": self._net_interface})

        # File system tools
        self.register_tool(FileSystemTool, {"interface": self._fs_interface})

        # Audio tools
        self.register_tool(AudioTool, {"interface": self._audio_interface})

    def _register_agent_tools(self) -> None:
        """Register agent-specific tools."""
        # Agent-specific tools will be implemented here
        pass

    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about the Labeeb agent.

        Returns:
            Dict[str, Any]: Dictionary containing agent information
        """
        info = super().get_agent_info()
        info.update(
            {
                "platform_interfaces": {
                    "ui": bool(self._ui_interface),
                    "net": bool(self._net_interface),
                    "fs": bool(self._fs_interface),
                    "audio": bool(self._audio_interface),
                }
            }
        )
        return info


# Platform-specific tool implementations
class UITool(BaseAgentTool):
    """Tool for UI operations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._interface = config.get("interface")

    def initialize(self) -> bool:
        return bool(self._interface)

    def cleanup(self) -> None:
        pass

    def get_capabilities(self) -> Dict[str, bool]:
        return self._interface.get_capabilities() if self._interface else {}

    def get_status(self) -> Dict[str, Any]:
        return self._interface.get_status() if self._interface else {"error": "Not initialized"}

    def execute(self, command: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self._interface:
            return {"error": "Not initialized"}
        try:
            if command == "get_screen_info":
                return self._interface.get_screen_info()
            elif command == "get_window_list":
                return self._interface.get_window_list()
            elif command == "get_window_info":
                return self._interface.get_window_info(args.get("window_id", ""))
            elif command == "get_active_window":
                return self._interface.get_active_window()
            elif command == "get_mouse_position":
                return {"position": self._interface.get_mouse_position()}
            elif command == "get_keyboard_layout":
                return {"layout": self._interface.get_keyboard_layout()}
            elif command == "get_clipboard_content":
                return {"content": self._interface.get_clipboard_content()}
            elif command == "set_clipboard_content":
                return {"success": self._interface.set_clipboard_content(args.get("content", ""))}
            elif command == "get_ui_theme":
                return self._interface.get_ui_theme()
            elif command == "get_ui_scale":
                return {"scale": self._interface.get_ui_scale()}
            else:
                return {"error": f"Unknown command: {command}"}
        except Exception as e:
            return {"error": str(e)}

    def get_available_commands(self) -> List[str]:
        return [
            "get_screen_info",
            "get_window_list",
            "get_window_info",
            "get_active_window",
            "get_mouse_position",
            "get_keyboard_layout",
            "get_clipboard_content",
            "set_clipboard_content",
            "get_ui_theme",
            "get_ui_scale",
        ]

    def get_command_help(self, command: str) -> Dict[str, Any]:
        help_info = {
            "get_screen_info": {
                "description": "Get information about all screens/displays",
                "args": {},
            },
            "get_window_list": {"description": "Get list of all windows", "args": {}},
            "get_window_info": {
                "description": "Get information about a specific window",
                "args": {"window_id": "Window identifier"},
            },
            "get_active_window": {
                "description": "Get information about the currently active window",
                "args": {},
            },
            "get_mouse_position": {"description": "Get the current mouse position", "args": {}},
            "get_keyboard_layout": {"description": "Get the current keyboard layout", "args": {}},
            "get_clipboard_content": {
                "description": "Get the current clipboard content",
                "args": {},
            },
            "set_clipboard_content": {
                "description": "Set the clipboard content",
                "args": {"content": "Content to set"},
            },
            "get_ui_theme": {"description": "Get the current UI theme", "args": {}},
            "get_ui_scale": {"description": "Get the current UI scale", "args": {}},
        }
        return help_info.get(command, {"description": "Unknown command", "args": {}})

    def validate_command(self, command: str, args: Optional[Dict[str, Any]] = None) -> bool:
        return command in self.get_available_commands()


class NetworkTool(BaseAgentTool):
    """Tool for network operations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._interface = config.get("interface")

    def initialize(self) -> bool:
        return bool(self._interface)

    def cleanup(self) -> None:
        pass

    def get_capabilities(self) -> Dict[str, bool]:
        return self._interface.get_capabilities() if self._interface else {}

    def get_status(self) -> Dict[str, Any]:
        return self._interface.get_status() if self._interface else {"error": "Not initialized"}

    def execute(self, command: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self._interface:
            return {"error": "Not initialized"}
        try:
            return self._interface.execute_command(command, args)
        except Exception as e:
            return {"error": str(e)}

    def get_available_commands(self) -> List[str]:
        return self._interface.get_available_commands() if self._interface else []

    def get_command_help(self, command: str) -> Dict[str, Any]:
        return self._interface.get_command_help(command) if self._interface else {}

    def validate_command(self, command: str, args: Optional[Dict[str, Any]] = None) -> bool:
        return command in self.get_available_commands()


class FileSystemTool(BaseAgentTool):
    """Tool for file system operations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._interface = config.get("interface")

    def initialize(self) -> bool:
        return bool(self._interface)

    def cleanup(self) -> None:
        pass

    def get_capabilities(self) -> Dict[str, bool]:
        return self._interface.get_capabilities() if self._interface else {}

    def get_status(self) -> Dict[str, Any]:
        return self._interface.get_status() if self._interface else {"error": "Not initialized"}

    def execute(self, command: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self._interface:
            return {"error": "Not initialized"}
        try:
            return self._interface.execute_command(command, args)
        except Exception as e:
            return {"error": str(e)}

    def get_available_commands(self) -> List[str]:
        return self._interface.get_available_commands() if self._interface else []

    def get_command_help(self, command: str) -> Dict[str, Any]:
        return self._interface.get_command_help(command) if self._interface else {}

    def validate_command(self, command: str, args: Optional[Dict[str, Any]] = None) -> bool:
        return command in self.get_available_commands()


class AudioTool(BaseAgentTool):
    """Tool for audio operations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._interface = config.get("interface")

    def initialize(self) -> bool:
        return bool(self._interface)

    def cleanup(self) -> None:
        pass

    def get_capabilities(self) -> Dict[str, bool]:
        return self._interface.get_capabilities() if self._interface else {}

    def get_status(self) -> Dict[str, Any]:
        return self._interface.get_status() if self._interface else {"error": "Not initialized"}

    def execute(self, command: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self._interface:
            return {"error": "Not initialized"}
        try:
            return self._interface.execute_command(command, args)
        except Exception as e:
            return {"error": str(e)}

    def get_available_commands(self) -> List[str]:
        return self._interface.get_available_commands() if self._interface else []

    def get_command_help(self, command: str) -> Dict[str, Any]:
        return self._interface.get_command_help(command) if self._interface else {}

    def validate_command(self, command: str, args: Optional[Dict[str, Any]] = None) -> bool:
        return command in self.get_available_commands()
