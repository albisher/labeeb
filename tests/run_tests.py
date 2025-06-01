"""
Test runner for Labeeb.

This module provides a test runner to execute all tests in the project.

---
description: Run all tests
endpoints: [run_all_tests]
inputs: []
outputs: [test_results]
dependencies: [pytest, pytest-cov]
auth: none
alwaysApply: false
---
"""

import os
import sys
import pytest
import logging
from datetime import datetime

# Add src to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from labeeb.utils.platform_utils import ensure_labeeb_directories

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/test_runner.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_all_tests():
    """Run all tests in the project."""
    try:
        # Ensure directories exist
        base_dir = ensure_labeeb_directories()
        
        # Create test results directory
        results_dir = os.path.join(base_dir, "tests", "results")
        os.makedirs(results_dir, exist_ok=True)
        
        # Generate test report filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(results_dir, f"test_report_{timestamp}.xml")
        coverage_file = os.path.join(results_dir, f"coverage_{timestamp}.xml")
        
        # Run tests with pytest
        args = [
            "--verbose",
            "--junitxml", report_file,
            "--cov", "labeeb",
            "--cov-report", f"xml:{coverage_file}",
            "--cov-report", "term-missing",
            "--capture=no",  # Show print statements
            "tests/"
        ]
        
        logger.info("Starting test run...")
        result = pytest.main(args)
        
        if result == 0:
            logger.info("All tests passed!")
        else:
            logger.error(f"Tests failed with exit code {result}")
            
        return result
        
    except Exception as e:
        error_msg = f"Error running tests: {e}"
        logger.error(error_msg)
        raise Exception(error_msg)

if __name__ == "__main__":
    run_all_tests() 