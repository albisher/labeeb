"""
Sound tool module for Labeeb.

This module provides functionality to play sound files.
It uses the pygame library for cross-platform sound support.

---
description: Play sound files
endpoints: [play_sound]
inputs: [filename]
outputs: [success]
dependencies: [pygame]
auth: none
alwaysApply: false
---
"""

import os
import logging
import pygame
from typing import Optional
from labeeb.core.config_manager import ConfigManager

logger = logging.getLogger(__name__)

class SoundTool:
    """Tool for playing sound files."""
    
    def __init__(self):
        """Initialize the sound tool."""
        self.config = ConfigManager()
        pygame.mixer.init()
        
    def play_sound(self, filename: str) -> bool:
        """
        Play a sound file.
        
        Args:
            filename: Path to the sound file
            
        Returns:
            True if playback was successful
            
        Raises:
            FileNotFoundError: If the sound file doesn't exist
            Exception: If playback fails
        """
        try:
            # Check if file exists
            if not os.path.exists(filename):
                raise FileNotFoundError(f"Sound file not found: {filename}")
                
            # Load and play sound
            sound = pygame.mixer.Sound(filename)
            sound.play()
            
            # Wait for sound to finish
            pygame.time.wait(int(sound.get_length() * 1000))
            
            return True
            
        except Exception as e:
            logger.error(f"Error playing sound: {e}")
            raise 