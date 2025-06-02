"""
Command Processor Service for handling user commands.

---
description: Processes and executes user commands
endpoints: [command_processor]
inputs: [command]
outputs: [result]
dependencies: [ai_handler, ai_command_extractor, error_handler, user_interaction_history, ai_response_cache]
auth: none
alwaysApply: false
---

- Receive command from user
- Check response cache for existing result
- Process command using AI handler
- Extract and validate command
- Store result in cache
- Update interaction history
- Handle errors appropriately
"""

import logging
from typing import Dict, Any, Optional
import asyncio

from labeeb.services.ai_handler import AIHandler
from labeeb.core.exceptions import CommandError
from labeeb.services.ai_command_extractor import AICommandExtractor
from labeeb.services.error_handler import ErrorHandler
from labeeb.services.user_interaction_history import UserInteractionHistory
from labeeb.services.ai_response_cache import AIResponseCache

logger = logging.getLogger(__name__)

class CommandProcessor:
    """Processes and executes user commands."""
    
    def __init__(self, ai_handler: AIHandler):
        """Initialize the command processor.
        
        Args:
            ai_handler: The AI handler to use for processing commands
        """
        self.ai_handler = ai_handler
        self.command_extractor = AICommandExtractor()
        self.error_handler = ErrorHandler()
        self.interaction_history = UserInteractionHistory()
        self.response_cache = AIResponseCache()
        logger.info("Command processor initialized")
    
    def process_command(self, command: str) -> str:
        """Process a command synchronously.
        
        Args:
            command: The command to process
            
        Returns:
            The command result
            
        Raises:
            CommandError: If there's an error processing the command
        """
        try:
            # Create event loop if needed
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run the async command
            return loop.run_until_complete(self.process_command_async(command))
        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            raise CommandError(f"Failed to process command: {str(e)}")
    
    async def process_command_async(self, command: str) -> str:
        """Process a command asynchronously.
        
        Args:
            command: The command to process
            
        Returns:
            The command result
            
        Raises:
            CommandError: If there's an error processing the command
        """
        try:
            # Check cache first
            cached_result = self.response_cache.get(command)
            if cached_result:
                return cached_result

            # Process the command using the AI handler
            result = await self.ai_handler.process_command(command)
            
            # Extract and validate command
            success, plan, metadata = self.command_extractor.extract_command(result)
            if not success:
                error_msg = metadata.get("error_message", "Unknown error")
                logger.error(f"Command extraction failed: {error_msg}")
                raise CommandError(f"Failed to extract command: {error_msg}")

            # Store in cache
            self.response_cache.set(command, result)
            
            # Update interaction history
            self.interaction_history.add(command, result)
            
            return result
        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            self.error_handler.handle_error(e)
            raise CommandError(f"Failed to process command: {str(e)}")
