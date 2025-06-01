"""
Test workflow for TTS and STT functionality.

This module provides a comprehensive test workflow for testing TTS and STT functionality
in both English and Arabic, following the workflow architecture rules.

---
description: Test TTS and STT workflow
endpoints: [test_tts_stt_workflow]
inputs: [language]
outputs: [test_results]
dependencies: [pytest, pyttsx3, whisper, sounddevice]
auth: none
alwaysApply: false
---
"""

import os
import sys
import pytest
import logging
import json
from datetime import datetime
from typing import Dict, Any, List

# Add src to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from labeeb.tools.tts_tool import TTSTool
from labeeb.tools.stt_tool import STTTool
from labeeb.utils.platform_utils import ensure_labeeb_directories

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/tts_stt_test.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TTSSTTWorkflow:
    """Workflow for testing TTS and STT functionality."""
    
    def __init__(self):
        """Initialize the workflow."""
        self.tts = TTSTool()
        self.stt = STTTool()
        self.base_dir = ensure_labeeb_directories()
        
        # Test texts
        self.test_texts = {
            "en": [
                "Hello, this is a test of the text to speech system.",
                "The weather is sunny today.",
                "Please confirm your identity."
            ],
            "ar": [
                "مرحبا، هذا اختبار لنظام تحويل النص إلى كلام",
                "الطقس مشمس اليوم",
                "يرجى تأكيد هويتك"
            ]
        }
        
    def test_tts(self, text: str, language: str) -> Dict[str, Any]:
        """
        Test TTS functionality.
        
        Args:
            text: Text to convert to speech
            language: Language code ("en" or "ar")
            
        Returns:
            Dict containing test results
        """
        try:
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(
                self.base_dir,
                "output",
                "audio",
                f"tts_test_{language}_{timestamp}.wav"
            )
            
            # Convert text to speech
            result = self.tts.save_to_file(text, output_file, language=language)
            
            return {
                "success": True,
                "output_file": output_file,
                "text": text,
                "language": language
            }
            
        except Exception as e:
            error_msg = f"Error in TTS test: {e}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
            
    def test_stt(self, audio_file: str, language: str) -> Dict[str, Any]:
        """
        Test STT functionality.
        
        Args:
            audio_file: Path to audio file
            language: Language code ("en" or "ar")
            
        Returns:
            Dict containing test results
        """
        try:
            # Transcribe audio
            result = self.stt.transcribe(audio_file, language=language)
            
            return {
                "success": True,
                "text": result["text"],
                "language": language
            }
            
        except Exception as e:
            error_msg = f"Error in STT test: {e}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
            
    def run_workflow(self) -> Dict[str, Any]:
        """
        Run the complete TTS-STT workflow test.
        
        Returns:
            Dict containing test results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "tests": []
        }
        
        # Test each language
        for language in ["en", "ar"]:
            logger.info(f"Testing {language} workflow")
            
            # Test each text
            for text in self.test_texts[language]:
                # Step 1: TTS
                tts_result = self.test_tts(text, language)
                if not tts_result["success"]:
                    results["tests"].append({
                        "language": language,
                        "text": text,
                        "tts_result": tts_result,
                        "stt_result": None
                    })
                    continue
                    
                # Step 2: STT
                stt_result = self.test_stt(tts_result["output_file"], language)
                
                # Step 3: Compare results
                comparison = {
                    "original_text": text,
                    "transcribed_text": stt_result.get("text", ""),
                    "match": text.lower() == stt_result.get("text", "").lower()
                }
                
                # Add to results
                results["tests"].append({
                    "language": language,
                    "text": text,
                    "tts_result": tts_result,
                    "stt_result": stt_result,
                    "comparison": comparison
                })
                
        # Save results
        results_file = os.path.join(
            self.base_dir,
            "tests",
            "results",
            f"tts_stt_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
            
        return results

def test_tts_stt_workflow():
    """Run the TTS-STT workflow test."""
    workflow = TTSSTTWorkflow()
    results = workflow.run_workflow()
    
    # Print summary
    print("\n=== TTS-STT Workflow Test Results ===")
    
    for test in results["tests"]:
        print(f"\nLanguage: {test['language']}")
        print(f"Original text: {test['text']}")
        if test["stt_result"]:
            print(f"Transcribed text: {test['stt_result']['text']}")
            print(f"Match: {test['comparison']['match']}")
        else:
            print("STT failed")
            
    # Save results
    print(f"\nDetailed results saved to: {results_file}")
    
    # Assert all tests passed
    assert all(test["tts_result"]["success"] for test in results["tests"]), "Some TTS tests failed"
    assert all(test["stt_result"]["success"] for test in results["tests"]), "Some STT tests failed"
    assert all(test["comparison"]["match"] for test in results["tests"]), "Some text comparisons failed"

if __name__ == "__main__":
    test_tts_stt_workflow() 