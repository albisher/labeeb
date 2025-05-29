"""
Configuration management module for Labeeb.

This module provides centralized configuration management for the Labeeb application.
It handles loading, validating, and accessing configuration settings from various sources,
including environment variables, configuration files, and command-line arguments.

The module includes:
- Configuration loading and validation
- Environment variable handling
- Default value management
- Configuration file support
- Type conversion and validation

Example:
    >>> config = ConfigManager()
    >>> model_type = config.get("model_type", "local")
    >>> ollama_url = config.get("ollama_base_url")
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

T = TypeVar('T')

@dataclass
class LoggingConfig:
    """Configuration for logging settings."""
    log_level: str = "INFO"
    log_file: str = "log/labeeb.log"
    log_errors: bool = True
    log_commands: bool = True
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class FileOperationConfig:
    """Configuration for file operations."""
    max_results: int = 20
    max_content_length: int = 1000
    default_directory: str = "data"
    test_directory: str = "tests"
    last_updated: datetime = field(default_factory=datetime.now)

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
    default_ollama_model: str = "gemma3:4b"
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
    supporting multiple configuration sources and validation. It handles:
    - Environment variables
    - Configuration files
    - Default values
    - Type conversion
    - Value validation
    
    Attributes:
        config_dir (Path): Directory for configuration files
        settings_file (Path): Path to the main configuration file
        user_settings_file (Path): Path to the user-specific configuration file
        config (Config): Current configuration settings
    """
    
    def __init__(self, settings_file: str = 'config/labeeb_config.json'):
        self.settings_file = settings_file
        self._ensure_config_file()
        self.config = self._load_config()
        self._validate_config()
        self.valid_keys = {
            'default_ai_provider',
            'ollama_base_url',
            'default_ollama_model',
            'text_model',
            'vision_model',
            'stt_model',
            'tts_model',
            'shell_safe_mode',
            'shell_dangerous_check',
            'interactive_mode',
            'use_gui',
            'use_structured_ai_responses',
            'prefer_json_format',
            'output_verbosity',
            'language_support',
            'use_fp32',
            'openweathermap_api_key'
        }
    
    def _ensure_config_file(self):
        config_dir = os.path.dirname(self.settings_file)
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
        if not os.path.exists(self.settings_file) or os.path.getsize(self.settings_file) == 0:
            with open(self.settings_file, 'w') as f:
                f.write('{}')
    
    def _load_config(self) -> Config:
        """Load configuration from files."""
        self._ensure_config_file()
        with open(self.settings_file, 'r') as f:
            try:
                config_dict = json.load(f)
            except json.JSONDecodeError:
                # If file is empty or invalid, reset to '{}'
                with open(self.settings_file, 'w') as fw:
                    fw.write('{}')
                config_dict = {}
        
        # Convert dict to Config object
        return self._dict_to_config(config_dict)
    
    def _dict_to_config(self, config_dict: Dict[str, Any]) -> Config:
        """Convert dictionary to Config object, filtering out unknown keys."""
        # Handle nested configs
        if 'language_support' in config_dict:
            lang = config_dict['language_support']
            if isinstance(lang, dict):
                if 'last_updated' in lang and isinstance(lang['last_updated'], str):
                    try:
                        lang['last_updated'] = datetime.fromisoformat(lang['last_updated'])
                    except Exception:
                        lang['last_updated'] = datetime.now()
                config_dict['language_support'] = LanguageConfig(**lang)
        if 'file_operation_settings' in config_dict:
            fos = config_dict['file_operation_settings']
            if isinstance(fos, dict):
                if 'last_updated' in fos and isinstance(fos['last_updated'], str):
                    try:
                        fos['last_updated'] = datetime.fromisoformat(fos['last_updated'])
                    except Exception:
                        fos['last_updated'] = datetime.now()
                config_dict['file_operation_settings'] = FileOperationConfig(**fos)
        if 'logging' in config_dict:
            log = config_dict['logging']
            if isinstance(log, dict):
                if 'last_updated' in log and isinstance(log['last_updated'], str):
                    try:
                        log['last_updated'] = datetime.fromisoformat(log['last_updated'])
                    except Exception:
                        log['last_updated'] = datetime.now()
                config_dict['logging'] = LoggingConfig(**log)
        # Top-level last_updated
        if 'last_updated' in config_dict and isinstance(config_dict['last_updated'], str):
            try:
                config_dict['last_updated'] = datetime.fromisoformat(config_dict['last_updated'])
            except Exception:
                config_dict['last_updated'] = datetime.now()
        # Only keep keys that are fields in Config
        config_fields = set(f.name for f in Config.__dataclass_fields__.values())
        filtered = {k: v for k, v in config_dict.items() if k in config_fields}
        if 'openweathermap_api_key' not in filtered:
            filtered['openweathermap_api_key'] = ""
        return Config(**filtered)
    
    def _interpolate_value(self, value: Any) -> Any:
        """Interpolate environment variables in a value, recursively for nested dicts/lists."""
        if isinstance(value, str):
            # Handle environment variable interpolation
            if value.startswith('${') and value.endswith('}'):
                var_name = value[2:-1]
                if ':-' in var_name:
                    var_name, default = var_name.split(':-', 1)
                    return os.environ.get(var_name, default)
                return os.environ.get(var_name, value)
            # Also interpolate any ${VAR} or ${VAR:-default} inside the string
            def replacer(match: re.Match) -> str:
                var = match.group(1)
                if ':-' in var:
                    var_name, default = var.split(':-', 1)
                    return os.environ.get(var_name, default)
                return os.environ.get(var, match.group(0))
            return re.sub(r'\${([^}]+)}', replacer, value)
        elif isinstance(value, dict):
            return {k: self._interpolate_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._interpolate_value(item) for item in value]
        return value
    
    def get(self, key: str, default: Optional[T] = None) -> Union[T, Any]:
        """Get a configuration value."""
        value = getattr(self.config, key, default)
        return self._interpolate_value(value)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        if not hasattr(self.config, key):
            raise ValueError(f"Invalid configuration key: {key}")
        setattr(self.config, key, value)
        self.config.last_updated = datetime.now()
    
    def save(self) -> None:
        """Save configuration to files."""
        self._validate_config()
        
        # Convert Config object to dict
        config_dict = self._config_to_dict(self.config)
        
        # Save settings.json
        config_dir = os.path.dirname(self.settings_file)
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
        with open(self.settings_file, 'w') as f:
            json.dump(config_dict, f, indent=4)
    
    def _config_to_dict(self, config: Config) -> Dict[str, Any]:
        """Convert Config object to dictionary."""
        return {
            'default_ai_provider': config.default_ai_provider,
            'ollama_base_url': config.ollama_base_url,
            'default_ollama_model': config.default_ollama_model,
            'text_model': config.text_model,
            'vision_model': config.vision_model,
            'stt_model': config.stt_model,
            'tts_model': config.tts_model,
            'shell_safe_mode': config.shell_safe_mode,
            'shell_dangerous_check': config.shell_dangerous_check,
            'interactive_mode': config.interactive_mode,
            'use_gui': config.use_gui,
            'use_structured_ai_responses': config.use_structured_ai_responses,
            'prefer_json_format': config.prefer_json_format,
            'output_verbosity': config.output_verbosity,
            'language_support': {
                'english': config.language_support.english,
                'arabic': config.language_support.arabic,
                'last_updated': config.language_support.last_updated.isoformat()
            },
            'file_operation_settings': {
                'max_results': config.file_operation_settings.max_results,
                'max_content_length': config.file_operation_settings.max_content_length,
                'default_directory': config.file_operation_settings.default_directory,
                'test_directory': config.file_operation_settings.test_directory,
                'last_updated': config.file_operation_settings.last_updated.isoformat()
            },
            'logging': {
                'log_level': config.logging.log_level,
                'log_file': config.logging.log_file,
                'log_errors': config.logging.log_errors,
                'log_commands': config.logging.log_commands,
                'last_updated': config.logging.last_updated.isoformat()
            },
            'last_updated': config.last_updated.isoformat(),
            'use_fp32': config.use_fp32,
            'openweathermap_api_key': config.openweathermap_api_key
        }
    
    def _validate_config(self) -> None:
        """Validate configuration settings."""
        required_settings = [
            'default_ai_provider',
            'ollama_base_url',
            'default_ollama_model',
            'text_model',
            'vision_model',
            'stt_model',
            'tts_model'
        ]
        
        for setting in required_settings:
            if not hasattr(self.config, setting):
                raise ValueError(f"Missing required setting: {setting}")
        
        if self.config.default_ai_provider != 'ollama':
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
    "log_commands": True
} 