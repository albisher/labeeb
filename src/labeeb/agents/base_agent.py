"""
Base agent class for all agents.

---
description: Base class for all agents in the system
endpoints: [base_agent]
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

class BaseAgent(ABC):
    """Base class for all agents in the system."""

    def __init__(self):
        """Initialize the base agent."""
        self.name = "base_agent"
        self.description = "Base class for all agents"
        self.version = "1.0.0"
        
        # Ensure required directories exist
        ensure_labeeb_directories()
        
        # Initialize configuration
        self.config = {}
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate the agent configuration."""
        pass
    
    def get_name(self) -> str:
        """Get the agent name."""
        return self.name
    
    def get_description(self) -> str:
        """Get the agent description."""
        return self.description

    def get_version(self) -> str:
        """Get the agent version."""
        return self.version

    def get_config(self) -> Dict[str, Any]:
        """Get the agent configuration."""
        return self.config
    
    def set_config(self, config: Dict[str, Any]) -> None:
        """Set the agent configuration."""
        self.config = config
    
    def update_config(self, config: Dict[str, Any]) -> None:
        """Update the agent configuration."""
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
        """Clear the agent configuration."""
        self.config.clear()
    
    def get_status(self) -> Dict[str, Any]:
        """Get the agent status."""
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
