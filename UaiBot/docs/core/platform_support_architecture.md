# Labeeb Platform Support Architecture

## Overview

Labeeb is designed to work seamlessly across multiple platforms, including:

- **macOS** (both Intel and Apple Silicon)
- **Ubuntu** (and other Linux distributions)
- **Jetson** Nano (ARM-based embedded Linux)
- **Windows** (basic support)

This document explains the architecture that enables platform-specific functionality while maintaining a consistent user experience.

## Architecture

### Platform Detection

Platform detection is handled by the `platform_factory.py` module in `src/labeeb/platform_services/`, which identifies the current platform and maps it to the appropriate handler directory. The detection logic considers:

- Operating system (via `sys.platform`)
- CPU architecture (via `platform.machine()`)
- Special cases like Jetson hardware (by checking device tree)

### Platform Manager

The platform factory and service modules serve as the central coordinator for platform-specific functionality:

1. **Initialization**: Detects the platform and initializes appropriate handlers
2. **Handler Access**: Provides access to platform-specific handlers through getter methods
3. **Cleanup**: Ensures proper resource cleanup when shutting down

### Platform-Specific Modules

Each supported platform has its own directory under `src/labeeb/platform_services/`:

```
src/labeeb/platform_services/
├── common/            # Common implementations and base classes
├── macos/             # macOS specific implementations
├── linux/             # Linux specific implementations
├── windows/           # Windows specific implementations
├── platform_factory.py
```

### Handler Types

Labeeb provides several types of platform-specific handlers:

1. **Audio Handler**: For platform-specific audio recording and playback
2. **USB Handler**: For USB device detection and interaction
3. **Input Handler**: For mouse and keyboard control

### Fallback Mechanism

If a platform-specific implementation is not available, Labeeb will:

1. First try to load the specific platform implementation
2. If not available, fall back to the common implementation
3. If neither is available, gracefully degrade functionality

### Simulation Mode

For headless environments or when hardware access is not available, handlers can run in simulation mode:

- Mouse movements are tracked but not actually performed
- Audio is simulated rather than actually recorded/played
- USB operations are logged but not executed

## Implementation Details

### Handler Base Classes

Each handler type has a base class that defines the interface:

- `BaseAudioHandler`: For audio operations
- `BaseUSBHandler`: For USB operations
- `BaseInputHandler`: For input control

### Platform Utilities

The platform factory module provides functions to obtain the appropriate handler for the current platform:

- `get_audio_handler()`
- `get_usb_handler()`
- `get_input_handler()`

## Adding Support for a New Platform

To add support for a new platform:

1. Create a new directory under `src/labeeb/platform_services/` (e.g., `src/labeeb/platform_services/new_platform/`)
2. Implement the necessary handlers (audio_handler.py, usb_handler.py, input_control.py)
3. Update `platform_factory.py` to recognize the new platform
4. Add any special initialization or cleanup logic as needed

## Testing Platform Support

The `tests/unit/labeeb/platform_services/` or `tests/integration/labeeb/platform_services/` directories can be used to verify that platform detection and handler initialization work correctly on your system.

## Test File Structure

All test files should be located in the `tests/` directory, with platform-specific tests in `tests/unit/labeeb/platform_services/` or `tests/integration/labeeb/platform_services/` and test artifacts in `tests/test_files/` for better organization and clarity.
