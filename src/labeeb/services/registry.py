"""
Service Registry for Labeeb

This module provides a central registry for all service classes, supporting dynamic discovery and documentation.
Compliant with @service-architecture.mdc: all services must be registered here for discoverability and integration.
"""

from typing import Type, Dict, List


class ServiceRegistry:
    """Central registry for service classes."""

    _registry: Dict[str, Type] = {}

    @classmethod
    def register(cls, service_class: Type):
        cls._registry[service_class.__name__] = service_class

    @classmethod
    def get(cls, name: str) -> Type:
        return cls._registry[name]

    @classmethod
    def list_services(cls) -> List[str]:
        return list(cls._registry.keys())


# Register built-in services here
