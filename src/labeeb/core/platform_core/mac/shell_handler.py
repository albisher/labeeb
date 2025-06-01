"""
macOS Shell Handler for Labeeb.

This handler provides shell command execution and related functionality for macOS platforms.
Compliant with handler-architecture.mdc: single responsibility, clear input/output, robust error handling, and logging.
"""

import subprocess
import logging
from typing import Dict, Any, List, Tuple, Optional
from labeeb.core.platform_core.shell_handler import BaseShellHandler, CommandSafetyLevel

logger = logging.getLogger(__name__)

class MacShellHandler(BaseShellHandler):
    """macOS-specific shell handler implementation."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the macOS shell handler.

        Args:
            config: Optional configuration dictionary
        """
        super().__init__(
            safe_mode=config.get("safe_mode", True) if config else True,
            enable_dangerous_command_check=config.get("enable_dangerous_command_check", True) if config else True,
            suppress_prompt=config.get("suppress_prompt", False) if config else False,
            quiet_mode=config.get("quiet_mode", False) if config else False,
            fast_mode=config.get("fast_mode", False) if config else False,
        )
        self._initialized = False
        self._last_result = None

    def initialize(self) -> bool:
        """Initialize the handler.

        Returns:
            bool: True if initialization was successful
        """
        try:
            # Test shell availability
            result = subprocess.run(["zsh", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                self._initialized = True
                logger.info("MacShellHandler initialized successfully.")
                return True
            else:
                logger.error("Failed to initialize MacShellHandler: zsh not available")
                return False
        except Exception as e:
            logger.error(f"Error initializing MacShellHandler: {str(e)}")
            return False

    def cleanup(self) -> None:
        """Clean up resources."""
        self._initialized = False
        self._last_result = None
        logger.info("MacShellHandler cleaned up.")

    def get_safe_commands(self) -> List[str]:
        """Get the list of safe commands for macOS.

        Returns:
            List of safe command names
        """
        return [
            "ls", "pwd", "cd", "cat", "echo", "grep", "find", "which",
            "date", "whoami", "hostname", "uname", "sw_vers", "ps",
            "top", "df", "du", "wc", "head", "tail", "sort", "uniq",
            "diff", "mkdir", "touch", "cp", "mv", "rm", "chmod", "chown",
            "tar", "gzip", "gunzip", "zip", "unzip", "curl", "wget",
            "ping", "traceroute", "netstat", "ifconfig", "dig", "nslookup",
            "screencapture", "say", "afplay", "osascript"
        ]

    def get_dangerous_commands(self) -> List[str]:
        """Get the list of dangerous commands for macOS.

        Returns:
            List of dangerous command names
        """
        return [
            "rm -rf", "sudo", "mkfs", "shutdown", "reboot", "dd",
            "fdisk", "kill", "chmod 777", "chown root", "format",
            "diskutil eraseDisk", "diskutil partitionDisk",
            "sudo rm", "sudo mkfs", "sudo dd", "sudo fdisk",
            "sudo chmod", "sudo chown", "sudo format",
            "sudo diskutil", "sudo shutdown", "sudo reboot"
        ]

    def execute_command(
        self, command: str, force_shell: bool = False, timeout: Optional[int] = None
    ) -> Tuple[int, str, str]:
        """Execute a shell command on macOS.

        Args:
            command: The command to execute
            force_shell: Whether to force shell execution
            timeout: Command timeout in seconds

        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        if not self._initialized:
            logger.error("MacShellHandler not initialized")
            return -1, "", "Handler not initialized"

        try:
            # Check command safety if enabled
            if self.safe_mode and not self.is_command_safe(command):
                logger.warning(f"Command not in safe list: {command}")
                return -1, "", "Command not in safe list"

            if self.enable_dangerous_command_check and self.is_potentially_dangerous(command):
                logger.warning(f"Potentially dangerous command: {command}")
                if not self.suppress_prompt:
                    # TODO: Implement user prompt for dangerous commands
                    return -1, "", "Dangerous command blocked"

            # Fix command for macOS if needed
            command = self.fix_platform_command(command)

            # Execute the command
            process = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            self._last_result = (process.returncode, process.stdout, process.stderr)
            return self._last_result

        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {command}")
            return -1, "", "Command timed out"
        except Exception as e:
            logger.error(f"Error executing command: {str(e)}")
            return -1, "", str(e)

    def fix_platform_command(self, command: str) -> str:
        """Fix command for macOS-specific requirements.

        Args:
            command: The command string to fix

        Returns:
            Fixed command string
        """
        # Add macOS-specific command fixes here
        # For example, ensure commands use zsh instead of bash
        if command.startswith("#!/bin/bash"):
            command = command.replace("#!/bin/bash", "#!/bin/zsh")
        return command

    def is_available(self) -> bool:
        """Check if the shell handler is available.

        Returns:
            bool: True if the handler is available and initialized
        """
        return self._initialized 