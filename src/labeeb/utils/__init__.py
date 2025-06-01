"""
Utility functions for Labeeb.

This module provides various utility functions used throughout the application.
"""

from .platform_utils import (
    ensure_labeeb_directories,
    get_labeeb_base_dir,
    get_labeeb_log_dir,
    get_labeeb_data_dir,
    get_labeeb_cache_dir,
    get_labeeb_config_dir,
    get_labeeb_temp_dir,
    get_platform_info,
    is_windows,
    is_macos,
    is_linux,
    get_environment_variables,
    get_environment_variable,
    set_environment_variable,
    remove_environment_variable,
    get_current_user,
    get_home_directory
)

# Optional imports to make formatting utilities available directly
try:
    from .output_formatter import (
        EMOJI,
        format_header,
        format_table_row,
        format_box,
        format_status_line,
        format_list,
        create_divider,
    )
except ImportError:
    # Output formatter not available, ignore
    pass

__all__ = [
    "ensure_labeeb_directories",
    "get_labeeb_base_dir",
    "get_labeeb_log_dir",
    "get_labeeb_data_dir",
    "get_labeeb_cache_dir",
    "get_labeeb_config_dir",
    "get_labeeb_temp_dir",
    "get_platform_info",
    "is_windows",
    "is_macos",
    "is_linux",
    "get_environment_variables",
    "get_environment_variable",
    "set_environment_variable",
    "remove_environment_variable",
    "get_current_user",
    "get_home_directory"
]
