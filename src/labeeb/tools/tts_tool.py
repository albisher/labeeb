"""
Text-to-speech tool for converting text to speech.

This module provides functionality to convert text to speech using a workflow approach.
It uses pyttsx3 for text-to-speech conversion.

---
description: Convert text to speech
endpoints: [speak, save_to_file]
inputs: [text, language]
outputs: [audio_file]
dependencies: [pyttsx3]
auth: none
alwaysApply: false
---
"""

import os
import logging
import pyttsx3
from typing import Dict, Any, Optional
from labeeb.core.config_manager import ConfigManager
import tempfile
import platform

logger = logging.getLogger(__name__)

class TTSTool:
    """Tool for converting text to speech."""
    
    def __init__(self):
        """Initialize the TTS tool."""
        self.config = ConfigManager()
        self.engine = pyttsx3.init()
        
        # Set up voices
        voices = self.engine.getProperty('voices')
        self.voices = {
            'en': next((v for v in voices if 'en' in v.id.lower()), voices[0]),
            'ar': next((v for v in voices if 'ar' in v.id.lower()), voices[0])
        }
        
        # Set default properties
        self.engine.setProperty('rate', 150)    # Speed of speech
        self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        
    def speak(self, text: str, language: str = "en") -> None:
        """
        Convert text to speech and play it.
        
        Args:
            text: The text to convert to speech.
            language: The language of the text ('en' or 'ar').
            
        Raises:
            Exception: If text cannot be converted to speech.
        """
        try:
            # Set the voice based on language
            voice = self.voices.get(language, self.voices['en'])
            self.engine.setProperty('voice', voice.id)
            
            # For Arabic text, ensure proper text direction
            if language == 'ar':
                # Add RTL mark and ensure proper text direction
                text = f"\u202E{text}\u202C"
            
            # Speak the text
            self.engine.say(text)
            self.engine.runAndWait()
            
        except Exception as e:
            error_msg = f"Error converting text to speech: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
    def save_to_file(self, text: str, output_file: str, language: str = "en") -> Dict[str, Any]:
        """
        Convert text to speech and save to a file.
        
        Args:
            text: The text to convert to speech.
            output_file: The path to save the audio file.
            language: The language of the text ('en' or 'ar').
            
        Returns:
            Dict containing the output file path.
            
        Raises:
            Exception: If text cannot be converted to speech.
        """
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Set the voice based on language
            voice = self.voices.get(language, self.voices['en'])
            self.engine.setProperty('voice', voice.id)
            
            # For Arabic text, ensure proper text direction
            if language == 'ar':
                # Add RTL mark and ensure proper text direction
                text = f"\u202E{text}\u202C"
            
            # Save to file
            self.engine.save_to_file(text, output_file)
            self.engine.runAndWait()
            
            return {
                "output_file": output_file,
                "language": language
            }
            
        except Exception as e:
            error_msg = f"Error saving text to speech file: {e}"
            logger.error(error_msg)
            raise Exception(error_msg) 