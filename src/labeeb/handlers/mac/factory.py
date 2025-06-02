"""
Mac Handler Factory for creating platform-specific handlers.

---
description: Creates and initializes Mac-specific handlers
endpoints: [mac_handler_factory]
inputs: [handler_name]
outputs: [handler_instance]
dependencies: [logging]
auth: none
alwaysApply: true
---

- Create Mac-specific handlers
- Initialize handler instances
- Handle handler configuration
- Support handler lifecycle
- Provide handler utilities
"""

import logging
from typing import Dict, Any, Optional, Type

logger = logging.getLogger(__name__)

class MacHandlerFactory:
    """Factory for creating Mac-specific handlers."""

    _handlers: Dict[str, Type] = {}

    @classmethod
    def register_handler(cls, name: str, handler_class: Type) -> None:
        """
        Register a handler class.

        Args:
            name: Handler name
            handler_class: Handler class
        """
        cls._handlers[name] = handler_class
        logger.info(f"Registered Mac handler: {name}")

    @classmethod
    def create_handler(cls, name: str) -> Optional[Any]:
        """
        Create a handler instance.

        Args:
            name: Handler name

        Returns:
            Optional[Any]: Handler instance if available
        """
        handler_class = cls._handlers.get(name)
        if not handler_class:
            logger.warning(f"Mac handler not found: {name}")
            return None

        try:
            handler = handler_class()
            logger.info(f"Created Mac handler: {name}")
            return handler
        except Exception as e:
            logger.error(f"Error creating Mac handler {name}: {str(e)}")
            return None

# Register built-in handlers
from labeeb.handlers.mac.browser import MacBrowserHandler
from labeeb.handlers.mac.input import MacInputHandler
from labeeb.handlers.mac.net import MacNetHandler
from labeeb.handlers.mac.fs import MacFSHandler
from labeeb.handlers.mac.audio import MacAudioHandler
from labeeb.handlers.mac.display import MacDisplayHandler
from labeeb.handlers.mac.usb import MacUSBHandler

MacHandlerFactory.register_handler("browser", MacBrowserHandler)
MacHandlerFactory.register_handler("input", MacInputHandler)
MacHandlerFactory.register_handler("net", MacNetHandler)
MacHandlerFactory.register_handler("fs", MacFSHandler)
MacHandlerFactory.register_handler("audio", MacAudioHandler)
MacHandlerFactory.register_handler("display", MacDisplayHandler)
MacHandlerFactory.register_handler("usb", MacUSBHandler) 