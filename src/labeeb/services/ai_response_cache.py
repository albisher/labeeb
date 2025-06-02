"""
AI Response Cache Service for caching AI model responses.

---
description: Caches AI model responses for improved performance
endpoints: [response_cache]
inputs: [key, response]
outputs: [cached_response]
dependencies: [logging]
auth: none
alwaysApply: false
---

- Cache AI model responses
- Manage cache size and TTL
- Provide cache retrieval
- Support cache statistics
- Handle cache eviction
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AIResponseCache:
    """Caches AI model responses for improved performance."""

    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        """
        Initialize the AI response cache.

        Args:
            max_size: Maximum number of responses to cache
            ttl: Time to live for cached responses in seconds
        """
        self.max_size = max_size
        self.ttl = ttl
        self.cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Get a response from the cache.

        Args:
            key: The cache key

        Returns:
            Optional[Dict[str, Any]]: The cached response, or None if not found or expired
        """
        if key not in self.cache:
            return None

        cached = self.cache[key]
        if self._is_expired(cached):
            del self.cache[key]
            return None

        logger.debug(f"Cache hit for key: {key}")
        return cached["response"]

    def set(self, key: str, response: Dict[str, Any]) -> None:
        """
        Set a response in the cache.

        Args:
            key: The cache key
            response: The response to cache
        """
        if len(self.cache) >= self.max_size:
            self._evict_oldest()

        self.cache[key] = {
            "response": response,
            "timestamp": datetime.now()
        }

        logger.debug(f"Cached response for key: {key}")

    def clear(self) -> None:
        """Clear the cache."""
        self.cache = {}
        logger.info("Cleared response cache")

    def _is_expired(self, cached: Dict[str, Any]) -> bool:
        """
        Check if a cached response is expired.

        Args:
            cached: The cached response

        Returns:
            bool: True if the response is expired, False otherwise
        """
        timestamp = cached["timestamp"]
        return datetime.now() - timestamp > timedelta(seconds=self.ttl)

    def _evict_oldest(self) -> None:
        """Evict the oldest entry from the cache."""
        if not self.cache:
            return

        oldest_key = min(
            self.cache.keys(),
            key=lambda k: self.cache[k]["timestamp"]
        )
        del self.cache[oldest_key]
        logger.debug(f"Evicted oldest cache entry: {oldest_key}")

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dict[str, Any]: Cache statistics
        """
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "ttl": self.ttl,
            "oldest_entry": min(
                (entry["timestamp"] for entry in self.cache.values()),
                default=None
            ),
            "newest_entry": max(
                (entry["timestamp"] for entry in self.cache.values()),
                default=None
            )
        }
