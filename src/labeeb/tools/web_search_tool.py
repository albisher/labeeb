"""
Web search tool module for Labeeb.

This module provides functionality to perform web searches.
It uses the DuckDuckGo API to perform searches.

---
description: Perform web searches
endpoints: [search]
inputs: [query]
outputs: [search_results]
dependencies: [duckduckgo_search]
auth: none
alwaysApply: false
---
"""

import time
import logging
from typing import List, Dict, Any
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)

class WebSearchTool:
    """Tool for performing web searches."""
    
    def __init__(self):
        """Initialize the web search tool."""
        self.ddgs = DDGS()
        self.last_request_time = 0
        self.min_delay = 2  # Minimum delay between requests in seconds
        self.max_retries = 3  # Maximum number of retries for rate-limited requests
        
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Perform a web search.
        
        Args:
            query: The search query
            max_results: Maximum number of results to return (default: 5)
            
        Returns:
            List of search results, each containing title, link, and snippet
            
        Raises:
            Exception: If the search fails
        """
        try:
            # Add delay between requests
            current_time = time.time()
            time_since_last_request = current_time - self.last_request_time
            if time_since_last_request < self.min_delay:
                time.sleep(self.min_delay - time_since_last_request)
                
            # Perform search with retries
            for attempt in range(self.max_retries):
                try:
                    results = []
                    for r in self.ddgs.text(query, max_results=max_results):
                        result = {
                            "title": r.get("title", ""),
                            "link": r.get("link", ""),
                            "snippet": r.get("body", "")
                        }
                        results.append(result)
                        
                    self.last_request_time = time.time()
                    return results
                    
                except Exception as e:
                    if "Ratelimit" in str(e) and attempt < self.max_retries - 1:
                        # Wait longer between retries
                        time.sleep(self.min_delay * (attempt + 2))
                        continue
                    raise
                    
        except Exception as e:
            error_msg = f"Error performing web search: {e}"
            logger.error(error_msg)
            raise Exception(error_msg) 