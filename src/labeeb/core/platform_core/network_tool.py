"""
Network Tool for Labeeb

Provides atomic network status and interface information in a platform-agnostic way.

---
description: Atomic network status and interface info tool
inputs: [action]
outputs: [status, interfaces, error]
dependencies: [psutil]
alwaysApply: false
---
"""

from typing import Dict, Any

class NetworkTool:
    """Tool for querying network status and interfaces."""

    def get_status(self) -> Dict[str, Any]:
        """
        Get network status and interface information.
        Returns:
            dict: {"status": str, "interfaces": list, "error": str}
        """
        try:
            import psutil
            interfaces = psutil.net_if_addrs()
            status = "connected" if interfaces else "disconnected"
            return {"status": status, "interfaces": list(interfaces.keys()), "error": None}
        except ImportError:
            return {"status": "unknown", "interfaces": [], "error": "psutil not installed"}
        except Exception as e:
            return {"status": "error", "interfaces": [], "error": str(e)}

# Usage Example:
# tool = NetworkTool()
# print(tool.get_status())
