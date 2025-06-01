"""
Base workflow class for all workflows.

---
description: Base class for all workflows in the system
endpoints: [base_workflow]
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

class BaseWorkflow(ABC):
    """Base class for all workflows in the system."""
    
    def __init__(self):
        """Initialize the base workflow."""
        self.name = "base_workflow"
        self.description = "Base class for all workflows"
        self.version = "1.0.0"
        
        # Ensure required directories exist
        ensure_labeeb_directories()
        
        # Initialize configuration
        self.config = {}
        
        # Initialize workflow state
        self.state = {
            "status": "initialized",
            "current_step": None,
            "steps_completed": [],
            "steps_remaining": [],
            "error": None
        }
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate the workflow configuration."""
        pass
    
    def get_name(self) -> str:
        """Get the workflow name."""
        return self.name
    
    def get_description(self) -> str:
        """Get the workflow description."""
        return self.description
    
    def get_version(self) -> str:
        """Get the workflow version."""
        return self.version
    
    def get_config(self) -> Dict[str, Any]:
        """Get the workflow configuration."""
        return self.config
    
    def set_config(self, config: Dict[str, Any]) -> None:
        """Set the workflow configuration."""
        self.config = config
    
    def update_config(self, config: Dict[str, Any]) -> None:
        """Update the workflow configuration."""
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
        """Clear the workflow configuration."""
        self.config.clear()
    
    def get_status(self) -> Dict[str, Any]:
        """Get the workflow status."""
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
        """Execute the workflow.
        
        Args:
            input_data: Input data for the workflow
            
        Returns:
            Dict containing the result of executing the workflow
        """
        try:
            if not self.validate_config():
                return {
                    "status": "error",
                    "message": "Workflow configuration is invalid"
                }
            
            # Initialize workflow state
            self.state = {
                "status": "running",
                "current_step": None,
                "steps_completed": [],
                "steps_remaining": self._get_workflow_steps(),
                "error": None
            }
            
            # Execute workflow steps
            result = self._execute_workflow(input_data)
            
            # Update workflow state
            self.state["status"] = "completed" if result["status"] == "success" else "failed"
            self.state["error"] = result.get("message")
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing workflow: {str(e)}")
            self.state["status"] = "failed"
            self.state["error"] = str(e)
            return {
                "status": "error",
                "message": f"Failed to execute workflow: {str(e)}"
            }
    
    @abstractmethod
    def _get_workflow_steps(self) -> List[str]:
        """Get the list of workflow steps.
        
        Returns:
            List of workflow step names
        """
        pass
    
    @abstractmethod
    def _execute_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the workflow steps.
        
        Args:
            input_data: Input data for the workflow
            
        Returns:
            Dict containing the result of executing the workflow
        """
        pass
    
    def _update_workflow_state(self, step: str, status: str) -> None:
        """Update the workflow state.
        
        Args:
            step: Name of the current step
            status: Status of the step
        """
        self.state["current_step"] = step
        if status == "completed":
            self.state["steps_completed"].append(step)
            if step in self.state["steps_remaining"]:
                self.state["steps_remaining"].remove(step)
        elif status == "failed":
            self.state["status"] = "failed"
    
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