"""
Screen Reader tool for extracting text from images.

This module provides functionality to read text from screenshots using Tesseract OCR.

---
description: Extract text from screenshots
endpoints: [read_screenshot]
inputs: [image_path]
outputs: [text, confidence]
dependencies: [pytesseract, pillow]
auth: none
alwaysApply: false
---
"""

import os
import logging
import pytesseract
from PIL import Image
from pathlib import Path

logger = logging.getLogger(__name__)

class ScreenReaderTool:
    """Tool for reading text from screenshots."""
    
    def __init__(self):
        """Initialize the screen reader tool."""
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "output", "screenshots")
        os.makedirs(self.output_dir, exist_ok=True)
        
    def read_screenshot(self, image_path: str) -> dict:
        """
        Extract text from a screenshot.
        
        Args:
            image_path: Path to the screenshot image.
            
        Returns:
            dict: Dictionary containing the extracted text and confidence score.
            
        Raises:
            Exception: If text extraction fails.
        """
        try:
            # Ensure image path is absolute
            if not os.path.isabs(image_path):
                image_path = os.path.join(self.output_dir, image_path)
                
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
                
            # Open and process the image
            image = Image.open(image_path)
            
            # Extract text using Tesseract
            text = pytesseract.image_to_string(image)
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            # Calculate average confidence
            confidences = [int(conf) for conf in data['conf'] if conf != '-1']
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            result = {
                "text": text.strip(),
                "confidence": avg_confidence
            }
            
            logger.info(f"Successfully extracted text from {image_path}")
            return result
            
        except FileNotFoundError as e:
            logger.error(str(e))
            raise
        except Exception as e:
            error_msg = f"Error reading screenshot: {e}"
            logger.error(error_msg)
            raise Exception(error_msg) 