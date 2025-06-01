"""
Base config class for all configs.

---
description: Base class for all configs in the system
endpoints: [base_config]
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

class BaseConfig(ABC):
    """Base class for all configs in the system."""
    
    def __init__(self):
        """Initialize the base config."""
        self.name = "base_config"
        self.description = "Base class for all configs"
        self.version = "1.0.0"
        
        # Ensure required directories exist
        ensure_labeeb_directories()
        
        # Initialize configuration
        self.config = {}
        
        # Initialize config state
        self.state = {
            "status": "initialized",
            "last_used": None,
            "usage_count": 0,
            "error": None
        }
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate the config configuration."""
        pass
    
    def get_name(self) -> str:
        """Get the config name."""
        return self.name
    
    def get_description(self) -> str:
        """Get the config description."""
        return self.description
    
    def get_version(self) -> str:
        """Get the config version."""
        return self.version
    
    def get_config(self) -> Dict[str, Any]:
        """Get the config configuration."""
        return self.config
    
    def set_config(self, config: Dict[str, Any]) -> None:
        """Set the config configuration."""
        self.config = config
    
    def update_config(self, config: Dict[str, Any]) -> None:
        """Update the config configuration."""
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
        """Clear the config configuration."""
        self.config.clear()
    
    def get_status(self) -> Dict[str, Any]:
        """Get the config status."""
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
        """Execute the config.
        
        Args:
            input_data: Input data for the config
            
        Returns:
            Dict containing the result of executing the config
        """
        try:
            if not self.validate_config():
                return {
                    "status": "error",
                    "message": "Config configuration is invalid"
                }
            
            # Update config state
            self.state["status"] = "running"
            self.state["last_used"] = datetime.now().isoformat()
            self.state["usage_count"] += 1
            
            # Execute config
            result = self._execute_config(input_data)
            
            # Update config state
            self.state["status"] = "completed" if result["status"] == "success" else "failed"
            self.state["error"] = result.get("message")
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing config: {str(e)}")
            self.state["status"] = "failed"
            self.state["error"] = str(e)
            return {
                "status": "error",
                "message": f"Failed to execute config: {str(e)}"
            }
    
    @abstractmethod
    def _execute_config(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the config.
        
        Args:
            input_data: Input data for the config
            
        Returns:
            Dict containing the result of executing the config
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