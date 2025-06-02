"""
Mouse Control Tool for Labeeb

Provides atomic mouse movement and click operations in a platform-agnostic way.

---
description: Atomic mouse movement and click tool
inputs: [action, x, y, button]
outputs: [success, error]
dependencies: [pyautogui, Xlib (Linux)]
alwaysApply: false
---
"""

from typing import Optional

class MouseControlTool:
    """Tool for controlling the mouse (move, click) in a platform-agnostic way."""

    def move(self, x: int, y: int) -> bool:
        """
        Move the mouse to the specified (x, y) coordinates.
        Args:
            x (int): X coordinate
            y (int): Y coordinate
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            import pyautogui
            pyautogui.moveTo(x, y)
            return True
        except ImportError:
            print("pyautogui is not installed. Mouse movement not available.")
            return False
        except Exception as e:
            print(f"Mouse move failed: {e}")
            return False

    def click(self, x: Optional[int] = None, y: Optional[int] = None, button: str = 'left') -> bool:
        """
        Click the mouse at the specified (x, y) coordinates, or current position if not specified.
        Args:
            x (int, optional): X coordinate
            y (int, optional): Y coordinate
            button (str): Mouse button ('left', 'right', 'middle')
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            import pyautogui
            if x is not None and y is not None:
                pyautogui.click(x, y, button=button)
            else:
                pyautogui.click(button=button)
            return True
        except ImportError:
            print("pyautogui is not installed. Mouse click not available.")
            return False
        except Exception as e:
            print(f"Mouse click failed: {e}")
            return False

# Usage Example:
# tool = MouseControlTool()
# tool.move(100, 200)
# tool.click(100, 200, button='left')
