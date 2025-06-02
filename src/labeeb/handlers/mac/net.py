"""
Mac Network Handler for managing network operations.

---
description: Handles network operations on macOS
endpoints: [mac_net_handler]
inputs: [network_command]
outputs: [network_result]
dependencies: [socket, logging]
auth: none
alwaysApply: true
---

- Handle network connections
- Manage network interfaces
- Support network utilities
- Handle network errors
- Provide network status
"""

import logging
import socket
import subprocess
from typing import Dict, Any, Optional, List, Tuple

logger = logging.getLogger(__name__)

class MacNetHandler:
    """Handles network operations on macOS."""

    def __init__(self):
        """Initialize the Mac network handler."""
        self._interfaces = self._get_network_interfaces()
        logger.info(f"Detected network interfaces: {list(self._interfaces.keys())}")

    def _get_network_interfaces(self) -> Dict[str, Dict[str, Any]]:
        """
        Get network interfaces.

        Returns:
            Dict[str, Dict[str, Any]]: Map of interface names to info
        """
        interfaces = {}
        try:
            # Get list of network interfaces
            output = subprocess.check_output(["networksetup", "-listallnetworkservices"]).decode()
            for line in output.splitlines():
                if line and not line.startswith("*"):
                    interface = line.strip()
                    interfaces[interface] = self._get_interface_info(interface)
            return interfaces
        except Exception as e:
            logger.error(f"Error getting network interfaces: {str(e)}")
            return {}

    def _get_interface_info(self, interface: str) -> Dict[str, Any]:
        """
        Get information about a network interface.

        Args:
            interface: Interface name

        Returns:
            Dict[str, Any]: Interface information
        """
        try:
            info = {}
            # Get IP address
            output = subprocess.check_output(["ipconfig", "getifaddr", interface]).decode().strip()
            info["ip_address"] = output if output else None

            # Get MAC address
            output = subprocess.check_output(["ifconfig", interface]).decode()
            for line in output.splitlines():
                if "ether" in line:
                    info["mac_address"] = line.split("ether")[1].strip()
                    break

            # Get interface status
            output = subprocess.check_output(["networksetup", "-getinfo", interface]).decode()
            info["status"] = "active" if "IP address" in output else "inactive"

            return info
        except Exception as e:
            logger.error(f"Error getting interface info for {interface}: {str(e)}")
            return {}

    def get_interface_status(self, interface: str) -> Optional[str]:
        """
        Get status of a network interface.

        Args:
            interface: Interface name

        Returns:
            Optional[str]: Interface status
        """
        if interface not in self._interfaces:
            logger.warning(f"Interface not found: {interface}")
            return None
        return self._interfaces[interface].get("status")

    def get_interface_ip(self, interface: str) -> Optional[str]:
        """
        Get IP address of a network interface.

        Args:
            interface: Interface name

        Returns:
            Optional[str]: IP address
        """
        if interface not in self._interfaces:
            logger.warning(f"Interface not found: {interface}")
            return None
        return self._interfaces[interface].get("ip_address")

    def get_interface_mac(self, interface: str) -> Optional[str]:
        """
        Get MAC address of a network interface.

        Args:
            interface: Interface name

        Returns:
            Optional[str]: MAC address
        """
        if interface not in self._interfaces:
            logger.warning(f"Interface not found: {interface}")
            return None
        return self._interfaces[interface].get("mac_address")

    def get_all_interfaces(self) -> List[str]:
        """
        Get list of all network interfaces.

        Returns:
            List[str]: List of interface names
        """
        return list(self._interfaces.keys())

    def is_interface_active(self, interface: str) -> bool:
        """
        Check if a network interface is active.

        Args:
            interface: Interface name

        Returns:
            bool: True if interface is active
        """
        return self.get_interface_status(interface) == "active" 