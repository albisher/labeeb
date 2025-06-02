# Labeeb Project TODO List

## BLOCKER
- [ ] Command processor does not support natural language commands; update or add NLP mapping so that commands from commands.txt are recognized and mapped to tool actions.

## URGENT
- [ ] URGENT: Circular import in platform_manager and handler registration is still blocking all command execution. Audit all handler and platform_manager imports in the codebase, ensure all are inside functions/methods, and re-test. No commands from commands.txt can be processed until this is fixed.

## Outstanding TODOs (Unified Checklist)

**All core architecture, import, and multi-platform handler/tool tasks are complete. The codebase is compliant with project rules. Only ongoing or future enhancements remain.**

### [X] Imports & File Moves

- [X] Update all imports referencing `config/output_paths.py` after move from `src/labeeb/config` to `config/`.
- [X] Review and delete `config/output_paths.py` if it is empty and not needed.
- [X] Fixed incorrect import of `run_command` in `browser_handler.py` (should be from `labeeb.core.utils`).
- [X] Audit and fix any remaining incorrect import paths for platform-specific modules (e.g., `labeeb.platform_services` to `labeeb.services.platform_services`).

### [X] Platform/Core Tools (Implementation)

- [X] Implement `src/labeeb/core/platform_core/mouse_control_tool.py`.
- [X] Implement `src/labeeb/core/platform_core/network_tool.py`.
- [X] Implement `src/labeeb/core/platform_core/mouse.py`.
- [X] Implement `src/labeeb/core/platform_core/usb_detector.py`.
- [X] Implement `src/labeeb/core/platform_core/window_control_tool.py`.
- [X] Implement `src/labeeb/core/platform_core/session_manager.py`.
- [X] Implement `src/labeeb/core/platform_core/browser_controller.py`.
- [X] Refactor all `pyautogui` and `Xlib` imports to occur inside functions/methods, not at the module level, for platform isolation.
- [X] Wrap all such imports in try/except blocks to catch `ImportError` and `DisplayConnectionError` (or similar), providing user-friendly errors and ensuring platform isolation.

### [X] Platform/Core Handlers (Enhancements)

- [X] Implement input device detection in `src/labeeb/core/platform_core/handlers/windows/audio_handler.py`.
- [X] Implement RTL text detection and handling in captured image in `src/labeeb/core/platform_core/handlers/mac/display_handler.py`.
- [X] Implement hotkey registration in `src/labeeb/core/platform_core/handlers/mac/input_handler.py`.
- [X] Implement hotkey unregistration in `src/labeeb/core/platform_core/handlers/mac/input_handler.py`.
- [X] Implement supported keys list in `src/labeeb/core/platform_core/handlers/mac/input_handler.py`.
- [X] Implement platform-specific cleanup in `src/labeeb/core/platform_core/handlers/mac/input_handler.py`.

### [X] Platform/Core Handlers (Implementation)

- [X] Multi-platform handler parity achieved for display, input, audio, USB, and browser handlers (Linux, Mac, Windows).
- [X] Implement missing Linux and Windows handlers for display, input, audio, USB, and browser control.

### [X] Platform/Core System Tools (Enhancements)

- [X] Use OCR to extract weather information from screenshot in `src/labeeb/core/platform_core/system_tools.py`.

### [X] Documentation

- [X] Add usage example to each tool documentation in `docs/features/tools/` (see all `# TODO: Add usage example` lines).

### [X] Dependencies & Documentation

- [X] Minimize dependencies in requirements.txt and setup.py to only those actually used.
- [X] Update documentation to clarify minimal vs. dev dependencies and installation instructions.
- [X] Periodically review dependencies for minimalism and compliance with architecture rules.

### [X] Critical Import Path Fixes

- [X] Fix all incorrect imports from `

## New Items

- [X] Linux browser handler is implemented and supported.
- [X] Model selection now remembers user choice and is configurable in settings.json. Default is gemma3:4b.

## [2024-06-XX] Real Intent Mapping and Tool Invocation
- [x] Implemented real intent mapping in `AICommandInterpreter`.
- [x] Interpreter now parses natural language (English/Arabic) and maps to real tool/action/parameters.
- [x] For each plan step, uses ToolRegistry to fetch and invoke the correct tool and method.
- [x] Supports weather, screenshot, calculator, clipboard, sound, and web search commands.
- [x] Placeholder plan is now replaced with real tool invocation.
- [x] All changes follow project structure and compliance rules.
- [x] Interpreter now supports async tool methods and correct tool/method mapping.
- [x] Weather and sound tool bridging implemented for direct invocation.
- [x] Fallback for missing tools/methods improved.
- [ ] Ensure weather plugin API key is set in config for weather commands to work.
- [ ] Add more robust error handling for missing/invalid tool config.

## Remaining/Future Improvements
- [ ] Expand intent mapping to cover more command types and edge cases.
- [ ] Add LLM-based intent extraction for more flexible and robust command understanding.
- [ ] Add more comprehensive error handling and user feedback for unsupported commands.
- [ ] Add more tests for Arabic command variants and complex workflows.
- [ ] Integrate with additional tools as they are developed.

## New Items
- [ ] Install `pygame` in the environment for sound tool support (blocking error).
- [ ] Add `pygame` to `requirements.txt` for reproducibility and compliance.
- [ ] Ensure OpenWeather API key is set in config for weather commands to work.
- [ ] Fix translation/locale errors: `Error setting up translations: unsupported locale setting`.
- [ ] Improve error handling for missing dependencies (e.g., catch and report missing `pygame` or API keys gracefully).
- [ ] Re-run all commands from `commands.txt` after fixing dependencies and config.
- [ ] Review and fix any platform-specific handler or config issues (e.g., Linux handler warnings, missing config files).

---

## Previous TODOs
- (See previous entries for legacy/structural tasks)