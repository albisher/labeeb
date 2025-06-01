"""
Text-to-Speech tool for converting text to speech.

This module provides functionality to convert text to speech using system commands.
It supports both Arabic and English languages.

---
description: Convert text to speech
endpoints: [speak, save_to_file]
inputs: [text, filename, language]
outputs: [success]
dependencies: []
auth: none
alwaysApply: false
---
"""

import os
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from labeeb.core.config_manager import ConfigManager

logger = logging.getLogger(__name__)

class TTSTool:
    """Tool for text-to-speech conversion."""
    
    def __init__(self):
        """Initialize the TTS tool."""
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "output", "audio")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Available voices for each language
        self.voices = {
            "en": "Samantha",  # English voice
            "ar": "Tarik"      # Arabic voice
        }
            
    def speak(self, text: str, language: str = "en") -> bool:
        """
        Speak the given text.
        
        Args:
            text: The text to speak.
            language: Language code ("en" for English, "ar" for Arabic).
            
        Returns:
            bool: True if successful, False otherwise.
            
        Raises:
            Exception: If speaking fails.
        """
        try:
            voice = self.voices.get(language, self.voices["en"])
            cmd = ["say", "-v", voice, text]
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            error_msg = f"Error speaking text: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
    def save_to_file(self, text: str, filename: str, language: str = "en") -> bool:
        """
        Save the given text as speech to a file.
        
        Args:
            text: The text to convert to speech.
            filename: The name of the output file.
            language: Language code ("en" for English, "ar" for Arabic).
            
        Returns:
            bool: True if successful, False otherwise.
            
        Raises:
            Exception: If saving to file fails.
        """
        try:
            # Ensure filename is in the output directory
            if not os.path.isabs(filename):
                filename = os.path.join(self.output_dir, filename)
                
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            voice = self.voices.get(language, self.voices["en"])
            
            # First save to a temporary file
            temp_file = filename + ".aiff"
            cmd = ["say", "-v", voice, "-o", temp_file, text]
            subprocess.run(cmd, check=True)
            
            # Convert to WAV format
            cmd = ["afconvert", "-f", "WAVE", "-d", "LEI16@44100", temp_file, filename]
            subprocess.run(cmd, check=True)
            
            # Remove temporary file
            os.remove(temp_file)
            
            return True
        except Exception as e:
            error_msg = f"Error saving speech to file: {e}"
            logger.error(error_msg)
            raise Exception(error_msg) 