"""
Mac File System Handler for managing file operations.

---
description: Handles file system operations on macOS
endpoints: [mac_fs_handler]
inputs: [fs_command]
outputs: [fs_result]
dependencies: [os, shutil, logging]
auth: none
alwaysApply: true
---

- Handle file operations
- Manage directories
- Support file utilities
- Handle file errors
- Provide file status
"""

import os
import shutil
import logging
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class MacFSHandler:
    """Handles file system operations on macOS."""

    def __init__(self):
        """Initialize the Mac file system handler."""
        self._home_dir = str(Path.home())
        logger.info(f"Initialized file system handler with home directory: {self._home_dir}")

    def create_directory(self, path: str, parents: bool = True) -> bool:
        """
        Create a directory.

        Args:
            path: Directory path
            parents: Create parent directories if needed

        Returns:
            bool: True if successful
        """
        try:
            Path(path).mkdir(parents=parents, exist_ok=True)
            logger.info(f"Created directory: {path}")
            return True
        except Exception as e:
            logger.error(f"Error creating directory {path}: {str(e)}")
            return False

    def remove_directory(self, path: str, recursive: bool = False) -> bool:
        """
        Remove a directory.

        Args:
            path: Directory path
            recursive: Remove directory and contents

        Returns:
            bool: True if successful
        """
        try:
            if recursive:
                shutil.rmtree(path)
            else:
                os.rmdir(path)
            logger.info(f"Removed directory: {path}")
            return True
        except Exception as e:
            logger.error(f"Error removing directory {path}: {str(e)}")
            return False

    def create_file(self, path: str, content: str = "") -> bool:
        """
        Create a file.

        Args:
            path: File path
            content: File content

        Returns:
            bool: True if successful
        """
        try:
            with open(path, 'w') as f:
                f.write(content)
            logger.info(f"Created file: {path}")
            return True
        except Exception as e:
            logger.error(f"Error creating file {path}: {str(e)}")
            return False

    def remove_file(self, path: str) -> bool:
        """
        Remove a file.

        Args:
            path: File path

        Returns:
            bool: True if successful
        """
        try:
            os.remove(path)
            logger.info(f"Removed file: {path}")
            return True
        except Exception as e:
            logger.error(f"Error removing file {path}: {str(e)}")
            return False

    def copy_file(self, src: str, dst: str) -> bool:
        """
        Copy a file.

        Args:
            src: Source path
            dst: Destination path

        Returns:
            bool: True if successful
        """
        try:
            shutil.copy2(src, dst)
            logger.info(f"Copied file from {src} to {dst}")
            return True
        except Exception as e:
            logger.error(f"Error copying file from {src} to {dst}: {str(e)}")
            return False

    def move_file(self, src: str, dst: str) -> bool:
        """
        Move a file.

        Args:
            src: Source path
            dst: Destination path

        Returns:
            bool: True if successful
        """
        try:
            shutil.move(src, dst)
            logger.info(f"Moved file from {src} to {dst}")
            return True
        except Exception as e:
            logger.error(f"Error moving file from {src} to {dst}: {str(e)}")
            return False

    def get_file_info(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Get file information.

        Args:
            path: File path

        Returns:
            Optional[Dict[str, Any]]: File information
        """
        try:
            stat = os.stat(path)
            return {
                "size": stat.st_size,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "accessed": stat.st_atime,
                "mode": stat.st_mode,
                "is_dir": os.path.isdir(path),
                "is_file": os.path.isfile(path),
                "is_link": os.path.islink(path)
            }
        except Exception as e:
            logger.error(f"Error getting file info for {path}: {str(e)}")
            return None

    def list_directory(self, path: str) -> List[str]:
        """
        List directory contents.

        Args:
            path: Directory path

        Returns:
            List[str]: List of files and directories
        """
        try:
            return os.listdir(path)
        except Exception as e:
            logger.error(f"Error listing directory {path}: {str(e)}")
            return []

    def exists(self, path: str) -> bool:
        """
        Check if path exists.

        Args:
            path: Path to check

        Returns:
            bool: True if path exists
        """
        return os.path.exists(path)

    def is_file(self, path: str) -> bool:
        """
        Check if path is a file.

        Args:
            path: Path to check

        Returns:
            bool: True if path is a file
        """
        return os.path.isfile(path)

    def is_dir(self, path: str) -> bool:
        """
        Check if path is a directory.

        Args:
            path: Path to check

        Returns:
            bool: True if path is a directory
        """
        return os.path.isdir(path) 