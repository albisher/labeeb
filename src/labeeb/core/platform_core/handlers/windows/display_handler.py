"""
Windows display handler for Labeeb.

Provides platform-specific display handling for Windows, including screen capture, display information, and RTL text detection.

---
description: Windows display handler
inputs: [action, display_id]
outputs: [image, displays, error]
dependencies: [PIL, pytesseract]
alwaysApply: false
---
"""

from typing import Dict, Any, Optional, List, Tuple
from labeeb.core.platform_core.handlers.base_handler import BaseHandler

class WindowsDisplayHandler(BaseHandler):
    """Handler for Windows display devices."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._display_enabled = False
        self._displays = []
        self._main_display = None
        self._text_direction = "ltr"

    def initialize(self) -> bool:
        try:
            self._display_enabled = True
            return True
        except Exception as e:
            print(f"Failed to initialize WindowsDisplayHandler: {e}")
            return False

    def capture_screen(self, display_id: Optional[int] = None) -> Optional[bytes]:
        try:
            from PIL import ImageGrab
            import io
            image = ImageGrab.grab()
            data = io.BytesIO()
            # RTL text detection
            try:
                import pytesseract
                import arabic_reshaper
                from bidi.algorithm import get_display
                text = pytesseract.image_to_string(image, lang='ara+eng')
                if any('\u0600' <= c <= '\u06FF' for c in text):
                    reshaped_text = arabic_reshaper.reshape(text)
                    display_text = get_display(reshaped_text)
                    # Optionally overlay reshaped text on image (not implemented)
            except ImportError:
                pass
            except Exception:
                pass
            image.save(data, "PNG")
            return data.getvalue()
        except Exception as e:
            print(f"Failed to capture screen: {e}")
            return None

    def get_displays(self) -> List[Dict[str, Any]]:
        return self._displays

    def get_main_display(self) -> Optional[Dict[str, Any]]:
        return self._main_display 