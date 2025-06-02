"""
Platform manager service for Labeeb.

This service provides a central manager for platform-specific functionality,
coordinating between different platform handlers and ensuring proper isolation.
Following service-architecture.mdc and handler-architecture.mdc rules.

---
description: Manages platform-specific functionality and handlers
endpoints: [get_handler, get_platform_info, initialize, cleanup]
inputs: [handler_type, platform_name]
outputs: [handler_instance, platform_info]
dependencies: [platform_utils, handlers]
auth: none
alwaysApply: true
---
"""

import os
import logging
from typing import Dict, Any, Optional, List, Type, ClassVar
from labeeb.core.platform_core.handlers.base_handler import BaseHandler
from labeeb.services.platform_services.common.system_info import BaseSystemInfoGatherer
from .browser_handler import BaseBrowserHandler
from .i18n import gettext as _, is_rtl, get_current_language, setup_language
from labeeb.services.platform_services.common.platform_utils import (
    get_os_identifier,
    get_platform_name,
    PLATFORM_MAP
)

logger = logging.getLogger(__name__)


class PlatformManager:
    """Manager for platform-specific functionality.
    
    This is a singleton service that manages platform-specific handlers and functionality.
    Following service-architecture.mdc: single responsibility, clear interfaces, and proper error handling.
    """
    
    # Singleton instance
    _instance: ClassVar[Optional['PlatformManager']] = None
    
    # Supported platforms using canonical names
    SUPPORTED_PLATFORMS = {
        "macos": "macos",
        "windows": "windows",
        "linux": "linux"
    }
    
    # Platform-specific handler mappings
    _system_info_gatherers: Dict[str, Type[BaseSystemInfoGatherer]] = {
        "macos": None,  # Will be lazily loaded
        "windows": None,  # Will be lazily loaded
        "linux": None,  # Will be lazily loaded
    }
    
    _shell_handlers: Dict[str, Any] = {
        "macos": None,  # Will be lazily loaded
        "windows": None,  # TODO: Implement Windows shell handler
        "linux": None,  # TODO: Implement Linux shell handler
    }
    
    _browser_handlers: Dict[str, Any] = {
        "macos": None,  # Will be lazily loaded
        "windows": None,  # TODO: Implement Windows browser handler
        "linux": None,  # TODO: Implement Linux browser handler
    }
    
    def __new__(cls) -> 'PlatformManager':
        """Enforce singleton pattern.
        
        Returns:
            PlatformManager: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the platform manager if not already initialized."""
        if not hasattr(self, '_initialized'):
            try:
                self.os_identifier = get_os_identifier()
                self.platform_name = get_platform_name()
                self.handlers: Dict[str, BaseHandler] = {}
                self._config: Dict[str, Any] = {}
                self._initialized = False

                # Initialize language and RTL support
                self.current_language = get_current_language()
                self.rtl_support = is_rtl(self.current_language)
                setup_language(self.current_language)

                # Lazy load platform-specific modules
                self._load_platform_modules()

                # Initialize the manager
                self.initialize()

                logger.info(f"Platform manager initialized for platform: {self.platform_name}")
            except Exception as e:
                logger.error(f"Failed to initialize platform manager: {e}")
                raise
    
    def _load_platform_modules(self) -> None:
        """Load platform-specific modules based on the current platform."""
        try:
            if self.platform_name == "macos":
                from .mac.system_info import MacSystemInfoGatherer
                from .handlers.mac.shell_handler import MacShellHandler
                from .handlers.mac.browser_handler import MacBrowserHandler
                from .handlers.mac.input_handler import MacInputHandler
                from .handlers.mac.audio_handler import MacAudioHandler
                from .handlers.mac.usb_handler import MacUSBHandler
                self._system_info_gatherers["macos"] = MacSystemInfoGatherer
                self._shell_handlers["macos"] = MacShellHandler
                self._browser_handlers["macos"] = MacBrowserHandler
                self._mac_input_handler = MacInputHandler
                self._mac_audio_handler = MacAudioHandler
                self._mac_usb_handler = MacUSBHandler
            elif self.platform_name == "windows":
                from .windows.system_info import WindowsSystemInfoGatherer
                self._system_info_gatherers["windows"] = WindowsSystemInfoGatherer
            elif self.platform_name == "linux":
                from .ubuntu.system_info import UbuntuSystemInfoGatherer
                from labeeb.core.platform_core.handlers.linux.shell_handler import LinuxShellHandler
                from labeeb.core.platform_core.handlers.linux.browser_handler import LinuxBrowserHandler
                self._system_info_gatherers["linux"] = UbuntuSystemInfoGatherer
                self._shell_handlers["linux"] = LinuxShellHandler
                self._browser_handlers["linux"] = LinuxBrowserHandler
            else:
                logger.warning(f"Unsupported platform: {self.platform_name}")
        except ImportError as e:
            logger.error(f"Failed to load platform modules: {e}")
            raise
    
    def _load_config(self) -> None:
        """Load platform-specific configuration."""
        try:
            config_path = os.path.join(os.path.dirname(__file__), self.platform_name, "config.json")
            
            if os.path.exists(config_path):
                import json
                with open(config_path, "r", encoding="utf-8") as f:
                    self._config = json.load(f)
                logger.info(f"Loaded configuration from {config_path}")
            else:
                logger.warning(f"No configuration file found at {config_path}")
                self._config = {}
                
        except Exception as e:
            logger.error(f"Failed to load platform configuration: {e}")
            self._config = {}
    
    def initialize(self) -> bool:
        """Initialize the platform manager.
        
        Returns:
            bool: True if initialization was successful, False otherwise.
        """
        if self._initialized:
            return True
        
        try:
            # Load platform configuration
            self._load_config()
            
            # Initialize platform-specific handlers
            self._initialize_handlers()
            
            # Update RTL support based on current language
            self.current_language = get_current_language()
            self.rtl_support = is_rtl(self.current_language)
            
            self._initialized = True
            logger.info(f"Platform manager initialized with handlers: {list(self.handlers.keys())}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize PlatformManager: {e}")
            return False
    
    def _initialize_handlers(self) -> None:
        """Initialize platform-specific handlers."""
        try:
            if self.platform_name == "macos":
                from labeeb.core.platform_core.handlers.mac.display_handler import MacDisplayHandler
                from labeeb.core.platform_core.handlers.mac.input_handler import MacInputHandler
                from labeeb.core.platform_core.handlers.mac.audio_handler import MacAudioHandler
                from labeeb.core.platform_core.handlers.mac.usb_handler import MacUSBHandler
                handler_map: Dict[str, Type[BaseHandler]] = {
                    "input": MacInputHandler,
                    "audio": MacAudioHandler,
                    "display": MacDisplayHandler,
                    "usb": MacUSBHandler,
                    "shell": self._shell_handlers["macos"],
                    "browser": self._browser_handlers["macos"],
                }
            elif self.platform_name == "linux":
                from labeeb.core.platform_core.handlers.linux.shell_handler import LinuxShellHandler
                from labeeb.core.platform_core.handlers.linux.browser_handler import LinuxBrowserHandler
                handler_map: Dict[str, Type[BaseHandler]] = {
                    "shell": LinuxShellHandler,
                    "browser": LinuxBrowserHandler,
                }
            else:
                handler_map: Dict[str, Type[BaseHandler]] = {}

            # Initialize each handler
            for handler_type, handler_class in handler_map.items():
                if handler_class is None:
                    logger.warning(f"{handler_type} handler class is None")
                    continue
                try:
                    handler = handler_class(self._config.get(handler_type, {}))
                    if handler.initialize():
                        self.handlers[handler_type] = handler
                        logger.info(f"Successfully initialized {handler_type} handler")
                    else:
                        logger.warning(f"{handler_type} handler initialization failed")
                except Exception as e:
                    logger.error(f"Error initializing {handler_type} handler: {e}")
            logger.info(f"Handlers after initialization: {list(self.handlers.keys())}")
        except Exception as e:
            logger.error(f"Failed to initialize handlers: {e}")
            raise
    
    def get_handler(self, handler_type: str) -> Optional[BaseHandler]:
        """Get a platform-specific handler.
        
        Args:
            handler_type: Type of handler to get (e.g., 'input', 'audio').
            
        Returns:
            Optional[BaseHandler]: The requested handler or None if not available.
        """
        logger.info(f"Getting handler '{handler_type}'. Available handlers: {list(self.handlers.keys())}")
        return self.handlers.get(handler_type)
    
    def is_handler_available(self, handler_type: str) -> bool:
        """Check if a handler is available.
        
        Args:
            handler_type: Type of handler to check.
            
        Returns:
            bool: True if the handler is available, False otherwise.
        """
        return handler_type in self.handlers
    
    def get_platform(self) -> str:
        """Get the current platform identifier.
        
        Returns:
            str: Platform identifier.
        """
        return self.platform_name
    
    def is_platform_supported(self) -> bool:
        """Check if the current platform is supported.
        
        Returns:
            bool: True if the platform is supported, False otherwise.
        """
        return self.platform_name in self.SUPPORTED_PLATFORMS
    
    def get_config(self) -> Dict[str, Any]:
        """Get the platform configuration.
        
        Returns:
            Dict[str, Any]: Platform configuration.
        """
        return self._config.copy()
    
    def get_available_handlers(self) -> List[str]:
        """Get list of available handlers.
        
        Returns:
            List[str]: List of available handler types.
        """
        return list(self.handlers.keys())
    
    def get_platform_info(self) -> Dict[str, Any]:
        """Get platform information.
        
        Returns:
            Dict[str, Any]: Platform information including features and paths.
        """
        return {
            "platform": self.platform_name,
            "platform_name": self.platform_name,
            "features": self._get_platform_features(),
            "paths": self._get_platform_paths(),
            "language": self.current_language,
            "rtl_support": self.rtl_support,
        }
    
    def _get_platform_features(self) -> Dict[str, bool]:
        """Get platform-specific features.
        
        Returns:
            Dict[str, bool]: Dictionary of feature flags.
        """
        features = {
            "gui": True,
            "audio": True,
            "usb": True,
            "bluetooth": True,
            "network": True,
            "shell": True,
            "browser": True,
            "rtl": self.rtl_support,
        }
        
        # Platform-specific feature adjustments
        if self.platform_name == "macos":
            features.update({"calendar": True, "notifications": True, "accessibility": True})
        elif self.platform_name == "win32":
            features.update({"calendar": False, "notifications": True, "accessibility": True})
        elif self.platform_name.startswith("linux"):
            features.update({"calendar": False, "notifications": True, "accessibility": True})
            
        return features
    
    def _get_platform_paths(self) -> Dict[str, str]:
        """Get platform-specific paths.
        
        Returns:
            Dict[str, str]: Dictionary of platform paths.
        """
        paths = {}
        
        if self.platform_name == "macos":
            paths.update(
                {
                    "home": os.path.expanduser("~"),
                    "config": os.path.join(
                        os.path.expanduser("~"), "Library", "Application Support", "Labeeb"
                    ),
                    "cache": os.path.join(os.path.expanduser("~"), "Library", "Caches", "Labeeb"),
                    "logs": os.path.join(os.path.expanduser("~"), "Library", "Logs", "Labeeb"),
                }
            )
        elif self.platform_name == "win32":
            paths.update(
                {
                    "home": os.path.expanduser("~"),
                    "config": os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Labeeb"),
                    "cache": os.path.join(os.path.expanduser("~"), "AppData", "Local", "Labeeb"),
                    "logs": os.path.join(
                        os.path.expanduser("~"), "AppData", "Local", "Labeeb", "Logs"
                    ),
                }
            )
        elif self.platform_name.startswith("linux"):
            paths.update(
                {
                    "home": os.path.expanduser("~"),
                    "config": os.path.join(os.path.expanduser("~"), ".config", "labeeb"),
                    "cache": os.path.join(os.path.expanduser("~"), ".cache", "labeeb"),
                    "logs": os.path.join(
                        os.path.expanduser("~"), ".local", "share", "labeeb", "logs"
                    ),
                }
            )
            
        return paths
    
    def get_handlers(self) -> Dict[str, Any]:
        """Get all initialized handlers.
        
        Returns:
            Dict[str, Any]: Dictionary of initialized handlers.
        """
        return self.handlers.copy()
    
    def cleanup(self) -> None:
        """Clean up platform manager resources."""
        if not self._initialized:
            return
        
        try:
            # Clean up all handlers
            for handler in self.handlers.values():
                try:
                    handler.cleanup()
                except Exception as e:
                    logger.error(f"Error cleaning up handler: {e}")
            
            self.handlers.clear()
            self._initialized = False
            PlatformManager._instance = None  # Reset singleton instance
            logger.info("Platform manager cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during platform manager cleanup: {e}")
            raise
    
    @classmethod
    def get_instance(cls) -> 'PlatformManager':
        """Get the singleton instance of PlatformManager.
            
        Returns:
            PlatformManager: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def get_platform_system_info_gatherer() -> Optional[BaseSystemInfoGatherer]:
    """Get the appropriate system info gatherer for the current platform.
    
    This function provides a module-level interface to access the system info gatherer
    while maintaining proper encapsulation and avoiding circular dependencies.
    
    Returns:
        Optional[BaseSystemInfoGatherer]: The system info gatherer instance for the current platform,
        or None if not available.
    """
    try:
        return platform_manager.get_handler("system_info")
    except Exception as e:
        logger.error(f"Failed to get system info gatherer: {e}")
        return None
