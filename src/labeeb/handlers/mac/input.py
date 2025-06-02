"""
Mac Input Handler for managing input operations.

---
description: Handles input operations on macOS
endpoints: [mac_input_handler]
inputs: [input_command]
outputs: [input_result]
dependencies: [Quartz, logging]
auth: required
alwaysApply: true
---

- Handle keyboard input
- Manage mouse input
- Support accessibility
- Handle input permissions
- Provide input utilities
"""

import logging
from typing import Dict, Any, Optional, Tuple
import Quartz
import subprocess
import os

logger = logging.getLogger(__name__)

class MacInputHandler:
    """Handles input operations on macOS."""

    def __init__(self):
        """Initialize the Mac input handler."""
        self._has_accessibility = self._check_accessibility()
        logger.info(f"Accessibility access: {self._has_accessibility}")

    def _check_accessibility(self) -> bool:
        """
        Check if accessibility access is granted.

        Returns:
            bool: True if accessibility access is granted
        """
        try:
            # Check if we have accessibility permissions
            trusted = Quartz.AXIsProcessTrusted()
            if not trusted:
                logger.warning("Accessibility access not granted")
                self._request_accessibility()
            return trusted
        except Exception as e:
            logger.error(f"Error checking accessibility: {str(e)}")
            return False

    def _request_accessibility(self) -> None:
        """Request accessibility access."""
        try:
            # Open System Preferences to the Security & Privacy pane
            subprocess.Popen([
                "osascript",
                "-e",
                'tell application "System Preferences" to activate',
                "-e",
                'tell application "System Preferences" to set current pane to pane id "com.apple.preference.security"'
            ])
            logger.info("Opened System Preferences for accessibility access")
        except Exception as e:
            logger.error(f"Error requesting accessibility access: {str(e)}")

    def send_key(self, key: str, modifiers: Optional[list] = None) -> bool:
        """
        Send a keyboard key.

        Args:
            key: Key to send
            modifiers: Optional list of modifier keys

        Returns:
            bool: True if successful
        """
        if not self._has_accessibility:
            logger.error("Accessibility access required for keyboard input")
            return False

        try:
            # Convert key to Quartz key code
            key_code = self._get_key_code(key)
            if key_code is None:
                logger.error(f"Invalid key: {key}")
                return False

            # Create keyboard event
            event = Quartz.CGEventCreateKeyboardEvent(None, key_code, True)
            if modifiers:
                for mod in modifiers:
                    mod_code = self._get_modifier_code(mod)
                    if mod_code:
                        Quartz.CGEventSetFlags(event, mod_code)

            # Send key down
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
            # Send key up
            Quartz.CGEventSetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode, key_code)
            Quartz.CGEventSetType(event, Quartz.kCGEventKeyUp)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

            logger.info(f"Sent key: {key}")
            return True
        except Exception as e:
            logger.error(f"Error sending key {key}: {str(e)}")
            return False

    def _get_key_code(self, key: str) -> Optional[int]:
        """
        Get Quartz key code for a key.

        Args:
            key: Key to get code for

        Returns:
            Optional[int]: Key code if found
        """
        # Map common keys to Quartz key codes
        key_map = {
            "a": 0x00, "b": 0x0B, "c": 0x08, "d": 0x02,
            "e": 0x0E, "f": 0x03, "g": 0x05, "h": 0x04,
            "i": 0x22, "j": 0x26, "k": 0x28, "l": 0x25,
            "m": 0x2E, "n": 0x2D, "o": 0x1F, "p": 0x23,
            "q": 0x0C, "r": 0x0F, "s": 0x01, "t": 0x11,
            "u": 0x20, "v": 0x09, "w": 0x0D, "x": 0x07,
            "y": 0x10, "z": 0x06,
            "return": 0x24, "tab": 0x30, "space": 0x31,
            "delete": 0x33, "escape": 0x35
        }
        return key_map.get(key.lower())

    def _get_modifier_code(self, modifier: str) -> Optional[int]:
        """
        Get Quartz modifier code.

        Args:
            modifier: Modifier key name

        Returns:
            Optional[int]: Modifier code if found
        """
        modifier_map = {
            "shift": Quartz.kCGEventFlagMaskShift,
            "control": Quartz.kCGEventFlagMaskControl,
            "option": Quartz.kCGEventFlagMaskAlternate,
            "command": Quartz.kCGEventFlagMaskCommand
        }
        return modifier_map.get(modifier.lower())

    def has_accessibility(self) -> bool:
        """
        Check if accessibility access is granted.

        Returns:
            bool: True if accessibility access is granted
        """
        return self._has_accessibility 