"""
Command-line interface for Labeeb.

This module provides a command-line interface to run individual tests and commands.
"""

import os
import sys
import argparse
import logging
from typing import Dict, Any, List, Optional

# Add src to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from labeeb.tools.weather_tool import WeatherTool
from labeeb.tools.calculator_tool import CalculatorTool
from labeeb.tools.web_search_tool import WebSearchTool
from labeeb.tools.stt_tool import STTTool
from labeeb.tools.tts_tool import TTSTool
from labeeb.tools.screenshot_tool import ScreenshotTool
from labeeb.tools.clipboard_tool import ClipboardTool
from labeeb.tools.sound_tool import SoundTool
from labeeb.tools.screen_reader_tool import ScreenReaderTool
from labeeb.tools.automation_tool import AutomationTool
from labeeb.utils.platform_utils import ensure_labeeb_directories

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/labeeb.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_weather(location: str, language: str = "en", show_browser: bool = True) -> None:
    """Run weather command."""
    try:
        print(f"\n=== Getting Weather for {location} ===")
        tool = WeatherTool()
        
        # Get weather info
        result = tool.get_weather(location)
        print(f"Weather result: {result}")
        
        # Show in browser if requested
        if show_browser:
            tool.show_in_browser(location)
        
        # Speak the result
        tts = TTSTool()
        if language == "ar":
            tts.speak(f"الطقس في {location} {result['temperature']} درجة مع {result['conditions']}", language="ar")
        else:
            tts.speak(f"The weather in {location} is {result['temperature']} degrees with {result['conditions']}")
            
    except Exception as e:
        print(f"Error: {e}")

def run_calculator(expression: str, show_gui: bool = True) -> None:
    """Run calculator command."""
    try:
        print(f"\n=== Calculating: {expression} ===")
        tool = CalculatorTool()
        
        # Calculate result
        result = tool.calculate(expression)
        print(f"Result: {result}")
        
        # Show GUI if requested
        if show_gui:
            tool.show_calculator()
            tool.type_expression(expression)
            tool.press_equals()
        
        # Speak the result
        tts = TTSTool()
        tts.speak(f"The result is {result}")
        
    except Exception as e:
        print(f"Error: {e}")

def run_web_search(query: str) -> None:
    """Run web search command."""
    try:
        print(f"\n=== Searching for: {query} ===")
        tool = WebSearchTool()
        results = tool.search(query)
        print(f"Search results: {results}")
        
        # Speak the first result
        if results:
            tts = TTSTool()
            first_result = results[0]
            tts.speak(f"First result: {first_result['title']}. {first_result['snippet']}")
            
    except Exception as e:
        print(f"Error: {e}")

def run_stt(file_path: str = None, language: str = "en", use_mic: bool = False) -> None:
    """Run speech-to-text command."""
    try:
        print(f"\n=== Transcribing Audio ===")
        tool = STTTool()
        
        if use_mic:
            print("Recording from microphone... (Press Ctrl+C to stop)")
            result = tool.record_from_microphone(language=language)
        else:
            print(f"Transcribing file: {file_path}")
            result = tool.transcribe(file_path, language=language)
            
        print(f"Transcription: {result['text']}")
        
        # Speak the result
        tts = TTSTool()
        if language == "ar":
            tts.speak(f"النص المكتوب هو: {result['text']}", language="ar")
        else:
            tts.speak(f"The transcribed text is: {result['text']}")
            
    except Exception as e:
        print(f"Error: {e}")

def run_tts(text: str, output_file: str, language: str = "en") -> None:
    """Run text-to-speech command."""
    try:
        print(f"\n=== Converting to speech: {text} ===")
        tool = TTSTool()
        
        # First save to file
        result = tool.save_to_file(text, output_file, language=language)
        print(f"Saved to: {output_file}")
        
        # Then speak it
        print(f"Speaking in {language}...")
        tool.speak(text, language=language)
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Labeeb Command Line Interface")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Weather command
    weather_parser = subparsers.add_parser("weather", help="Get weather information")
    weather_parser.add_argument("location", help="Location to get weather for")
    weather_parser.add_argument("--language", choices=["en", "ar"], default="en", help="Language for output")
    weather_parser.add_argument("--no-browser", action="store_true", help="Don't show browser")
    
    # Calculator command
    calc_parser = subparsers.add_parser("calc", help="Run calculator")
    calc_parser.add_argument("expression", help="Expression to calculate")
    calc_parser.add_argument("--no-gui", action="store_true", help="Don't show calculator GUI")
    
    # Web search command
    search_parser = subparsers.add_parser("search", help="Search the web")
    search_parser.add_argument("query", help="Search query")
    
    # STT command
    stt_parser = subparsers.add_parser("stt", help="Convert speech to text")
    stt_parser.add_argument("--file", help="Audio file to transcribe")
    stt_parser.add_argument("--language", choices=["en", "ar"], default="en", help="Language of the audio")
    stt_parser.add_argument("--mic", action="store_true", help="Use microphone input")
    
    # TTS command
    tts_parser = subparsers.add_parser("tts", help="Convert text to speech")
    tts_parser.add_argument("text", help="Text to convert")
    tts_parser.add_argument("output", help="Output file path")
    tts_parser.add_argument("--language", choices=["en", "ar"], default="en", help="Language of the text")
    
    args = parser.parse_args()
    
    # Ensure directories exist
    ensure_labeeb_directories()
    
    if args.command == "weather":
        run_weather(args.location, args.language, not args.no_browser)
    elif args.command == "calc":
        run_calculator(args.expression, not args.no_gui)
    elif args.command == "search":
        run_web_search(args.query)
    elif args.command == "stt":
        if not args.file and not args.mic:
            stt_parser.error("Either --file or --mic must be specified")
        run_stt(args.file, args.language, args.mic)
    elif args.command == "tts":
        run_tts(args.text, args.output, args.language)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 