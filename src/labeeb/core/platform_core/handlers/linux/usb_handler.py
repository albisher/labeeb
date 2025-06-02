"""
Linux USB handler for Labeeb.

Provides platform-specific USB device detection for Linux.

---
description: Linux USB handler
inputs: [action]
outputs: [devices, error]
dependencies: [pyudev]
alwaysApply: false
---
"""

from typing import List, Dict, Any, Optional
from labeeb.core.platform_core.handlers.base_handler import BaseHandler

class LinuxUsbHandler(BaseHandler):
    """Handler for Linux USB device detection."""

    def list_devices(self) -> Dict[str, Any]:
        try:
            try:
                import pyudev
                context = pyudev.Context()
                devices = [
                    {
                        "device_node": device.device_node,
                        "sys_name": device.sys_name,
                        "sys_path": device.sys_path,
                        "id_vendor": device.get("ID_VENDOR"),
                        "id_model": device.get("ID_MODEL"),
                    }
                    for device in context.list_devices(subsystem="usb", DEVTYPE="usb_device")
                ]
                return {"devices": devices, "error": None}
            except ImportError:
                return {"devices": [], "error": "pyudev not installed"}
            except Exception as e:
                return {"devices": [], "error": str(e)}
        except Exception as e:
            return {"devices": [], "error": str(e)} 