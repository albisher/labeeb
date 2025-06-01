"""
Workflow Registry for Labeeb

This module provides a central registry for all workflow classes, supporting dynamic discovery and documentation.
Compliant with @workflow-architecture.mdc: all workflows must be registered here for discoverability and integration.
"""

from typing import Type, Dict, List


class WorkflowRegistry:
    """Central registry for workflow classes."""

    _registry: Dict[str, Type] = {}

    @classmethod
    def register(cls, workflow_class: Type):
        cls._registry[workflow_class.__name__] = workflow_class

    @classmethod
    def get(cls, name: str) -> Type:
        return cls._registry[name]

    @classmethod
    def list_workflows(cls) -> List[str]:
        return list(cls._registry.keys())


# Register built-in workflows here
