"""
Base handler class for all handlers.

---
description: Base class for all handlers in the system
endpoints: [base_handler]
inputs: []
outputs: []
dependencies: []
auth: none
alwaysApply: false
---
"""

import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

from labeeb.utils.platform_utils import ensure_labeeb_directories

# Configure logging
logger = logging.getLogger(__name__)

class BaseHandler(ABC):
    """Base class for all handlers in the system."""
    
    def __init__(self):
        """Initialize the base handler."""
        self.name = "base_handler"
        self.description = "Base class for all handlers"
        self.version = "1.0.0"
        
        # Ensure required directories exist
        ensure_labeeb_directories()
        
        # Initialize configuration
        self.config = {}
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate the handler configuration."""
        pass
    
    def get_name(self) -> str:
        """Get the handler name."""
        return self.name
    
    def get_description(self) -> str:
        """Get the handler description."""
        return self.description
    
    def get_version(self) -> str:
        """Get the handler version."""
        return self.version
    
    def get_config(self) -> Dict[str, Any]:
        """Get the handler configuration."""
        return self.config
    
    def set_config(self, config: Dict[str, Any]) -> None:
        """Set the handler configuration."""
        self.config = config
    
    def update_config(self, config: Dict[str, Any]) -> None:
        """Update the handler configuration."""
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
        """Clear the handler configuration."""
        self.config.clear()
    
    def get_status(self) -> Dict[str, Any]:
        """Get the handler status."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "config_valid": self.validate_config()
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
    
    def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Handle an event.
        
        Args:
            event: Event to handle
            
        Returns:
            Dict containing the result of handling the event
        """
        try:
            if not self.validate_config():
                return {
                    "status": "error",
                    "message": "Handler configuration is invalid"
                }
            
            return self._process_event(event)
            
        except Exception as e:
            logger.error(f"Error handling event: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to handle event: {str(e)}"
            }
    
    @abstractmethod
    def _process_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Process an event.
        
        Args:
            event: Event to process
            
        Returns:
            Dict containing the result of processing the event
        """
        pass 