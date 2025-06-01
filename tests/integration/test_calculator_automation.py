"""
Integration tests for calculator automation functionality.

---
description: Test calculator automation
endpoints: [test_calculator_automation]
inputs: []
outputs: []
dependencies: [pytest]
auth: none
alwaysApply: false
---
"""

import os
import pytest
from labeeb.tools.calculator_tool import CalculatorTool
from labeeb.utils.platform_utils import ensure_labeeb_directories

@pytest.fixture
def calculator_tool():
    """Create a calculator tool instance."""
    return CalculatorTool()

def test_calculator_initialization(calculator_tool):
    """Test calculator tool initialization."""
    assert calculator_tool is not None
    assert isinstance(calculator_tool, CalculatorTool)

def test_basic_arithmetic(calculator_tool):
    """Test basic arithmetic operations."""
    # Test addition
    assert calculator_tool.calculate("2 + 2") == 4
    assert calculator_tool.calculate("10 + 20") == 30
    
    # Test subtraction
    assert calculator_tool.calculate("5 - 3") == 2
    assert calculator_tool.calculate("20 - 10") == 10
    
    # Test multiplication
    assert calculator_tool.calculate("4 * 3") == 12
    assert calculator_tool.calculate("10 * 5") == 50
    
    # Test division
    assert calculator_tool.calculate("10 / 2") == 5
    assert calculator_tool.calculate("20 / 4") == 5

def test_complex_operations(calculator_tool):
    """Test complex mathematical operations."""
    # Test parentheses
    assert calculator_tool.calculate("(2 + 3) * 4") == 20
    assert calculator_tool.calculate("(10 - 5) * (3 + 2)") == 25
    
    # Test exponents
    assert calculator_tool.calculate("2 ** 3") == 8
    assert calculator_tool.calculate("3 ** 2") == 9
    
    # Test square root
    assert calculator_tool.calculate("sqrt(16)") == 4
    assert calculator_tool.calculate("sqrt(25)") == 5

def test_error_handling(calculator_tool):
    """Test error handling in calculator."""
    # Test division by zero
    with pytest.raises(ZeroDivisionError):
        calculator_tool.calculate("10 / 0")
    
    # Test invalid expression
    with pytest.raises(ValueError):
        calculator_tool.calculate("2 + + 3")
    
    # Test invalid function
    with pytest.raises(ValueError):
        calculator_tool.calculate("invalid(5)")

def test_decimal_operations(calculator_tool):
    """Test operations with decimal numbers."""
    # Test addition with decimals
    assert calculator_tool.calculate("2.5 + 3.5") == 6.0
    assert calculator_tool.calculate("10.75 + 20.25") == 31.0
    
    # Test multiplication with decimals
    assert calculator_tool.calculate("2.5 * 2") == 5.0
    assert calculator_tool.calculate("3.5 * 2.5") == 8.75

def test_negative_numbers(calculator_tool):
    """Test operations with negative numbers."""
    # Test addition with negatives
    assert calculator_tool.calculate("-2 + 3") == 1
    assert calculator_tool.calculate("2 + (-3)") == -1
    
    # Test multiplication with negatives
    assert calculator_tool.calculate("-2 * 3") == -6
    assert calculator_tool.calculate("-2 * (-3)") == 6

def test_calculator_history(calculator_tool):
    """Test calculator history functionality."""
    # Perform some calculations
    calculator_tool.calculate("2 + 2")
    calculator_tool.calculate("3 * 4")
    calculator_tool.calculate("10 / 2")
    
    # Check history
    history = calculator_tool.get_history()
    assert len(history) == 3
    assert history[0]["expression"] == "2 + 2"
    assert history[0]["result"] == 4
    assert history[1]["expression"] == "3 * 4"
    assert history[1]["result"] == 12
    assert history[2]["expression"] == "10 / 2"
    assert history[2]["result"] == 5

def test_calculator_clear_history(calculator_tool):
    """Test clearing calculator history."""
    # Add some calculations
    calculator_tool.calculate("2 + 2")
    calculator_tool.calculate("3 * 4")
    
    # Clear history
    calculator_tool.clear_history()
    
    # Verify history is empty
    assert len(calculator_tool.get_history()) == 0

def test_calculator_precision(calculator_tool):
    """Test calculator precision with floating point numbers."""
    # Test addition with many decimal places
    result = calculator_tool.calculate("0.1 + 0.2")
    assert abs(result - 0.3) < 1e-10
    
    # Test multiplication with many decimal places
    result = calculator_tool.calculate("0.1 * 0.2")
    assert abs(result - 0.02) < 1e-10

def test_calculator_expression_validation(calculator_tool):
    """Test expression validation in calculator."""
    # Test valid expressions
    assert calculator_tool.validate_expression("2 + 2") is True
    assert calculator_tool.validate_expression("(2 + 3) * 4") is True
    assert calculator_tool.validate_expression("sqrt(16)") is True
    
    # Test invalid expressions
    assert calculator_tool.validate_expression("2 + + 3") is False
    assert calculator_tool.validate_expression("invalid(5)") is False
    assert calculator_tool.validate_expression("2 + ") is False

def test_calculator_performance(calculator_tool):
    """Test calculator performance with complex expressions."""
    import time
    
    # Test complex expression
    start_time = time.time()
    result = calculator_tool.calculate("(2 + 3) * (4 + 5) * (6 + 7)")
    end_time = time.time()
    
    assert result == 585  # (5 * 9 * 13)
    assert end_time - start_time < 0.1  # Should complete within 100ms 