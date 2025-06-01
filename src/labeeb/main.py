#!/usr/bin/env python3
"""
Labeeb: AI-powered shell assistant.
Main entry point for the Labeeb application.
Supports both GUI and command-line interfaces with RTL and Arabic language support.

Copyright (c) 2025 Labeeb Team
License: Custom license - free for personal and educational use.
Commercial use requires a paid license. See LICENSE file for details.
"""
import os
import sys
import logging
import warnings
import urllib3
import argparse
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import asyncio
import arabic_reshaper
from bidi.algorithm import get_display
from labeeb.services.platform_services.common.platform_utils import get_platform_name

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from labeeb.core.logging_config import setup_logging, get_logger
from labeeb.core.exceptions import LabeebError, AIError, ConfigurationError, CommandError
from labeeb.core.cache_manager import CacheManager
from labeeb.core.platform_core.platform_manager import PlatformManager
from labeeb.core.command_processor.command_processor import CommandProcessor
from labeeb.core.shell_handler import ShellHandler
from labeeb.core.ai_handler import AIHandler
from labeeb.utils.output_facade import output
from labeeb.core.file_operations import process_file_flag_request
from labeeb.services.health_check.ollama_health_check import check_ollama_server, check_model_available
from labeeb.core.model_manager import ModelManager
from labeeb.core.config_manager import ConfigManager
from labeeb.core.ai.agent import LabeebAgent
from labeeb.core.ai.workflows.base_workflow import LabeebWorkflow
from labeeb.tools.base_tool import BaseAgentTool
from labeeb.utils.platform_utils import ensure_labeeb_directories

# Set up logging
logger = get_logger(__name__)

# Disable httpx INFO level logging to prevent duplicate request logs
logging.getLogger("httpx").setLevel(logging.WARNING)

# Suppress all urllib3 warnings
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=urllib3.exceptions.NotOpenSSLWarning)
urllib3.disable_warnings()


class Labeeb:
    """Main Labeeb class that handles user interaction."""

    SUPPORTED_LANGUAGES = {
        "ar": "العربية",
        "ar-SA": "العربية (السعودية)",
        "ar-KW": "العربية (الكويت)",
        "ar-MA": "العربية (المغرب)",
        "ar-EG": "العربية (مصر)",
        "en": "English",
    }

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        debug: bool = False,
        mode: str = "interactive",
        fast_mode: bool = False,
    ):
        """
        Initialize Labeeb with configuration.

        Args:
            config: Optional configuration dictionary
            debug: Boolean to enable debug output
            mode: The mode of operation (interactive, command, or file)
            fast_mode: Boolean to enable fast mode (minimal prompts, quick exit)
        """
        try:
            self.mode = mode
            self.fast_mode = fast_mode
            self.debug = debug

            # Initialize RTL and Arabic text support
            self.arabic_support = True
            self.rtl_support = True

            # Ensure Labeeb directories exist
            self.base_dir = ensure_labeeb_directories()
            if not self.base_dir:
                raise ConfigurationError("Failed to create Labeeb directories")

            # Initialize platform manager with mode awareness
            self.platform_manager = PlatformManager()
            platform_name = get_platform_name()
            if not self.platform_manager.is_platform_supported():
                raise ConfigurationError(f"Unsupported platform: {platform_name}")

            # Initialize platform components
            logger.info("Initializing platform components...")
            self.platform_manager.initialize()

            # Load configuration from file if not provided
            if config is None:
                config_path = os.path.join(self.base_dir, "config", "settings.json")
                if os.path.exists(config_path):
                    with open(config_path, "r", encoding="utf-8") as f:
                        self.config = json.load(f)
                else:
                    self.config = {}
            else:
                self.config = config

            # Configure output facade with verbosity settings and RTL support
            output_verbosity = self.config.get("output_verbosity", "normal")
            output.set_verbosity(output_verbosity)
            output.set_rtl_support(self.rtl_support)

            # Initialize shell handler and command processor
            self.shell_handler = ShellHandler(fast_mode=fast_mode)

            # Initialize AI handler with caching and Arabic support
            model_type = self.config.get("default_ai_provider", "ollama")
            ollama_base_url = self.config.get("ollama_base_url", "http://localhost:11434")

            # --- Automated Ollama model selection ---
            default_model = self.config.get("default_ollama_model", "gemma:2b")
            selected_model = default_model
            if model_type == "ollama":
                ok, tags_json = check_ollama_server()
                if ok:
                    ok, selected_model = check_model_available(tags_json, default_model)
                    if ok:
                        print(f"[Labeeb] Using Ollama model: {selected_model}")
                        # Update the config with the selected model
                        if self.update_config(selected_model):
                            self.config["default_ollama_model"] = selected_model
                        else:
                            print(
                                "[Labeeb] Warning: Failed to update configuration with selected model"
                            )
                    else:
                        print("[Labeeb] No available Ollama model found. Exiting.")
                        raise RuntimeError("No available Ollama model found.")
            else:
                selected_model = default_model

            # Initialize AIHandler with only supported arguments
            config_manager = ConfigManager()
            config_manager.set("default_ollama_model", selected_model)
            config_manager.set("ollama_base_url", ollama_base_url)
            config_manager.set("arabic_support", self.arabic_support)
            config_manager.set("rtl_support", self.rtl_support)

            self.ai_handler = AIHandler(model_manager=ModelManager(config_manager))

            # Patch the model name for Ollama if needed
            if model_type == "ollama":
                setattr(self.ai_handler, "ollama_model_name", selected_model)

            self.command_processor = CommandProcessor(self.ai_handler)

            # Set up language-specific welcome messages
            self.welcome_messages = {
                "ar": """
🤖 مرحباً بك في لبيب!
أنا مساعدك الذكي، جاهز لمساعدتك في مهامك.
يعمل على: {platform_info}
اكتب 'help' للحصول على الأوامر المتاحة أو اسألني أي شيء!
""",
                "en": """
🤖 Welcome to Labeeb!
I'm your intelligent assistant, ready to help you with your tasks.
Running on: {platform_info}
Type 'help' for available commands or ask me anything!
""",
            }

            # Get platform info
            platform_info = platform_utils.get_system_info()

            # Set default welcome message based on system locale
            default_lang = "ar" if self.rtl_support else "en"
            welcome_text = self.welcome_messages[default_lang].format(
                platform_info=platform_info["system"]
            )

            if self.rtl_support:
                welcome_text = get_display(arabic_reshaper.reshape(welcome_text))
            self.welcome_message = welcome_text

            logger.info("Labeeb initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Labeeb: {str(e)}")
            raise

    def _get_platform_specific_path(self) -> str:
        """Get platform-specific directory path."""
        system = get_platform_name().lower()
        if system == "darwin":
            return "macos"
        elif system == "windows":
            return "windows"
        elif system == "linux":
            return "linux"
        else:
            return "generic"

    def _handle_task(self, task: str) -> str:
        """Handle a single task with human-like variations in Arabic and English."""
        try:
            # Process task in both languages
            arabic_task = f"المهمة: {task}"
            english_task = f"Task: {task}"

            # Get platform-specific path
            platform_path = self._get_platform_specific_path()

            # Process task with platform awareness
            response = self.command_processor.process_command(task)

            # Format response based on language
            if self.rtl_support:
                return f"{arabic_task}\n{response}"
            else:
                return f"{english_task}\n{response}"

        except Exception as e:
            logger.error(f"Error processing task: {str(e)}")
            return f"Error processing task: {str(e)}"

    def _process_tasks_sequentially(self, tasks: List[str]) -> None:
        """Process a list of tasks one by one."""
        for task in tasks:
            try:
                response = self._handle_task(task)
                if not self.fast_mode:
                    output.info(response)
                else:
                    print(response)
            except Exception as e:
                logger.error(f"Error in task processing: {str(e)}")
                if not self.fast_mode:
                    output.error(f"Task failed: {str(e)}")
                else:
                    print(f"Error: {str(e)}")

    def start(self) -> None:
        """Start the Labeeb interactive session."""
        try:
            if not self.fast_mode:
                output.box(self.welcome_message, "Welcome")
            self._interactive_loop()
        except KeyboardInterrupt:
            if not self.fast_mode:
                output.info("👋 Session interrupted. Goodbye!")
        except Exception as e:
            logger.error(f"Error in interactive session: {str(e)}")
            if not self.fast_mode:
                output.error(f"An error occurred: {str(e)}")
            else:
                print(f"Error: {str(e)}")
        finally:
            self.cleanup()

    def _interactive_loop(self) -> None:
        """Main interactive loop for Labeeb."""
        model_switch_triggers = [
            "switch model",
            "change model",
            "set model",
            "use model",
            "change ai model",
            "set ai model",
            "switch ai model",
            "use ai model",
            "select model",
            "select ai model",
            "update model",
            "update ai model",
            # Arabic triggers
            "تغيير النموذج",
            "تحديث النموذج",
            "استخدام نموذج",
            "اختيار نموذج",
        ]
        while True:
            try:
                prompt = ">" if self.fast_mode else "\nأنت: " if self.rtl_support else "\nYou: "
                user_input = input(prompt).strip()
                if not user_input:
                    continue

                # Handle RTL input
                if self.rtl_support and any("\u0600" <= c <= "\u06ff" for c in user_input):
                    user_input = arabic_reshaper.reshape(user_input)
                    user_input = get_display(user_input)

                if user_input.lower() in ["exit", "quit", "bye", "x", "خروج", "وداعاً"]:
                    if not self.fast_mode:
                        output.success(
                            "👋 مع السلامة! أتمنى لك يوماً رائعاً!"
                            if self.rtl_support
                            else "👋 Goodbye! Have a great day!"
                        )
                    break

                if user_input.lower() in ["help", "مساعدة"]:
                    if not self.fast_mode:
                        self._show_help()
                    continue

                if user_input.lower() in ["clear", "مسح"]:
                    self.ai_handler.clear_cache()
                    if not self.fast_mode:
                        output.success(
                            "تم مسح الذاكرة المؤقتة بنجاح"
                            if self.rtl_support
                            else "Cache cleared successfully"
                        )
                    continue

                # Check for model switch triggers
                lowered = user_input.lower()
                if any(
                    lowered.startswith(trigger) or trigger in lowered
                    for trigger in model_switch_triggers
                ):
                    self.switch_model()
                    continue

                response = self.command_processor.process_command(user_input)

                # Handle RTL output
                if self.rtl_support and any("\u0600" <= c <= "\u06ff" for c in response):
                    response = arabic_reshaper.reshape(response)
                    response = get_display(response)

                if not self.fast_mode:
                    output.info(response)
                else:
                    print(response)

            except KeyboardInterrupt:
                if not self.fast_mode:
                    output.info(
                        "👋 تم مقاطعة الجلسة. مع السلامة!"
                        if self.rtl_support
                        else "👋 Session interrupted. Goodbye!"
                    )
                break
            except CommandError as e:
                if not self.fast_mode:
                    output.error(
                        f"خطأ في الأمر: {str(e)}"
                        if self.rtl_support
                        else f"Command error: {str(e)}"
                    )
                else:
                    print(f"Error: {str(e)}")
            except AIError as e:
                if not self.fast_mode:
                    output.error(
                        f"خطأ في معالجة الذكاء الاصطناعي: {str(e)}"
                        if self.rtl_support
                        else f"AI processing error: {str(e)}"
                    )
                else:
                    print(f"Error: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}", exc_info=True)
                if not self.fast_mode:
                    output.error(
                        f"حدث خطأ غير متوقع: {str(e)}"
                        if self.rtl_support
                        else f"An unexpected error occurred: {str(e)}"
                    )
                else:
                    print(f"Error: {str(e)}")

    def _show_help(self) -> None:
        """Show help information."""
        help_text = """
الأوامر المتاحة:
- help/مساعدة: عرض رسالة المساعدة هذه
- clear/مسح: مسح ذاكرة الذكاء الاصطناعي المؤقتة
- exit/quit/bye/خروج/وداعاً: الخروج من لبيب

يمكنك أيضاً:
- طلب تنفيذ أوامر النظام
- طرح أسئلة حول نظامك
- طلب عمليات الملفات
- الحصول على معلومات النظام
"""
        if self.rtl_support:
            help_text = get_display(arabic_reshaper.reshape(help_text))
        output.box(help_text, "المساعدة" if self.rtl_support else "Help")

    def process_single_command(self, command: str) -> str:
        """
        Process a single command and return the result.

        Args:
            command: The command to process

        Returns:
            The command response
        """
        try:
            result = self.command_processor.process_command(command)
            return result
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """Clean up resources."""
        try:
            self.platform_manager.cleanup()
            logger.info("Resources cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

    def process_test_requests(self, file_path: str) -> None:
        """
        Process test requests from a file.

        Args:
            file_path: Path to the file containing test requests
        """
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            requests = [
                line.strip() for line in lines if line.strip() and not line.strip().startswith("#")
            ]
            for request in requests:
                output.box(f"🤖 Processing your request: '{request}'", "Request")
                response = self.command_processor.process_command(request)
                output.info(response)
        except Exception as e:
            logger.error(f"Error processing test requests: {str(e)}")
            raise

    def update_config(self, selected_model: str) -> bool:
        """
        Update the configuration with the selected model.

        Args:
            selected_model: The selected model name

        Returns:
            True if the update was successful, False otherwise
        """
        try:
            # Get the project root directory
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_dir = os.path.join(project_root, "config")
            config_path = os.path.join(config_dir, "settings.json")

            # Create config directory if it doesn't exist
            os.makedirs(config_dir, exist_ok=True)

            # Load existing config or create new one
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    config = json.load(f)
            else:
                config = {}

            # Update the model setting
            config["default_ollama_model"] = selected_model

            # Write the updated config
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)

            logger.info(f"Updated configuration with model: {selected_model}")
            return True
        except Exception as e:
            logger.error(f"Failed to update configuration: {str(e)}")
            return False

    def switch_model(self):
        """Interactively switch the AI model at runtime."""
        # Get available models for the selected provider
        if self.config["default_ai_provider"] == "ollama":
            from labeeb.services.health_check.ollama_health_check import check_ollama_server

            ok, tags_json = check_ollama_server()
            if not ok:
                output.error("Could not connect to Ollama server. Please ensure it's running.")
                return

            if not tags_json or not isinstance(tags_json, list):
                output.error("No models available from Ollama server.")
                return

            if ok and tags_json and isinstance(tags_json, list):
                available_models = [m.get("name", "") for m in tags_json if m.get("name")]
            else:
                available_models = []
        else:
            output.error("Invalid provider selected.")
            return

        if not available_models:
            output.error("No models available for the selected provider.")
            return

        print("\nAvailable models:")
        for i, model in enumerate(available_models, 1):
            print(f"{i}. {model}")

        choice = input("Enter model number to switch to (or press Enter to abort): ").strip()
        if not choice or not choice.isdigit():
            output.info("Model switch aborted.")
            return

        idx = int(choice) - 1
        if 0 <= idx < len(available_models):
            selected_model = available_models[idx]
            # Update provider and model in config
            self.config["default_ai_provider"] = "ollama"
            self.config["default_ollama_model"] = selected_model

            # Save config to file
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "config",
                "settings.json",
            )
            with open(config_path, "w") as f:
                json.dump(self.config, f, indent=2)

            # Re-initialize AI handler
            self.ai_handler = AIHandler(model_manager=ModelManager(config_manager=ConfigManager()))
            output.success(f"Switched to Ollama model: {selected_model}")
        else:
            output.error("Invalid model selection.")


async def main():
    """Main entry point for Labeeb."""
    parser = argparse.ArgumentParser(description="Labeeb - AI-powered shell assistant")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "--fast", action="store_true", help="Enable fast mode (minimal prompts, quick exit)"
    )
    parser.add_argument(
        "--mode",
        choices=["interactive", "command", "file"],
        default="interactive",
        help="Operation mode: interactive, command, or file",
    )
    parser.add_argument("--command", help="Single command to execute")
    parser.add_argument("--file", help="File containing commands to execute")
    parser.add_argument("--tasks", nargs="+", help="List of tasks to execute")
    parser.add_argument("--test-dir", help="Directory for test-related operations")

    args = parser.parse_args()

    try:
        # Set up logging
        setup_logging("main")

        # Initialize Labeeb
        labeeb = Labeeb(debug=args.debug, mode=args.mode, fast_mode=args.fast)

        if args.command:
            # Process single command
            response = labeeb.process_single_command(args.command)
            print(response)
        elif args.file:
            # Process commands from file
            with open(args.file, "r", encoding="utf-8") as f:
                commands = f.readlines()
            for cmd in commands:
                cmd = cmd.strip()
                if cmd and not cmd.startswith("#"):
                    response = labeeb.process_single_command(cmd)
                    print(response)
        elif args.tasks:
            # Process list of tasks
            labeeb._process_tasks_sequentially(args.tasks)
        else:
            # Start interactive session
            labeeb.start()

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)


async def process_command_and_log(command: str):
    """Process a command and log its execution."""
    try:
        start_time = datetime.now()
        response = await process_command(command)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        log_entry = {
            "timestamp": start_time.isoformat(),
            "command": command,
            "response": response,
            "duration": duration,
        }

        # Log to file
        log_file = os.path.join(project_root, "logs", "command_history.json")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        with open(log_file, "a", encoding="utf-8") as f:
            json.dump(log_entry, f, ensure_ascii=False)
            f.write("\n")

        return response
    except Exception as e:
        logger.error(f"Error processing command: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
