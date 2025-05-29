# Input Control in Labeeb

**PyAutoGUI is the official and default technology for all screenshots, mouse, and keyboard automation in Labeeb. All input automation should use PyAutoGUI for cross-platform compatibility (Linux, macOS, Windows).**

## Overview

The input control module provides functions to programmatically control the mouse and keyboard using PyAutoGUI and other libraries. It allows Labeeb to perform automated input operations across different operating systems.

## Organization

The input control functionality follows a clear organization structure:

```
/src/labeeb/
    /platform_core/           # System files for platform-specific implementations
        /common/
            /input_control/
                base_handler.py      # Core interface definition
                mouse_keyboard_handler.py  # Core implementation
                __init__.py
        /ubuntu/
            /input_control/
                ubuntu_input_handler.py  # Ubuntu-specific implementation
                __init__.py
        /windows/
            /input_control/
                windows_input_handler.py  # Windows-specific implementation
                __init__.py
        /mac/
            /input_control/
                mac_input_handler.py  # macOS-specific implementation
                __init__.py
        /jetson/
            /input_control/
                jetson_input_handler.py  # Jetson-specific implementation
                __init__.py
    /setup/                  # Setup files for one-time initialization
        /input_control/
            input_setup.py   # Input control initialization
            device_setup.py  # Device detection and setup
    /tests/                  # Test files (development only)
        /input_control/
            test_handlers.py
            test_platforms.py
```

## File Naming Conventions

1. **System Files**: Core functionality files that are required for the system to operate
   - Located in `/src/labeeb/platform_core/`
   - Named descriptively (e.g., `ubuntu_input_handler.py`, `mac_input_handler.py`)
   - No "test" in production filenames

2. **Setup Files**: One-time initialization or health check files
   - Located in `/src/labeeb/setup/`
   - Named with `_setup.py` suffix
   - Run during initial setup or health checks

3. **Test Files**: Development and testing files
   - Located in `/tests/`
   - Named with `test_` prefix
   - Not included in production builds

## Usage

### Recommended Import Method

```python
from labeeb.platform_core.platform_utils import get_input_handler

# Get the platform-specific handler automatically
handler = get_input_handler()

# Use the handler
handler.move_mouse(100, 100)
handler.click_mouse()
handler.type_text("Hello, world!")
```

### Alternative Import Methods

```python
# Method 1: Import specific implementation (if you know the platform)
from labeeb.platform_core.ubuntu.input_control import UbuntuInputHandler
handler = UbuntuInputHandler()

# Method 2: Legacy import (backwards compatibility)
from labeeb.platform_core.common.input_control import MouseKeyboardHandler
handler = MouseKeyboardHandler()
```

## Features

- **Cross-platform support**: Works on Windows, macOS, Ubuntu, and Jetson platforms
- **Simulation mode**: Works in environments without display access
- **Automatic platform detection**: Selects the appropriate implementation for the current platform
- **Backward compatibility**: Legacy code continues to work without modifications

## Simulation Mode

When running in an environment without a display (such as a headless server or Docker container), the handlers automatically fall back to simulation mode. In this mode:

- Mouse movements are tracked internally but not actually performed
- Screen size defaults to a reasonable value (1920x1080)
- All operations are logged but not actually executed

To force simulation mode for testing:

```python
import os
os.environ['DISPLAY'] = ''  # Set before importing the handler
from labeeb.platform_core.platform_utils import get_input_handler
```

## Available Methods

All input handlers implement the following methods:

- `get_mouse_position()`: Get the current mouse position
- `get_screen_size()`: Get the screen size