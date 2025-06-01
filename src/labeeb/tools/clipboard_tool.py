"""
Clipboard tool module for Labeeb.

This module provides functionality to interact with the system clipboard.
It uses the pyperclip library for cross-platform clipboard support.

---
description: Interact with system clipboard
endpoints: [copy, paste]
inputs: [text]
outputs: [text]
dependencies: [pyperclip]
auth: none
alwaysApply: false
---
"""

import logging
import pyperclip
from typing import Optional

logger = logging.getLogger(__name__)

class ClipboardTool:
    """Tool for clipboard operations."""
    
    def __init__(self):
        """Initialize the clipboard tool."""
        # Test clipboard access
        try:
            pyperclip.copy("")
            pyperclip.paste()
        except Exception as e:
            logger.error(f"Error initializing clipboard: {e}")
            raise
            
    def copy(self, text: str) -> None:
        """
        Copy text to clipboard.
        
        Args:
            text: The text to copy
            
        Raises:
            Exception: If copying fails
        """
        try:
            pyperclip.copy(text)
        except Exception as e:
            logger.error(f"Error copying to clipboard: {e}")
            raise
            
    def paste(self) -> str:
        """
        Get text from clipboard.
        
        Returns:
            The text from clipboard
            
        Raises:
            Exception: If pasting fails
        """
        try:
            return pyperclip.paste()
        except Exception as e:
            logger.error(f"Error pasting from clipboard: {e}")
            raise 