"""
AI Command Extractor Service for processing AI model responses.

---
description: Extracts and validates commands from AI model responses
endpoints: [command_extractor]
inputs: [response]
outputs: [success, command_plan, metadata]
dependencies: [json, logging]
auth: none
alwaysApply: false
---

- Parse AI model response as JSON
- Validate response structure
- Extract command plan
- Validate command plan fields
- Return extraction result with metadata
"""

import json
import logging
from typing import Tuple, Dict, Any, Optional

from labeeb.core.exceptions import CommandError

logger = logging.getLogger(__name__)


class AICommandExtractor:
    """Extracts commands from AI model responses."""

    def extract_command(
        self, response: str
    ) -> Tuple[bool, Optional[Dict[str, Any]], Dict[str, Any]]:
        """
        Extract command from AI model response.

        Args:
            response: The AI model response text

        Returns:
            Tuple containing:
            - bool: Success status
            - Optional[Dict]: Command plan if successful
            - Dict: Metadata about the extraction
        """
        try:
            # Try to parse the response as JSON
            response_data = json.loads(response)

            # Validate the response structure
            if not isinstance(response_data, dict) or "plan" not in response_data:
                return (
                    False,
                    None,
                    {
                        "error_message": "Invalid response format: missing plan",
                        "response": response,
                    },
                )

            plan = response_data["plan"]
            if not isinstance(plan, list):
                return (
                    False,
                    None,
                    {"error_message": "Invalid plan format: not a list", "response": response},
                )

            # Validate each step in the plan
            for step in plan:
                if not isinstance(step, dict):
                    return (
                        False,
                        None,
                        {
                            "error_message": "Invalid step format: not a dictionary",
                            "response": response,
                        },
                    )

                required_fields = ["step", "description", "operation", "parameters"]
                for field in required_fields:
                    if field not in step:
                        return (
                            False,
                            None,
                            {
                                "error_message": f"Invalid step format: missing {field}",
                                "response": response,
                            },
                        )

            return True, response_data, {"steps": len(plan), "response": response}

        except json.JSONDecodeError:
            return (
                False,
                None,
                {"error_message": "Failed to parse response as JSON", "response": response},
            )
        except Exception as e:
            logger.error(f"Error extracting command: {str(e)}")
            return (
                False,
                None,
                {"error_message": f"Error extracting command: {str(e)}", "response": response},
            )

    def validate_command(self, command: Dict[str, Any]) -> bool:
        """
        Validate a command structure.

        Args:
            command: The command to validate

        Returns:
            bool: True if command is valid, False otherwise
        """
        try:
            if not isinstance(command, dict):
                return False

            required_fields = ["action", "parameters"]
            for field in required_fields:
                if field not in command:
                    return False

            return True
        except Exception as e:
            logger.error(f"Error validating command: {str(e)}")
            return False
