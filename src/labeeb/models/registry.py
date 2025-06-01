"""
Model Registry for Labeeb

This module provides a central registry for all model classes, supporting dynamic discovery and documentation.
Compliant with @model-architecture.mdc: all models must be registered here for discoverability and integration.
"""

from typing import Type, Dict, List

# Example: from .user_model import UserModel
# from .system_types import SystemTypes  # Uncomment if SystemTypes is a class


class ModelRegistry:
    """Central registry for model classes."""

    _registry: Dict[str, Type] = {}

    @classmethod
    def register(cls, model_class: Type):
        cls._registry[model_class.__name__] = model_class

    @classmethod
    def get(cls, name: str) -> Type:
        return cls._registry[name]

    @classmethod
    def list_models(cls) -> List[str]:
        return list(cls._registry.keys())


# Register built-in models here
# ModelRegistry.register(SystemTypes)  # Uncomment if SystemTypes is a class
