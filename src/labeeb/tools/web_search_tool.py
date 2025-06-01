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

import logging
from typing import List, Dict, Any
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)

class WebSearchTool:
    """Tool for performing web searches."""
    
    def __init__(self):
        """Initialize the web search tool."""
        self.ddgs = DDGS()
        
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
            results = []
            for r in self.ddgs.text(query, max_results=max_results):
                # Handle different response formats
                title = r.get("title", r.get("text", ""))
                link = r.get("link", r.get("url", ""))
                snippet = r.get("body", r.get("snippet", ""))
                
                if title and link:  # Only add if we have at least title and link
                    results.append({
                        "title": title,
                        "link": link,
                        "snippet": snippet
                    })
            return results
            
        except Exception as e:
            logger.error(f"Error performing web search: {e}")
            raise 