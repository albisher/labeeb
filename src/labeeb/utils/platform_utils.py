"""
Platform utilities for the system.

---
description: Utilities for platform-specific operations
endpoints: [platform_utils]
inputs: []
outputs: []
dependencies: []
auth: none
alwaysApply: false
---
"""

import os
import sys
import logging
from pathlib import Path
from typing import List, Optional

# Configure logging
logger = logging.getLogger(__name__)

def ensure_labeeb_directories() -> Path:
    """Ensure all required Labeeb directories exist and return the base directory."""
    try:
        # Get the base directory
        base_dir = get_labeeb_base_dir()
        
        # Create required directories
        directories = [
            "logs",
            "data",
            "cache",
            "config",
            "temp"
        ]
        
        for directory in directories:
            dir_path = base_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured directory exists: {dir_path}")
            
        return base_dir
    except Exception as e:
        logger.error(f"Error ensuring Labeeb directories: {str(e)}")
        raise

def get_labeeb_base_dir() -> Path:
    """Get the base directory for Labeeb.
    
    Returns:
        Path object pointing to the Labeeb base directory
    """
    # Try to get from environment variable
    base_dir = os.getenv("LABEEB_BASE_DIR")
    if base_dir:
        return Path(base_dir)
    
    # Default to user's home directory
    if sys.platform == "win32":
        base_dir = os.path.join(os.environ["USERPROFILE"], "Labeeb")
    else:
        base_dir = os.path.join(os.path.expanduser("~"), "Labeeb")
    
    return Path(base_dir)

def get_labeeb_log_dir() -> Path:
    """Get the log directory for Labeeb.
    
    Returns:
        Path object pointing to the Labeeb log directory
    """
    return get_labeeb_base_dir() / "logs"

def get_labeeb_data_dir() -> Path:
    """Get the data directory for Labeeb.
    
    Returns:
        Path object pointing to the Labeeb data directory
    """
    return get_labeeb_base_dir() / "data"

def get_labeeb_cache_dir() -> Path:
    """Get the cache directory for Labeeb.
    
    Returns:
        Path object pointing to the Labeeb cache directory
    """
    return get_labeeb_base_dir() / "cache"

def get_labeeb_config_dir() -> Path:
    """Get the config directory for Labeeb.
    
    Returns:
        Path object pointing to the Labeeb config directory
    """
    return get_labeeb_base_dir() / "config"

def get_labeeb_temp_dir() -> Path:
    """Get the temp directory for Labeeb.
    
    Returns:
        Path object pointing to the Labeeb temp directory
    """
    return get_labeeb_base_dir() / "temp"

def get_platform_info() -> dict:
    """Get information about the current platform.
    
    Returns:
        Dict containing platform information
    """
    return {
        "system": sys.platform,
        "python_version": sys.version,
        "python_implementation": sys.implementation.name,
        "machine": sys.machine,
        "processor": sys.processor,
        "base_dir": str(get_labeeb_base_dir()),
        "log_dir": str(get_labeeb_log_dir()),
        "data_dir": str(get_labeeb_data_dir()),
        "cache_dir": str(get_labeeb_cache_dir()),
        "config_dir": str(get_labeeb_config_dir()),
        "temp_dir": str(get_labeeb_temp_dir())
    }

def is_windows() -> bool:
    """Check if running on Windows.
    
    Returns:
        True if running on Windows, False otherwise
    """
    return sys.platform == "win32"

def is_macos() -> bool:
    """Check if running on macOS.
    
    Returns:
        True if running on macOS, False otherwise
    """
    return sys.platform == "darwin"

def is_linux() -> bool:
    """Check if running on Linux.
    
    Returns:
        True if running on Linux, False otherwise
    """
    return sys.platform.startswith("linux")

def get_environment_variables() -> dict:
    """Get all environment variables.
    
    Returns:
        Dict containing environment variables
    """
    return dict(os.environ)

def get_environment_variable(name: str, default: Optional[str] = None) -> Optional[str]:
    """Get an environment variable.
    
    Args:
        name: Name of the environment variable
        default: Default value if not found
        
    Returns:
        Value of the environment variable or default
    """
    return os.getenv(name, default)

def set_environment_variable(name: str, value: str) -> None:
    """Set an environment variable.
    
    Args:
        name: Name of the environment variable
        value: Value to set
    """
    os.environ[name] = value

def remove_environment_variable(name: str) -> None:
    """Remove an environment variable.
    
    Args:
        name: Name of the environment variable to remove
    """
    os.environ.pop(name, None)

def get_current_user() -> str:
    """Get the current user.
    
    Returns:
        Current username
    """
    if is_windows():
        return os.environ["USERNAME"]
    return os.environ["USER"]

def get_home_directory() -> Path:
    """Get the home directory.
    
    Returns:
        Path object pointing to the home directory
    """
    if is_windows():
        return Path(os.environ["USERPROFILE"])
    return Path(os.path.expanduser("~"))

def get_current_directory() -> Path:
    """Get the current working directory.
    
    Returns:
        Path object pointing to the current working directory
    """
    return Path(os.getcwd())

def change_directory(path: str) -> None:
    """Change the current working directory.
    
    Args:
        path: Path to change to
    """
    os.chdir(path)

def list_directory(path: str) -> List[str]:
    """List contents of a directory.
    
    Args:
        path: Path to list
        
    Returns:
        List of directory contents
    """
    return os.listdir(path)

def create_directory(path: str) -> None:
    """Create a directory.
    
    Args:
        path: Path to create
    """
    os.makedirs(path, exist_ok=True)

def remove_directory(path: str) -> None:
    """Remove a directory.
    
    Args:
        path: Path to remove
    """
    os.rmdir(path)

def remove_file(path: str) -> None:
    """Remove a file.
    
    Args:
        path: Path to remove
    """
    os.remove(path)

def file_exists(path: str) -> bool:
    """Check if a file exists.
    
    Args:
        path: Path to check
        
    Returns:
        True if file exists, False otherwise
    """
    return os.path.isfile(path)

def directory_exists(path: str) -> bool:
    """Check if a directory exists.
    
    Args:
        path: Path to check
        
    Returns:
        True if directory exists, False otherwise
    """
    return os.path.isdir(path)

def get_file_size(path: str) -> int:
    """Get the size of a file.
    
    Args:
        path: Path to file
        
    Returns:
        Size of file in bytes
    """
    return os.path.getsize(path)

def get_file_modified_time(path: str) -> float:
    """Get the last modified time of a file.
    
    Args:
        path: Path to file
        
    Returns:
        Last modified time as timestamp
    """
    return os.path.getmtime(path)

def get_file_created_time(path: str) -> float:
    """Get the creation time of a file.
    
    Args:
        path: Path to file
        
    Returns:
        Creation time as timestamp
    """
    return os.path.getctime(path)

def get_file_permissions(path: str) -> int:
    """Get the permissions of a file.
    
    Args:
        path: Path to file
        
    Returns:
        File permissions as integer
    """
    return os.stat(path).st_mode

def set_file_permissions(path: str, mode: int) -> None:
    """Set the permissions of a file.
    
    Args:
        path: Path to file
        mode: Permissions to set
    """
    os.chmod(path, mode)

def get_file_owner(path: str) -> str:
    """Get the owner of a file.
    
    Args:
        path: Path to file
        
    Returns:
        Owner username
    """
    return os.stat(path).st_uid

def get_file_group(path: str) -> str:
    """Get the group of a file.
    
    Args:
        path: Path to file
        
    Returns:
        Group name
    """
    return os.stat(path).st_gid

def get_file_extension(path: str) -> str:
    """Get the extension of a file.
    
    Args:
        path: Path to file
        
    Returns:
        File extension
    """
    return os.path.splitext(path)[1]

def get_file_name(path: str) -> str:
    """Get the name of a file.
    
    Args:
        path: Path to file
        
    Returns:
        File name
    """
    return os.path.basename(path)

def get_directory_name(path: str) -> str:
    """Get the name of a directory.
    
    Args:
        path: Path to directory
        
    Returns:
        Directory name
    """
    return os.path.dirname(path)

def get_absolute_path(path: str) -> str:
    """Get the absolute path.
    
    Args:
        path: Path to convert
        
    Returns:
        Absolute path
    """
    return os.path.abspath(path)

def get_relative_path(path: str, start: str) -> str:
    """Get the relative path.
    
    Args:
        path: Path to convert
        start: Start directory
        
    Returns:
        Relative path
    """
    return os.path.relpath(path, start)

def join_paths(*paths: str) -> str:
    """Join paths together.
    
    Args:
        *paths: Paths to join
        
    Returns:
        Joined path
    """
    return os.path.join(*paths)

def normalize_path(path: str) -> str:
    """Normalize a path.
    
    Args:
        path: Path to normalize
        
    Returns:
        Normalized path
    """
    return os.path.normpath(path)

def expand_path(path: str) -> str:
    """Expand a path.
    
    Args:
        path: Path to expand
        
    Returns:
        Expanded path
    """
    return os.path.expanduser(os.path.expandvars(path))
