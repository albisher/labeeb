"""
Calculator tool module for Labeeb.

This module provides functionality to perform arithmetic calculations.
It uses Python's eval() function with safety checks to evaluate expressions.

---
description: Perform arithmetic calculations
endpoints: [calculate]
inputs: [expression]
outputs: [result]
dependencies: []
auth: none
alwaysApply: false
---
"""

import logging
import re
from typing import Union, Any

logger = logging.getLogger(__name__)

class CalculatorTool:
    """Tool for performing arithmetic calculations."""
    
    def __init__(self):
        """Initialize the calculator tool."""
        # Define allowed operations and patterns
        self.allowed_ops = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '**': lambda x, y: x ** y,
            '%': lambda x, y: x % y
        }
        
        # Pattern to match valid arithmetic expressions
        self.valid_pattern = re.compile(r'^[\d\s+\-*/().%]+$')
        
    def calculate(self, expression: str) -> Union[float, int]:
        """
        Calculate the result of an arithmetic expression.
        
        Args:
            expression: The arithmetic expression to evaluate
            
        Returns:
            The result of the calculation
            
        Raises:
            ValueError: If the expression is invalid or contains unsafe operations
            ZeroDivisionError: If division by zero occurs
        """
        # Clean and validate expression
        expr = expression.strip()
        if not self.valid_pattern.match(expr):
            raise ValueError("Invalid expression: contains unsafe characters")
            
        try:
            # Evaluate the expression
            result = eval(expr, {"__builtins__": {}}, self.allowed_ops)
            
            # Convert to int if result is a whole number
            if isinstance(result, float) and result.is_integer():
                return int(result)
            return result
            
        except ZeroDivisionError:
            logger.error("Division by zero")
            raise
        except Exception as e:
            logger.error(f"Error calculating expression: {e}")
            raise ValueError(f"Invalid expression: {str(e)}") 