"""
Mouse Utilities for Labeeb

Provides atomic mouse information and state queries in a platform-agnostic way.

---
description: Atomic mouse info and state query tool
inputs: [action]
outputs: [position, error]
dependencies: [pyautogui]
alwaysApply: false
---
"""

from typing import Tuple, Optional

class Mouse:
    """Platform-agnostic mouse utility class."""

    def get_position(self) -> Tuple[Optional[int], Optional[int]]:
        """
        Get the current mouse position.
        Returns:
            tuple: (x, y) coordinates or (None, None) if unavailable
        """
        try:
            import pyautogui
            x, y = pyautogui.position()
            return x, y
        except ImportError:
            print("pyautogui is not installed. Mouse position not available.")
            return None, None
        except Exception as e:
            print(f"Mouse position query failed: {e}")
            return None, None

# Usage Example:
# mouse = Mouse()
# print(mouse.get_position())
