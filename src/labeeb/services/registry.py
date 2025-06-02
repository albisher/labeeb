"""
Service Registry for managing and discovering services.

---
description: Provides service registration, discovery, and health monitoring
endpoints: [service_registry]
inputs: [service_name, service_instance]
outputs: [service_info]
dependencies: [logging]
auth: none
alwaysApply: false
---

- Register services with metadata
- Discover services by name or type
- Monitor service health
- Track service dependencies
- Manage service lifecycle
"""

import logging
from typing import Dict, Any, Optional, Type, List
from datetime import datetime

logger = logging.getLogger(__name__)

class ServiceRegistry:
    """Manages service registration and discovery."""

    def __init__(self):
        """Initialize the service registry."""
        self._services: Dict[str, Dict[str, Any]] = {}
        self._health_checks: Dict[str, Any] = {}
        logger.info("Service registry initialized")

    def register_service(
        self,
        name: str,
        service: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Register a service with the registry.

        Args:
            name: Service name
            service: Service instance
            metadata: Optional service metadata
        """
        if name in self._services:
            logger.warning(f"Service {name} already registered, updating...")

        self._services[name] = {
            "instance": service,
            "metadata": metadata or {},
            "registered_at": datetime.now(),
            "last_health_check": None,
            "status": "unknown"
        }
        logger.info(f"Registered service: {name}")

    def get_service(self, name: str) -> Optional[Any]:
        """
        Get a service by name.

        Args:
            name: Service name

        Returns:
            Optional[Any]: Service instance if found
        """
        service_info = self._services.get(name)
        if not service_info:
            logger.warning(f"Service not found: {name}")
            return None
        return service_info["instance"]

    def get_service_metadata(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get service metadata.

        Args:
            name: Service name

        Returns:
            Optional[Dict[str, Any]]: Service metadata if found
        """
        service_info = self._services.get(name)
        if not service_info:
            return None
        return service_info["metadata"]

    def register_health_check(self, name: str, check_func: Any) -> None:
        """
        Register a health check function for a service.

        Args:
            name: Service name
            check_func: Health check function
        """
        self._health_checks[name] = check_func
        logger.info(f"Registered health check for service: {name}")

    def check_service_health(self, name: str) -> bool:
        """
        Check service health.

        Args:
            name: Service name

        Returns:
            bool: True if service is healthy
        """
        service_info = self._services.get(name)
        if not service_info:
            logger.warning(f"Service not found: {name}")
            return False

        check_func = self._health_checks.get(name)
        if not check_func:
            logger.warning(f"No health check registered for service: {name}")
            return False

        try:
            is_healthy = check_func(service_info["instance"])
            service_info["last_health_check"] = datetime.now()
            service_info["status"] = "healthy" if is_healthy else "unhealthy"
            return is_healthy
        except Exception as e:
            logger.error(f"Health check failed for service {name}: {str(e)}")
            service_info["status"] = "error"
            return False

    def get_all_services(self) -> List[str]:
        """
        Get all registered service names.

        Returns:
            List[str]: List of service names
        """
        return list(self._services.keys())

    def get_service_status(self, name: str) -> Optional[str]:
        """
        Get service status.

        Args:
            name: Service name

        Returns:
            Optional[str]: Service status if found
        """
        service_info = self._services.get(name)
        if not service_info:
            return None
        return service_info["status"]

    def unregister_service(self, name: str) -> None:
        """
        Unregister a service.

        Args:
            name: Service name
        """
        if name in self._services:
            del self._services[name]
            if name in self._health_checks:
                del self._health_checks[name]
            logger.info(f"Unregistered service: {name}")
        else:
            logger.warning(f"Service not found: {name}")
