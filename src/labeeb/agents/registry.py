"""
Agent Registry for Labeeb

This module provides a central registry for all agent classes, supporting dynamic discovery and documentation.
Compliant with @agent-architecture.mdc: all agents must be registered here for discoverability and orchestration.
"""

from typing import Type, Dict, List
from .base_agent import BaseAgent
from .labeeb_agent import LabeebAgent


class AgentRegistry:
    """Central registry for agent classes."""

    _registry: Dict[str, Type[BaseAgent]] = {}

    @classmethod
    def register(cls, agent_class: Type[BaseAgent]):
        cls._registry[agent_class.__name__] = agent_class

    @classmethod
    def get(cls, name: str) -> Type[BaseAgent]:
        return cls._registry[name]

    @classmethod
    def list_agents(cls) -> List[str]:
        return list(cls._registry.keys())


# Register built-in agents
AgentRegistry.register(BaseAgent)
AgentRegistry.register(LabeebAgent)
