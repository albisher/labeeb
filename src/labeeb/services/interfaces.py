"""
Service Interfaces for defining service contracts.

---
description: Defines interfaces and contracts for services
endpoints: [service_interfaces]
inputs: [service_definition]
outputs: [interface_contract]
dependencies: [abc, typing]
auth: none
alwaysApply: false
---

- Define service interfaces
- Specify input/output contracts
- Support service composition
- Enable service orchestration
- Document service contracts
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Protocol

class ServiceInterface(ABC):
    """Base interface for all services."""

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the service."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the service."""
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get service status."""
        pass

class CommandProcessorInterface(ServiceInterface):
    """Interface for command processing services."""

    @abstractmethod
    def process_command(self, command: str) -> str:
        """Process a command."""
        pass

    @abstractmethod
    def process_command_async(self, command: str) -> str:
        """Process a command asynchronously."""
        pass

class AIHandlerInterface(ServiceInterface):
    """Interface for AI handling services."""

    @abstractmethod
    def process_command(self, command: str) -> str:
        """Process a command using AI."""
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the AI model."""
        pass

class ErrorHandlerInterface(ServiceInterface):
    """Interface for error handling services."""

    @abstractmethod
    def handle_error(self, error: Exception) -> None:
        """Handle an error."""
        pass

    @abstractmethod
    def get_error_history(self) -> List[Dict[str, Any]]:
        """Get error history."""
        pass

class CacheInterface(ServiceInterface):
    """Interface for caching services."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Set a value in cache."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear the cache."""
        pass

class HistoryInterface(ServiceInterface):
    """Interface for history tracking services."""

    @abstractmethod
    def add(self, key: str, value: Any) -> None:
        """Add an entry to history."""
        pass

    @abstractmethod
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get history entries."""
        pass

    @abstractmethod
    def clear_history(self) -> None:
        """Clear history."""
        pass

class ServiceComposer(Protocol):
    """Protocol for service composition."""

    def compose_services(self, services: List[ServiceInterface]) -> ServiceInterface:
        """Compose multiple services into one."""
        pass

class ServiceOrchestrator(Protocol):
    """Protocol for service orchestration."""

    def orchestrate_services(
        self,
        services: List[ServiceInterface],
        workflow: Dict[str, Any]
    ) -> Any:
        """Orchestrate services according to workflow."""
        pass 