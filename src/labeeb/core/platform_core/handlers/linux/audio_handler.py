"""
Linux audio handler for Labeeb.

Provides platform-specific audio handling for Linux, including input device detection.

---
description: Linux audio handler
inputs: [action]
outputs: [status, error]
dependencies: [sounddevice, pyaudio]
alwaysApply: false
---
"""

from typing import Dict, Any, Optional
from labeeb.core.platform_core.handlers.base_handler import BaseHandler

class LinuxAudioHandler(BaseHandler):
    """Linux-specific audio handler implementation."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        return True

    def get_status(self) -> Dict[str, Any]:
        try:
            if not self._initialized:
                return {"error": "Handler not initialized"}
            input_available = False
            try:
                import sounddevice as sd
                input_available = any(dev['max_input_channels'] > 0 for dev in sd.query_devices())
            except ImportError:
                try:
                    import pyaudio
                    pa = pyaudio.PyAudio()
                    input_available = any(pa.get_device_info_by_index(i)['maxInputChannels'] > 0 for i in range(pa.get_device_count()))
                    pa.terminate()
                except ImportError:
                    input_available = True  # Fallback: assume available if cannot check
                except Exception:
                    input_available = False
            except Exception:
                input_available = False
            return {"input_available": input_available, "output_available": True, "error": None}
        except Exception as e:
            return {"error": str(e)} 