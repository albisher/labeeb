# Labeeb Project TODO List

## Outstanding TODOs (Unified Checklist)

### [ ] Imports & File Moves
- [ ] Update all imports referencing `config/output_paths.py` after move from `src/labeeb/config` to `config/`.
- [ ] Review and delete `config/output_paths.py` if it is empty and not needed.

### [ ] Platform/Core Tools (Implementation)
- [ ] Implement `src/labeeb/core/platform_core/mouse_control_tool.py`.
- [ ] Implement `src/labeeb/core/platform_core/network_tool.py`.
- [ ] Implement `src/labeeb/core/platform_core/mouse.py`.
- [ ] Implement `src/labeeb/core/platform_core/usb_detector.py`.
- [ ] Implement `src/labeeb/core/platform_core/window_control_tool.py`.
- [ ] Implement `src/labeeb/core/platform_core/session_manager.py`.
- [ ] Implement `src/labeeb/core/platform_core/browser_controller.py`.

### [ ] Platform/Core Handlers (Enhancements)
- [ ] Implement input device detection in `src/labeeb/core/platform_core/handlers/windows/audio_handler.py`.
- [ ] Implement RTL text detection and handling in captured image in `src/labeeb/core/platform_core/handlers/mac/display_handler.py`.
- [ ] Implement hotkey registration in `src/labeeb/core/platform_core/handlers/mac/input_handler.py`.
- [ ] Implement hotkey unregistration in `src/labeeb/core/platform_core/handlers/mac/input_handler.py`.
- [ ] Implement supported keys list in `src/labeeb/core/platform_core/handlers/mac/input_handler.py`.
- [ ] Implement platform-specific cleanup in `src/labeeb/core/platform_core/handlers/mac/input_handler.py`.

### [ ] Platform/Core System Tools (Enhancements)
- [ ] Use OCR to extract weather information from screenshot in `src/labeeb/core/platform_core/system_tools.py`.

### [ ] Documentation
- [ ] Add usage example to each tool documentation in `docs/features/tools/` (see all `# TODO: Add usage example` lines).

### [ ] Dependencies & Documentation
- [x] Minimize dependencies in requirements.txt and setup.py to only those actually used.
- [x] Update documentation to clarify minimal vs. dev dependencies and installation instructions.
- [ ] Periodically review dependencies for minimalism and compliance with architecture rules.

### [ ] Critical Import Path Fixes
- [ ] Fix all incorrect imports from `labeeb.platform_services` to `labeeb.services.platform_services` throughout the codebase. This is required for platform-specific features (e.g., screenshot, audio, system info) to work and is currently blocking command testing.

### [ ] Platform/Core Handlers (Implementation)
- [ ] Implement `src/labeeb/core/platform_core/mac/shell_handler.py` (MacShellHandler) - Required for basic command execution.
- [ ] Review and implement other missing platform-specific handlers in `src/labeeb/core/platform_core/mac/`.

## Weather Agent Implementation
- [ ] Fix BaseAgentTool Import Issue
  - [ ] Check `src/labeeb/tools/base_tool.py` and implement `BaseAgentTool` class
  - [ ] Or update `src/labeeb/agents/labeeb_agent.py` to use correct import

- [ ] Environment Setup
  - [ ] Create `.env` file in project root
  - [ ] Add `WEATHER_API_KEY=your_api_key_here` to `.env`

- [ ] Weather Agent Enhancements
  - [ ] Add Arabic language support in `WeatherAgent`
  - [ ] Improve city extraction for better natural language understanding
  - [ ] Add error handling for API rate limits
  - [ ] Add caching for API responses

- [ ] Testing
  - [ ] Test English weather queries
  - [ ] Test Arabic weather queries
  - [ ] Test weather forecasts
  - [ ] Test error handling
  - [ ] Test caching mechanism

- [ ] Documentation
  - [ ] Add docstrings for all methods
  - [ ] Add usage examples
  - [ ] Document configuration options
  - [ ] Add API documentation

- [ ] Integration
  - [ ] Integrate with main command processing system
  - [ ] Add support for weather alerts
  - [ ] Add support for weather history
  - [ ] Add support for multiple weather units (metric/imperial)

- [ ] Error Handling
  - [ ] Add proper error messages for API failures
  - [ ] Add retry mechanism for failed API calls
  - [ ] Add validation for city names
  - [ ] Add proper logging

- [ ] Performance
  - [ ] Optimize caching strategy
  - [ ] Add request rate limiting
  - [ ] Add response compression
  - [ ] Add connection pooling

- [ ] Security
  - [ ] Secure API key storage
  - [ ] Add request validation
  - [ ] Add response sanitization
  - [ ] Add proper error handling for security issues

- [ ] Monitoring
  - [ ] Add usage metrics
  - [ ] Add performance monitoring
  - [ ] Add error tracking
  - [ ] Add API usage tracking

---

All TODOs are now tracked in this unified checklist. Remove all inline TODOs from code and documentation after adding them here. Mark each as complete with [x] when done.
