#!/usr/bin/env python3
"""
Test script for Labeeb commands.

This script tests all commands from commands.txt to ensure they work correctly.
It uses the ConfigManager to handle configuration and model selection.
"""

import os
import sys
import json
import logging
import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from labeeb.core.config_manager import ConfigManager
from labeeb.tools.screenshot_tool import ScreenshotTool
from labeeb.tools.weather_tool import WeatherTool
from labeeb.tools.calculator_tool import CalculatorTool
from labeeb.tools.web_search_tool import WebSearchTool
from labeeb.tools.clipboard_tool import ClipboardTool
from labeeb.tools.sound_tool import SoundTool
from labeeb.tools.stt_tool import STTTool
from labeeb.tools.tts_tool import TTSTool
from labeeb.tools.screen_reader_tool import ScreenReaderTool
from labeeb.tools.automation_tool import AutomationTool
from labeeb.utils.platform_utils import ensure_labeeb_directories

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/test_commands.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_ollama_model() -> bool:
    """Set up the Ollama model non-interactively."""
    try:
        import requests
        from labeeb.core.config_manager import ConfigManager
        
        config = ConfigManager()
        base_url = config.get("ollama_base_url")
        
        # Check if server is running
        try:
            response = requests.get(f"{base_url}/api/tags")
            if response.status_code != 200:
                logger.error("Ollama server is not running")
                return False
        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to Ollama server")
            return False
            
        # Get available models
        models = response.json().get("models", [])
        if not models:
            logger.error("No models available")
            return False
            
        # Use the first available model
        model = models[0]["name"]
        logger.info(f"Using model: {model}")
        
        # Update config
        config.set("default_ollama_model", model)
        config.save()
        
        return True
        
    except Exception as e:
        logger.error(f"Error setting up Ollama model: {e}")
        return False

def setup_weather_api() -> bool:
    """Set up the OpenWeatherMap API key."""
    try:
        config = ConfigManager()
        api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
        
        if not api_key:
            logger.warning("OPENWEATHERMAP_API_KEY environment variable not set")
            return False
            
        config.set("openweathermap_api_key", api_key)
        config.save()
        return True
        
    except Exception as e:
        logger.error(f"Error setting up weather API: {e}")
        return False

def test_screenshot() -> Dict[str, Any]:
    """Test screenshot functionality."""
    try:
        tool = ScreenshotTool()
        result = tool.take_screenshot()
        return {
            "success": True,
            "result": result,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "result": None,
            "error": str(e)
        }

def test_weather() -> Dict[str, Any]:
    """Test weather command."""
    try:
        print("\n=== Testing Weather Tool ===")
        tool = WeatherTool()
        
        # Test English location
        print("\nTesting English location (Riyadh)...")
        result_en = tool.get_weather("Riyadh")
        print(f"English weather result: {result_en}")
        
        # Test Arabic location
        print("\nTesting Arabic location (الكويت)...")
        result_ar = tool.get_weather("الكويت")
        print(f"Arabic weather result: {result_ar}")
        
        # Speak the results
        tts = TTSTool()
        tts.speak(f"The weather in Riyadh is {result_en['temperature']} degrees with {result_en['conditions']}")
        tts.speak(f"الطقس في الكويت {result_ar['temperature']} درجة مع {result_ar['conditions']}", language="ar")
        
        return {
            "success": True,
            "result": {
                "english": result_en,
                "arabic": result_ar
            },
            "error": None
        }
    except Exception as e:
        print(f"\nError in weather test: {e}")
        return {
            "success": False,
            "result": None,
            "error": str(e)
        }

def test_arithmetic() -> Dict[str, Any]:
    """Test arithmetic operations."""
    try:
        tool = CalculatorTool()
        result = tool.calculate("2 + 2")
        return {
            "success": True,
            "result": result,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "result": None,
            "error": str(e)
        }

def test_web_search() -> Dict[str, Any]:
    """Test web search functionality."""
    try:
        print("\n=== Testing Web Search Tool ===")
        tool = WebSearchTool()
        tts = TTSTool()
        
        print("\nSearching for 'Python programming'...")
        result = tool.search("Python programming")
        print(f"Search results: {result}")
        
        # Speak the first result
        if result:
            first_result = result[0]
            tts.speak(f"First result: {first_result['title']}. {first_result['snippet']}")
        
        return {
            "success": True,
            "result": result,
            "error": None
        }
    except Exception as e:
        print(f"\nError in web search test: {e}")
        return {
            "success": False,
            "result": None,
            "error": str(e)
        }

def test_clipboard() -> Dict[str, Any]:
    """Test clipboard operations."""
    try:
        tool = ClipboardTool()
        test_text = "Test clipboard content"
        tool.copy(test_text)
        result = tool.paste()
        return {
            "success": result == test_text,
            "result": result,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "result": None,
            "error": str(e)
        }

def test_sound() -> Dict[str, Any]:
    """Test sound playback."""
    try:
        tool = SoundTool()
        result = tool.play_sound("test.wav")
        return {
            "success": True,
            "result": result,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "result": None,
            "error": str(e)
        }

def test_calculator() -> Dict[str, Any]:
    """Test calculator functionality."""
    try:
        print("\n=== Testing Calculator Tool ===")
        tool = CalculatorTool()
        tts = TTSTool()
        
        print("\nCalculating '2 * 3'...")
        result = tool.calculate("2 * 3")
        print(f"Calculation result: {result}")
        tts.speak(f"The result is {result}")
        
        return {
            "success": True,
            "result": result,
            "error": None
        }
    except Exception as e:
        print(f"\nError in calculator test: {e}")
        return {
            "success": False,
            "result": None,
            "error": str(e)
        }

def test_arabic_commands() -> Dict[str, Any]:
    """Test commands in Arabic."""
    try:
        # Test weather in Arabic
        tool = WeatherTool()
        if not os.environ.get("OPENWEATHERMAP_API_KEY"):
            return {
                "success": False,
                "result": None,
                "error": "OpenWeatherMap API key not set"
            }
        result = tool.get_weather("الرياض")
        return {
            "success": True,
            "result": result,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "result": None,
            "error": str(e)
        }

def test_stt() -> Dict[str, Any]:
    """Test speech-to-text functionality."""
    try:
        print("\n=== Testing Speech-to-Text Tool ===")
        tool = STTTool()
        tts = TTSTool()
        
        # Test English audio
        print("\nTesting English audio transcription...")
        result_en = tool.transcribe("output/audio/test_en.wav", language="en")
        print(f"English transcription result: {result_en['text']}")
        tts.speak(f"The transcribed text is: {result_en['text']}")
        
        # Test Arabic audio
        print("\nTesting Arabic audio transcription...")
        result_ar = tool.transcribe("output/audio/test_ar.wav", language="ar")
        print(f"Arabic transcription result: {result_ar['text']}")
        tts.speak(f"النص المكتوب هو: {result_ar['text']}", language="ar")
        
        return {
            "success": True,
            "result": {
                "english": result_en,
                "arabic": result_ar
            },
            "error": None
        }
    except Exception as e:
        print(f"\nError in STT test: {e}")
        return {
            "success": False,
            "result": None,
            "error": str(e)
        }

def test_tts() -> Dict[str, Any]:
    """Test text-to-speech functionality."""
    try:
        print("\n=== Testing Text-to-Speech Tool ===")
        tool = TTSTool()
        
        # Test English text
        print("\nTesting English text-to-speech...")
        result_en = tool.save_to_file("Hello, this is a test", "test_en.wav", language="en")
        print(f"English TTS result: {result_en}")
        tool.speak("Hello, this is a test")
        
        # Test Arabic text
        print("\nTesting Arabic text-to-speech...")
        result_ar = tool.save_to_file("مرحبا، هذا اختبار", "test_ar.wav", language="ar")
        print(f"Arabic TTS result: {result_ar}")
        tool.speak("مرحبا، هذا اختبار", language="ar")
        
        return {
            "success": True,
            "result": {
                "english": result_en,
                "arabic": result_ar
            },
            "error": None
        }
    except Exception as e:
        print(f"\nError in TTS test: {e}")
        return {
            "success": False,
            "result": None,
            "error": str(e)
        }

def test_screen_reader() -> Dict[str, Any]:
    """Test screen reading functionality."""
    try:
        tool = ScreenReaderTool()
        result = tool.read_screenshot("test_screenshot.png")
        return {
            "success": True,
            "result": result,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "result": None,
            "error": str(e)
        }

def test_automation() -> Dict[str, Any]:
    """Test automation functionality."""
    try:
        tool = AutomationTool()
        
        # Test window info
        windows = tool.get_window_info()
        
        # Test mouse movement
        tool.move_mouse(100, 100)
        
        # Test clicking
        tool.click()
        
        return {
            "success": True,
            "result": {
                "windows": windows,
                "mouse_moved": True,
                "clicked": True
            },
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "result": None,
            "error": str(e)
        }

def test_complex_workflow() -> Dict[str, Any]:
    """Test complex workflow functionality."""
    try:
        # Initialize tools
        automation = AutomationTool()
        screenshot = ScreenshotTool()
        screen_reader = ScreenReaderTool()
        tts = TTSTool()
        
        # 1. Open TextEdit
        automation.open_application("textedit")
        
        # 2. Type text
        automation.type_text("This is a test document")
        
        # 3. Save file
        automation.save_file("workflow_test.txt", os.path.expanduser("~/Documents"))
        
        # 4. Take screenshot
        screenshot_path = screenshot.take_screenshot()
        
        # 5. Read text from screenshot
        text = screen_reader.read_screenshot(screenshot_path)
        
        # 6. Convert to speech
        tts.save_to_file(text["text"], "workflow_audio.wav")
        
        return {
            "success": True,
            "result": {
                "screenshot_path": screenshot_path,
                "extracted_text": text,
                "audio_file": "workflow_audio.wav"
            },
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "result": None,
            "error": str(e)
        }

def main():
    """Run all tests and save results."""
    # Ensure directories exist
    base_dir = ensure_labeeb_directories()
    if not base_dir:
        logger.error("Failed to create required directories")
        sys.exit(1)
        
    # Set up Ollama model
    if not setup_ollama_model():
        logger.error("Failed to set up Ollama model")
        sys.exit(1)
        
    print("\n=== Starting Labeeb Command Tests ===")
    
    # Run all tests
    tests = [
        ("weather", test_weather),
        ("calculator", test_calculator),
        ("web_search", test_web_search),
        ("stt", test_stt),
        ("tts", test_tts),
        ("screenshot", test_screenshot),
        ("clipboard", test_clipboard),
        ("sound", test_sound),
        ("screen_reader", test_screen_reader),
        ("automation", test_automation),
        ("complex_workflow", test_complex_workflow)
    ]
    
    results = {}
    for name, test_func in tests:
        print(f"\nRunning test: {name}")
        results[name] = test_func()
        print(f"Test {name} completed with success: {results[name]['success']}")
        
    # Save results
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(base_dir, "logs", f"test_results_{timestamp}.json")
    
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        
    print(f"\nTest results saved to: {results_file}")
    
    # Print summary
    success_count = sum(1 for r in results.values() if r["success"])
    print(f"\n=== Test Summary ===")
    print(f"Total tests: {len(tests)}")
    print(f"Successful tests: {success_count}")
    print(f"Failed tests: {len(tests) - success_count}")
    
    # Print failed tests
    if success_count < len(tests):
        print("\nFailed tests:")
        for name, result in results.items():
            if not result["success"]:
                print(f"- {name}: {result['error']}")

if __name__ == "__main__":
    main() 