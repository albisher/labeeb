"""
Capability Registry for Labeeb

This module provides a central registry for all capability classes, supporting dynamic discovery and documentation.
Compliant with @capability-architecture.mdc: all capabilities must be registered here for discoverability and integration.
"""

from typing import Type, Dict, List


class CapabilityRegistry:
    """Central registry for capability classes."""

    _registry: Dict[str, Type] = {}

    @classmethod
    def register(cls, capability_class: Type):
        cls._registry[capability_class.__name__] = capability_class

    @classmethod
    def get(cls, name: str) -> Type:
        return cls._registry[name]

    @classmethod
    def list_capabilities(cls) -> List[str]:
        return list(cls._registry.keys())


# Register built-in capabilities here
