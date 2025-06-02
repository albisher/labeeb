"""
Error Handler Service for managing and processing errors.

---
description: Handles and processes errors in the application
endpoints: [error_handler]
inputs: [error]
outputs: [error_info]
dependencies: [logging]
auth: none
alwaysApply: false
---

- Track error occurrence
- Log error details
- Store error in history
- Provide error statistics
- Support error recovery
"""

import logging
import traceback
from typing import Optional, Dict, Any

from labeeb.core.exceptions import CommandError

logger = logging.getLogger(__name__)

class ErrorHandler:
    """Handles and processes errors in the application."""

    def __init__(self):
        """Initialize the error handler."""
        self.error_count = 0
        self.last_error: Optional[Exception] = None
        self.error_history: list[Dict[str, Any]] = []

    def handle_error(self, error: Exception) -> None:
        """
        Handle an error.

        Args:
            error: The error to handle
        """
        self.error_count += 1
        self.last_error = error

        error_info = {
            "type": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exc(),
            "timestamp": logging.Formatter.formatTime(logger, logging.Formatter())
        }

        self.error_history.append(error_info)
        logger.error(f"Error occurred: {error_info['message']}")
        logger.debug(f"Error traceback: {error_info['traceback']}")

        if isinstance(error, CommandError):
            logger.error(f"Command error: {error}")
        else:
            logger.error(f"Unexpected error: {error}")

    def get_last_error(self) -> Optional[Exception]:
        """
        Get the last error that occurred.

        Returns:
            Optional[Exception]: The last error, or None if no errors have occurred
        """
        return self.last_error

    def get_error_count(self) -> int:
        """
        Get the number of errors that have occurred.

        Returns:
            int: The number of errors
        """
        return self.error_count

    def get_error_history(self) -> list[Dict[str, Any]]:
        """
        Get the error history.

        Returns:
            list[Dict[str, Any]]: The error history
        """
        return self.error_history

    def clear_error_history(self) -> None:
        """Clear the error history."""
        self.error_count = 0
        self.last_error = None
        self.error_history = []
