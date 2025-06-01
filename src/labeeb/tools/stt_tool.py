"""
Speech-to-Text tool module for Labeeb.

This module provides functionality to convert speech to text using Whisper.
It uses the OpenAI Whisper model for accurate speech recognition in both Arabic and English.

---
description: Convert speech to text
endpoints: [transcribe]
inputs: [audio_file, language]
outputs: [text]
dependencies: [whisper]
auth: none
alwaysApply: false
---
"""

import os
import logging
import whisper
from typing import Dict, Any, Optional
from labeeb.core.config_manager import ConfigManager

logger = logging.getLogger(__name__)

class STTTool:
    """Tool for speech-to-text conversion."""
    
    def __init__(self):
        """Initialize the STT tool."""
        self.config = ConfigManager()
        self.models = {
            "en": "base.en",  # English model
            "ar": "base"      # Multilingual model for Arabic
        }
        self.loaded_models = {}
        
    def _load_model(self, language: str) -> whisper.Whisper:
        """Load the appropriate model for the given language."""
        if language not in self.models:
            raise ValueError(f"Unsupported language: {language}")
            
        if language not in self.loaded_models:
            try:
                model_name = self.models[language]
                self.loaded_models[language] = whisper.load_model(model_name)
            except Exception as e:
                logger.error(f"Error loading Whisper model for {language}: {e}")
                raise
                
        return self.loaded_models[language]
            
    def transcribe(self, audio_file: str, language: str = "en") -> Dict[str, Any]:
        """
        Transcribe speech from an audio file.
        
        Args:
            audio_file: Path to the audio file
            language: Language code ("en" for English, "ar" for Arabic)
            
        Returns:
            Dict containing transcription and metadata
            
        Raises:
            FileNotFoundError: If the audio file doesn't exist
            ValueError: If language is not supported
            Exception: If transcription fails
        """
        try:
            # Check if file exists
            if not os.path.exists(audio_file):
                raise FileNotFoundError(f"Audio file not found: {audio_file}")
                
            # Load appropriate model
            model = self._load_model(language)
            
            # Transcribe audio
            result = model.transcribe(
                audio_file,
                language=language,
                task="transcribe"
            )
            
            return {
                "text": result["text"],
                "segments": result["segments"],
                "language": result["language"]
            }
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            raise 