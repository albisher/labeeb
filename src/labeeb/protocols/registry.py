"""
Protocol Registry for Labeeb

This module provides a central registry for all protocol classes, supporting dynamic discovery and documentation.
Compliant with @protocol-architecture.mdc: all protocols must be registered here for discoverability and integration.
"""

from typing import Type, Dict, List


class ProtocolRegistry:
    """Central registry for protocol classes."""

    _registry: Dict[str, Type] = {}

    @classmethod
    def register(cls, protocol_class: Type):
        cls._registry[protocol_class.__name__] = protocol_class

    @classmethod
    def get(cls, name: str) -> Type:
        return cls._registry[name]

    @classmethod
    def list_protocols(cls) -> List[str]:
        return list(cls._registry.keys())


# Register built-in protocols here
