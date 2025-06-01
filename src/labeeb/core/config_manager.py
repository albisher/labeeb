"""
Configuration management module for Labeeb.

This module provides centralized configuration management for the Labeeb application.
It handles loading, validating, and accessing configuration settings from various sources,
including environment variables, configuration files, and command-line arguments.

---
description: Manages application configuration and settings
endpoints: [get, set, save, reload]
inputs: [key, value]
outputs: [config_value]
dependencies: [FileOperationConfig]
auth: none
alwaysApply: true
---
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union, List, TypeVar, cast
from dataclasses import dataclass, field
from datetime import datetime
import re

# Set up logging
logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class LoggingConfig:
    """Configuration for logging settings."""

    log_level: str = "INFO"
    log_file: str = "logs/labeeb.log"
    log_errors: bool = True
    log_commands: bool = True
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class FileOperationConfig:
    """Configuration for file operations."""

    base_dir: str = os.path.expanduser("~/Documents/labeeb")
    screenshots_dir: str = "screenshots"
    downloads_dir: str = "downloads"
    temp_dir: str = "temp"
    logs_dir: str = "logs"
    config_dir: str = "config"
    last_updated: datetime = field(default_factory=datetime.now)

    def get_full_path(self, subdir: str) -> str:
        """Get the full path for a subdirectory."""
        return os.path.join(self.base_dir, subdir)

    def ensure_directories(self) -> bool:
        """Ensure all required directories exist."""
        try:
            dirs = [
                self.base_dir,
                self.get_full_path(self.screenshots_dir),
                self.get_full_path(self.downloads_dir),
                self.get_full_path(self.temp_dir),
                self.get_full_path(self.logs_dir),
                self.get_full_path(self.config_dir)
            ]
            for dir_path in dirs:
                os.makedirs(dir_path, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Error creating directories: {e}")
            return False


@dataclass
class LanguageConfig:
    """Configuration for language support."""

    english: bool = True
    arabic: bool = True
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class Config:
    """Main configuration dataclass."""

    default_ai_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    default_ollama_model: str = "gemma3:latest"
    text_model: str = "smolvlm"
    vision_model: str = "smolvlm"
    stt_model: str = "whisper"
    tts_model: str = "none"
    shell_safe_mode: bool = True
    shell_dangerous_check: bool = True
    interactive_mode: bool = True
    use_gui: bool = False
    use_structured_ai_responses: bool = True
    prefer_json_format: bool = True
    output_verbosity: str = "normal"
    language_support: LanguageConfig = field(default_factory=LanguageConfig)
    file_operation_settings: FileOperationConfig = field(default_factory=FileOperationConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    last_updated: datetime = field(default_factory=datetime.now)
    use_fp32: bool = True
    openweathermap_api_key: str = ""


class ConfigManager:
    """
    A class to manage configuration settings for Labeeb.

    This class provides a centralized way to manage configuration settings,
    supporting multiple configuration sources and validation.
    """

    def __init__(self):
        """Initialize the configuration manager."""
        self.file_config = FileOperationConfig()
        self.config = self._load_config()
        self._validate_config()

    def _load_config(self) -> Config:
        """Load configuration from files."""
        try:
            # First try user-specific config
            user_config_path = os.path.join(
                self.file_config.get_full_path(self.file_config.config_dir),
                "labeeb_config.json"
            )
            
            # Then try project-level config
            project_config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                "config",
                "labeeb_config.json"
            )
            
            # Try to load user config first, fall back to project config
            config_path = user_config_path if os.path.exists(user_config_path) else project_config_path
            
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    config_dict = json.load(f)
            else:
                # Create default config
                config_dict = self._get_default_config()
                # Save to user config directory
                os.makedirs(os.path.dirname(user_config_path), exist_ok=True)
                with open(user_config_path, "w", encoding="utf-8") as f:
                    json.dump(config_dict, f, indent=4)
            
            return self._dict_to_config(config_dict)
            
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return Config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "default_ai_provider": "ollama",
            "ollama_base_url": "http://localhost:11434",
            "default_ollama_model": "gemma3:latest",
            "text_model": "smolvlm",
            "vision_model": "smolvlm",
            "stt_model": "whisper",
            "tts_model": "none",
            "shell_safe_mode": True,
            "shell_dangerous_check": True,
            "interactive_mode": True,
            "use_gui": False,
            "use_structured_ai_responses": True,
            "prefer_json_format": True,
            "output_verbosity": "normal",
            "language_support": {
                "english": True,
                "arabic": True,
                "last_updated": datetime.now().isoformat()
            },
            "file_operation_settings": {
                "base_dir": os.path.expanduser("~/Documents/labeeb"),
                "screenshots_dir": "screenshots",
                "downloads_dir": "downloads",
                "temp_dir": "temp",
                "logs_dir": "logs",
                "config_dir": "config",
                "last_updated": datetime.now().isoformat()
            },
            "logging": {
                "log_level": "INFO",
                "log_file": "logs/labeeb.log",
                "log_errors": True,
                "log_commands": True,
                "last_updated": datetime.now().isoformat()
            },
            "last_updated": datetime.now().isoformat(),
            "use_fp32": True,
            "openweathermap_api_key": ""
        }

    def _dict_to_config(self, config_dict: Dict[str, Any]) -> Config:
        """Convert dictionary to Config object."""
        # Handle nested configs
        if "language_support" in config_dict:
            lang = config_dict["language_support"]
            if isinstance(lang, dict):
                if "last_updated" in lang and isinstance(lang["last_updated"], str):
                    try:
                        lang["last_updated"] = datetime.fromisoformat(lang["last_updated"])
                    except Exception:
                        lang["last_updated"] = datetime.now()
                config_dict["language_support"] = LanguageConfig(**lang)
                
        if "file_operation_settings" in config_dict:
            fos = config_dict["file_operation_settings"]
            if isinstance(fos, dict):
                if "last_updated" in fos and isinstance(fos["last_updated"], str):
                    try:
                        fos["last_updated"] = datetime.fromisoformat(fos["last_updated"])
                    except Exception:
                        fos["last_updated"] = datetime.now()
                config_dict["file_operation_settings"] = FileOperationConfig(**fos)
                
        if "logging" in config_dict:
            log = config_dict["logging"]
            if isinstance(log, dict):
                if "last_updated" in log and isinstance(log["last_updated"], str):
                    try:
                        log["last_updated"] = datetime.fromisoformat(log["last_updated"])
                    except Exception:
                        log["last_updated"] = datetime.now()
                config_dict["logging"] = LoggingConfig(**log)
                
        # Top-level last_updated
        if "last_updated" in config_dict and isinstance(config_dict["last_updated"], str):
            try:
                config_dict["last_updated"] = datetime.fromisoformat(config_dict["last_updated"])
            except Exception:
                config_dict["last_updated"] = datetime.now()
                
        return Config(**config_dict)

    def get(self, key: str, default: Optional[T] = None) -> Union[T, Any]:
        """Get a configuration value."""
        return getattr(self.config, key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        if not hasattr(self.config, key):
            raise ValueError(f"Invalid configuration key: {key}")
        setattr(self.config, key, value)
        self.config.last_updated = datetime.now()

    def save(self) -> None:
        """Save configuration to file."""
        try:
            config_path = os.path.join(
                self.file_config.get_full_path(self.file_config.config_dir),
                "labeeb_config.json"
            )
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            # Convert Config to dict
            config_dict = self._config_to_dict(self.config)
            
            # Save to file
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config_dict, f, indent=4)
                
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            raise

    def _config_to_dict(self, config: Config) -> Dict[str, Any]:
        """Convert Config object to dictionary."""
        return {
            "default_ai_provider": config.default_ai_provider,
            "ollama_base_url": config.ollama_base_url,
            "default_ollama_model": config.default_ollama_model,
            "text_model": config.text_model,
            "vision_model": config.vision_model,
            "stt_model": config.stt_model,
            "tts_model": config.tts_model,
            "shell_safe_mode": config.shell_safe_mode,
            "shell_dangerous_check": config.shell_dangerous_check,
            "interactive_mode": config.interactive_mode,
            "use_gui": config.use_gui,
            "use_structured_ai_responses": config.use_structured_ai_responses,
            "prefer_json_format": config.prefer_json_format,
            "output_verbosity": config.output_verbosity,
            "language_support": {
                "english": config.language_support.english,
                "arabic": config.language_support.arabic,
                "last_updated": config.language_support.last_updated.isoformat(),
            },
            "file_operation_settings": {
                "base_dir": config.file_operation_settings.base_dir,
                "screenshots_dir": config.file_operation_settings.screenshots_dir,
                "downloads_dir": config.file_operation_settings.downloads_dir,
                "temp_dir": config.file_operation_settings.temp_dir,
                "logs_dir": config.file_operation_settings.logs_dir,
                "config_dir": config.file_operation_settings.config_dir,
                "last_updated": config.file_operation_settings.last_updated.isoformat(),
            },
            "logging": {
                "log_level": config.logging.log_level,
                "log_file": config.logging.log_file,
                "log_errors": config.logging.log_errors,
                "log_commands": config.logging.log_commands,
                "last_updated": config.logging.last_updated.isoformat(),
            },
            "last_updated": config.last_updated.isoformat(),
            "use_fp32": config.use_fp32,
            "openweathermap_api_key": config.openweathermap_api_key,
        }

    def _validate_config(self) -> None:
        """Validate configuration settings."""
        required_settings = [
            "default_ai_provider",
            "ollama_base_url",
            "default_ollama_model",
            "text_model",
            "vision_model",
            "stt_model",
            "tts_model",
        ]

        for setting in required_settings:
            if not hasattr(self.config, setting):
                raise ValueError(f"Missing required setting: {setting}")

        if self.config.default_ai_provider != "ollama":
            raise ValueError("Invalid AI provider. Only 'ollama' is supported.")

        # Validate nested configs
        if not isinstance(self.config.language_support, LanguageConfig):
            raise ValueError("Invalid language support configuration")
        if not isinstance(self.config.file_operation_settings, FileOperationConfig):
            raise ValueError("Invalid file operation settings")
        if not isinstance(self.config.logging, LoggingConfig):
            raise ValueError("Invalid logging configuration")

    def reload(self) -> None:
        """Reload configuration from files."""
        self.config = self._load_config()
        self._validate_config()


DEFAULT_CONFIG = {
    "project_name": "Labeeb",
    "log_level": "INFO",
    "log_file": "log/labeeb.log",
    "log_errors": True,
    "log_commands": True,
}
