"""
Base tool class for all tools.

---
description: Base class for all tools in the system
endpoints: [base_tool]
inputs: []
outputs: []
dependencies: []
auth: none
alwaysApply: false
---
"""

import logging
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

from labeeb.utils.platform_utils import ensure_labeeb_directories

# Configure logging
logger = logging.getLogger(__name__)

class BaseTool(ABC):
    """Base class for all tools in the system."""

    def __init__(self):
        """Initialize the base tool."""
        self.name = "base_tool"
        self.description = "Base class for all tools"
        self.version = "1.0.0"
        
        # Ensure required directories exist
        ensure_labeeb_directories()
        
        # Initialize configuration
        self.config = {}
        
        # Initialize tool state
        self.state = {
            "status": "initialized",
            "last_used": None,
            "usage_count": 0,
            "error": None
        }

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate the tool configuration."""
        pass
    
    def get_name(self) -> str:
        """Get the tool name."""
        return self.name
    
    def get_description(self) -> str:
        """Get the tool description."""
        return self.description
    
    def get_version(self) -> str:
        """Get the tool version."""
        return self.version
    
    def get_config(self) -> Dict[str, Any]:
        """Get the tool configuration."""
        return self.config
    
    def set_config(self, config: Dict[str, Any]) -> None:
        """Set the tool configuration."""
        self.config = config
    
    def update_config(self, config: Dict[str, Any]) -> None:
        """Update the tool configuration."""
        self.config.update(config)
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def set_config_value(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self.config[key] = value
    
    def remove_config_value(self, key: str) -> None:
        """Remove a configuration value."""
        self.config.pop(key, None)
    
    def has_config_value(self, key: str) -> bool:
        """Check if a configuration value exists."""
        return key in self.config
    
    def clear_config(self) -> None:
        """Clear the tool configuration."""
        self.config.clear()
    
    def get_status(self) -> Dict[str, Any]:
        """Get the tool status."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "config_valid": self.validate_config(),
            "state": self.state
        }
    
    def log_info(self, message: str) -> None:
        """Log an info message."""
        logger.info(f"[{self.name}] {message}")
    
    def log_warning(self, message: str) -> None:
        """Log a warning message."""
        logger.warning(f"[{self.name}] {message}")
    
    def log_error(self, message: str) -> None:
        """Log an error message."""
        logger.error(f"[{self.name}] {message}")
    
    def log_debug(self, message: str) -> None:
        """Log a debug message."""
        logger.debug(f"[{self.name}] {message}")
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool.

        Args:
            input_data: Input data for the tool

        Returns:
            Dict containing the result of executing the tool
        """
        try:
            if not self.validate_config():
                return {
                    "status": "error",
                    "message": "Tool configuration is invalid"
                }
            
            # Update tool state
            self.state["status"] = "running"
            self.state["last_used"] = datetime.now().isoformat()
            self.state["usage_count"] += 1
            
            # Execute tool
            result = self._execute_tool(input_data)
            
            # Update tool state
            self.state["status"] = "completed" if result["status"] == "success" else "failed"
            self.state["error"] = result.get("message")
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing tool: {str(e)}")
            self.state["status"] = "failed"
            self.state["error"] = str(e)
            return {
                "status": "error",
                "message": f"Failed to execute tool: {str(e)}"
            }

    @abstractmethod
    def _execute_tool(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool.

        Args:
            input_data: Input data for the tool

        Returns:
            Dict containing the result of executing the tool
        """
        pass

    def _validate_input_data(self, input_data: Dict[str, Any]) -> bool:
        """Validate the input data.

        Args:
            input_data: Input data to validate

        Returns:
            True if input data is valid, False otherwise
        """
        required_fields = self.get_config_value("required_input_fields", [])
        return all(field in input_data for field in required_fields)

    def _validate_output_data(self, output_data: Dict[str, Any]) -> bool:
        """Validate the output data.
        
        Args:
            output_data: Output data to validate

        Returns:
            True if output data is valid, False otherwise
        """
        required_fields = self.get_config_value("required_output_fields", [])
        return all(field in output_data for field in required_fields)
    
    def _format_error(self, error: Exception) -> Dict[str, Any]:
        """Format an error for the output.
        
        Args:
            error: Exception to format

        Returns:
            Dict containing the formatted error
        """
        return {
            "status": "error",
            "message": str(error),
            "type": error.__class__.__name__
        }

    def _format_success(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format success data for the output.

        Args:
            data: Data to format

        Returns:
            Dict containing the formatted success data
        """
        return {
            "status": "success",
            "data": data
        }

class BaseAgentTool(BaseTool):
    """Abstract base class for all agent tools, following agent-tool conventions."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.config = config or {}
        self.name = self.__class__.__name__
        self.description = getattr(self, 'description', 'Agent tool base class')

    @abstractmethod
    def execute(self, command: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute an agent tool command. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def get_available_commands(self) -> List[str]:
        """Return a list of available commands for this agent tool."""
        pass

    @abstractmethod
    def validate_command(self, command: str, args: Optional[Dict[str, Any]] = None) -> bool:
        """Validate if the command and arguments are supported by this tool."""
        pass

    @abstractmethod
    def get_command_help(self, command: str) -> Dict[str, Any]:
        """Return help information for a specific command."""
        pass

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the agent tool. Return True if successful."""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up any resources used by the agent tool."""
        pass

    @abstractmethod
    def get_capabilities(self) -> Dict[str, bool]:
        """Return a dictionary of the tool's capabilities."""
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Return the current status of the tool."""
        pass
