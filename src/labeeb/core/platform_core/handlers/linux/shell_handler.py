"""
Linux Shell Handler for Labeeb.

This handler provides shell command execution and related functionality for Linux platforms.
Compliant with handler-architecture.mdc: single responsibility, clear input/output, robust error handling, and logging.
"""

import subprocess
import logging
from typing import Dict, Any, Optional
from labeeb.core.platform_core.handlers.base_handler import BaseHandler

logger = logging.getLogger(__name__)

class LinuxShellHandler(BaseHandler):
    """Handler for executing shell commands on Linux."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._last_result = None

    def initialize(self) -> bool:
        self._initialized = True
        logger.info("LinuxShellHandler initialized.")
        return True

    def cleanup(self) -> None:
        self._initialized = False
        self._last_result = None
        logger.info("LinuxShellHandler cleaned up.")

    def execute_command(self, command: str, timeout: Optional[int] = 30) -> Dict[str, Any]:
        """Execute a shell command and return the result.

        Args:
            command (str): The shell command to execute.
            timeout (Optional[int]): Timeout in seconds.

        Returns:
            Dict[str, Any]: Result with output, error, exit_code, and success flag.
        """
        logger.debug(f"Executing shell command: {command}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            output = result.stdout.strip()
            error = result.stderr.strip()
            exit_code = result.returncode
            success = exit_code == 0
            self._last_result = {
                "output": output,
                "error": error,
                "exit_code": exit_code,
                "success": success,
            }
            logger.info(f"Command executed: {command} (exit_code={exit_code})")
            if error:
                logger.warning(f"Command error: {error}")
            return self._last_result
        except subprocess.TimeoutExpired as e:
            logger.error(f"Command timed out: {command}")
            return {
                "output": e.stdout or "",
                "error": f"Timeout: {str(e)}",
                "exit_code": -1,
                "success": False,
            }
        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            return {
                "output": "",
                "error": str(e),
                "exit_code": -1,
                "success": False,
            }

    def get_last_result(self) -> Optional[Dict[str, Any]]:
        """Get the result of the last executed command."""
        return self._last_result

    def is_available(self) -> bool:
        """Check if the shell handler is available."""
        return self._initialized 