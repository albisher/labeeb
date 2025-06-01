"""
Speech-to-text tool for converting speech to text.

This module provides functionality to convert speech to text using a workflow approach.
It uses Whisper for speech recognition.

---
description: Convert speech to text
endpoints: [transcribe, record_from_microphone]
inputs: [audio_file, language]
outputs: [text]
dependencies: [whisper, sounddevice, numpy]
auth: none
alwaysApply: false
---
"""

import os
import logging
import whisper
import sounddevice as sd
import numpy as np
from typing import Dict, Any, Optional
from labeeb.core.config_manager import ConfigManager
import tempfile
import wave

logger = logging.getLogger(__name__)

class STTTool:
    """Tool for converting speech to text."""
    
    def __init__(self):
        """Initialize the STT tool."""
        self.config = ConfigManager()
        self.model = whisper.load_model("base")
        
    def transcribe(self, audio_file: str, language: str = "en") -> Dict[str, Any]:
        """
        Convert speech to text from an audio file.
        
        Args:
            audio_file: Path to the audio file.
            language: Language code ("en" for English, "ar" for Arabic).
            
        Returns:
            Dict containing the transcribed text.
            
        Raises:
            Exception: If transcription fails.
        """
        try:
            # Transcribe audio
            result = self.model.transcribe(
                audio_file,
                language=language,
                task="transcribe"
            )
            
            return {
                "text": result["text"],
                "language": language
            }
            
        except Exception as e:
            error_msg = f"Error transcribing audio: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
    def record_from_microphone(self, language: str = "en", duration: int = 5) -> Dict[str, Any]:
        """
        Record audio from microphone and convert to text.
        
        Args:
            language: Language code ("en" for English, "ar" for Arabic).
            duration: Recording duration in seconds.
            
        Returns:
            Dict containing the transcribed text.
            
        Raises:
            Exception: If recording or transcription fails.
        """
        try:
            # Set up recording parameters
            sample_rate = 16000
            channels = 1
            
            print(f"Recording for {duration} seconds...")
            
            # Record audio
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=channels,
                dtype='float32'
            )
            sd.wait()
            
            # Convert to 16-bit PCM
            recording = (recording * 32767).astype(np.int16)
            
            # Save to temporary WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                with wave.open(temp_file.name, 'wb') as wf:
                    wf.setnchannels(channels)
                    wf.setsampwidth(2)  # 2 bytes for int16
                    wf.setframerate(sample_rate)
                    wf.writeframes(recording.tobytes())
                
                # Transcribe the temporary file
                result = self.transcribe(temp_file.name, language)
                
                # Clean up
                os.unlink(temp_file.name)
                
                return result
            
        except Exception as e:
            error_msg = f"Error recording from microphone: {e}"
            logger.error(error_msg)
            raise Exception(error_msg) 