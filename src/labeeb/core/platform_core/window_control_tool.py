"""
Window Control Tool for Labeeb

Provides atomic window management operations in a platform-agnostic way.

---
description: Atomic window management tool
inputs: [action, window_title]
outputs: [success, windows, error]
dependencies: [pygetwindow, pyautogui]
alwaysApply: false
---
"""

from typing import List, Dict, Any, Optional

class WindowControlTool:
    """Tool for managing windows (list, focus) in a platform-agnostic way."""

    def list_windows(self) -> Dict[str, Any]:
        """
        List all open windows.
        Returns:
            dict: {"windows": list, "error": str}
        """
        try:
            import pygetwindow
            windows = [w.title for w in pygetwindow.getAllWindows()]
            return {"windows": windows, "error": None}
        except ImportError:
            return {"windows": [], "error": "pygetwindow not installed"}
        except Exception as e:
            return {"windows": [], "error": str(e)}

    def focus_window(self, window_title: str) -> Dict[str, Any]:
        """
        Focus a window by its title.
        Args:
            window_title (str): The title of the window to focus
        Returns:
            dict: {"success": bool, "error": str}
        """
        try:
            import pygetwindow
            win = next((w for w in pygetwindow.getAllWindows() if w.title == window_title), None)
            if win:
                win.activate()
                return {"success": True, "error": None}
            else:
                return {"success": False, "error": "Window not found"}
        except ImportError:
            return {"success": False, "error": "pygetwindow not installed"}
        except Exception as e:
            return {"success": False, "error": str(e)}

# Usage Example:
# tool = WindowControlTool()
# print(tool.list_windows())
# print(tool.focus_window("Untitled - Notepad"))
