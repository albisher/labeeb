"""
Handler Registry for Labeeb

This module provides a central registry for all handler classes, supporting dynamic discovery and documentation.
Compliant with @handler-architecture.mdc: all handlers must be registered here for discoverability and integration.
"""

from typing import Type, Dict, List


class HandlerRegistry:
    """Central registry for handler classes."""

    _registry: Dict[str, Type] = {}

    @classmethod
    def register(cls, handler_class: Type):
        cls._registry[handler_class.__name__] = handler_class

    @classmethod
    def get(cls, name: str) -> Type:
        return cls._registry[name]

    @classmethod
    def list_handlers(cls) -> List[str]:
        return list(cls._registry.keys())


# Register built-in handlers here
