import logging
import json
import datetime
from typing import Dict, Any, List, Optional, Tuple
import subprocess

class Utils:
    def __init__(self):
        # Set up logging
        self.logger = logging.getLogger('Labeeb')
        self.logger.setLevel(logging.INFO)  # Default to INFO
        
        # Create a custom handler to capture log records
        self.log_handler = logging.StreamHandler()
        self.log_handler.setLevel(logging.INFO)  # Default to INFO
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.log_handler.setFormatter(formatter)
        self.logger.addHandler(self.log_handler)
        
        # Configuration
        self.config = {
            "version": "1.0.0",
            "debug_mode": False,
            "log_level": "INFO"
        }
        
        # Error log
        self.error_log = []
        
    def get_help(self) -> Dict[str, Any]:
        """Get help information."""
        return {
            "status": "success",
            "help": {
                "file_commands": [
                    "create file <filename>",
                    "read file <filename>",
                    "write file <filename> with content <content>",
                    "append to file <filename> with content <content>",
                    "delete file <filename>",
                    "list files",
                    "search files for <pattern>"
                ],
                "system_commands": [
                    "show system status",
                    "show cpu info",
                    "show memory info",
                    "show disk info",
                    "show network info",
                    "show process info",
                    "show system logs"
                ],
                "language_commands": [
                    "set language to <language>",
                    "detect language of <text>",
                    "translate <text> to <language>",
                    "show supported languages",
                    "set default language to <language>"
                ],
                "utility_commands": [
                    "show help",
                    "show version",
                    "show status",
                    "show configuration",
                    "show logs",
                    "enable debug",
                    "disable debug",
                    "show errors"
                ]
            }
        }
        
    def get_version(self) -> Dict[str, Any]:
        """Get version information."""
        return {
            "status": "success",
            "version": self.config["version"]
        }
        
    def get_status(self) -> Dict[str, Any]:
        """Get system status."""
        return {
            "status": "success",
            "system_status": {
                "version": self.config["version"],
                "debug_mode": self.config["debug_mode"],
                "log_level": self.config["log_level"],
                "timestamp": datetime.datetime.now().isoformat()
            }
        }
        
    def get_configuration(self) -> Dict[str, Any]:
        """Get configuration."""
        return {
            "status": "success",
            "configuration": self.config
        }
        
    def get_logs(self) -> Dict[str, Any]:
        """Get system logs."""
        return {
            "status": "success",
            "logs": [
                {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "level": "INFO",
                    "message": "System initialized"
                }
            ]
        }
        
    def set_debug_mode(self, enabled: bool) -> Dict[str, Any]:
        """Set debug mode."""
        self.config["debug_mode"] = enabled
        self.config["log_level"] = "DEBUG" if enabled else "INFO"
        self.logger.setLevel(logging.DEBUG if enabled else logging.INFO)
        self.log_handler.setLevel(logging.DEBUG if enabled else logging.INFO)
        
        return {
            "status": "success",
            "debug_mode": enabled,
            "message": f"Debug mode {'enabled' if enabled else 'disabled'}"
        }
        
    def get_errors(self) -> Dict[str, Any]:
        """Get error log."""
        return {
            "status": "success",
            "errors": self.error_log
        }
        
    def log_error(self, error: str) -> None:
        """Log an error."""
        self.error_log.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "error": error
        })
        self.logger.error(error)
        
    def execute_command(self, command: str) -> Dict[str, Any]:
        """Execute a utility command."""
        command_lower = command.lower()
        
        # Help command
        if any(word in command_lower for word in ["show help", "get help", "help"]):
            return self.get_help()
            
        # Version command
        elif any(word in command_lower for word in ["show version", "get version", "version"]):
            return self.get_version()
            
        # Status command
        elif any(word in command_lower for word in ["show status", "get status", "status"]):
            return self.get_status()
            
        # Configuration command
        elif any(word in command_lower for word in ["show configuration", "get configuration", "config"]):
            return self.get_configuration()
            
        # Logs command
        elif any(word in command_lower for word in ["show logs", "get logs", "logs"]):
            return self.get_logs()
            
        # Debug commands
        elif any(word in command_lower for word in ["enable debug", "turn on debug"]):
            return self.set_debug_mode(True)
        elif any(word in command_lower for word in ["disable debug", "turn off debug"]):
            return self.set_debug_mode(False)
            
        # Error command
        elif any(word in command_lower for word in ["show errors", "get errors", "errors"]):
            return self.get_errors()
            
        # Arabic commands
        elif "عرض المساعدة" in command:
            return self.get_help()
        elif "عرض الإصدار" in command:
            return self.get_version()
        elif "عرض الحالة" in command:
            return self.get_status()
        elif "عرض التكوين" in command:
            return self.get_configuration()
        elif "عرض السجلات" in command:
            return self.get_logs()
        elif "تفعيل التصحيح" in command:
            return self.set_debug_mode(True)
        elif "تعطيل التصحيح" in command:
            return self.set_debug_mode(False)
        elif "عرض الأخطاء" in command:
            return self.get_errors()
            
        return {"status": "error", "message": "Unknown utility command"}

def run_command(command: str, shell: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result.
    
    Args:
        command: Command to run
        shell: Whether to run in shell mode
        
    Returns:
        subprocess.CompletedProcess: Command execution result
    """
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            check=False
        )
        return result
    except Exception as e:
        logger.error(f"Error running command '{command}': {e}")
        return subprocess.CompletedProcess(
            command,
            returncode=1,
            stdout="",
            stderr=str(e)
        )

def get_command_output(command: str, shell: bool = True) -> Tuple[int, str, str]:
    """Run a command and return its output.
    
    Args:
        command: Command to run
        shell: Whether to run in shell mode
        
    Returns:
        Tuple[int, str, str]: (return code, stdout, stderr)
    """
    result = run_command(command, shell)
    return result.returncode, result.stdout, result.stderr

def run_command_with_timeout(
    command: str,
    timeout: int,
    shell: bool = True
) -> Optional[subprocess.CompletedProcess]:
    """Run a command with a timeout.
    
    Args:
        command: Command to run
        timeout: Timeout in seconds
        shell: Whether to run in shell mode
        
    Returns:
        Optional[subprocess.CompletedProcess]: Command result or None if timed out
    """
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False
        )
        return result
    except subprocess.TimeoutExpired:
        logger.error(f"Command '{command}' timed out after {timeout} seconds")
        return None
    except Exception as e:
        logger.error(f"Error running command '{command}': {e}")
        return None

def run_commands_parallel(
    commands: List[str],
    shell: bool = True
) -> List[subprocess.CompletedProcess]:
    """Run multiple commands in parallel.
    
    Args:
        commands: List of commands to run
        shell: Whether to run in shell mode
        
    Returns:
        List[subprocess.CompletedProcess]: List of command results
    """
    processes = []
    results = []
    
    # Start all processes
    for cmd in commands:
        try:
            process = subprocess.Popen(
                cmd,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            processes.append(process)
        except Exception as e:
            logger.error(f"Error starting command '{cmd}': {e}")
            results.append(
                subprocess.CompletedProcess(
                    cmd,
                    returncode=1,
                    stdout="",
                    stderr=str(e)
                )
            )
    
    # Wait for all processes to complete
    for process in processes:
        try:
            stdout, stderr = process.communicate()
            results.append(
                subprocess.CompletedProcess(
                    process.args,
                    process.returncode,
                    stdout,
                    stderr
                )
            )
        except Exception as e:
            logger.error(f"Error waiting for process: {e}")
            results.append(
                subprocess.CompletedProcess(
                    process.args,
                    1,
                    "",
                    str(e)
                )
            )
    
    return results 