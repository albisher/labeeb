"""
User Interaction History Service for tracking user commands and responses.

---
description: Tracks and stores user interactions
endpoints: [interaction_history]
inputs: [command, response]
outputs: [interaction_record]
dependencies: [logging]
auth: none
alwaysApply: false
---

- Record user commands and responses
- Maintain interaction history
- Provide history retrieval
- Support history management
- Track interaction timestamps
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class UserInteractionHistory:
    """Tracks and stores user interactions."""

    def __init__(self, max_history: int = 1000):
        """
        Initialize the user interaction history.

        Args:
            max_history: Maximum number of interactions to store
        """
        self.max_history = max_history
        self.history: List[Dict[str, Any]] = []

    def add(self, command: str, response: str) -> None:
        """
        Add a command and response to the history.

        Args:
            command: The command that was executed
            response: The response received
        """
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "response": response
        }

        self.history.append(interaction)

        # Trim history if it exceeds max_history
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

        logger.debug(f"Added interaction to history: {interaction}")

    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get the interaction history.

        Args:
            limit: Maximum number of interactions to return

        Returns:
            List[Dict[str, Any]]: The interaction history
        """
        if limit is None:
            return self.history
        return self.history[-limit:]

    def clear_history(self) -> None:
        """Clear the interaction history."""
        self.history = []
        logger.info("Cleared interaction history")

    def get_last_interaction(self) -> Optional[Dict[str, Any]]:
        """
        Get the last interaction.

        Returns:
            Optional[Dict[str, Any]]: The last interaction, or None if no interactions have occurred
        """
        if not self.history:
            return None
        return self.history[-1]

    def get_command_history(self) -> List[str]:
        """
        Get the history of commands.

        Returns:
            List[str]: The command history
        """
        return [interaction["command"] for interaction in self.history]

    def get_response_history(self) -> List[str]:
        """
        Get the history of responses.

        Returns:
            List[str]: The response history
        """
        return [interaction["response"] for interaction in self.history]
