# Labeeb Project TODO List

## BLOCKER
- [ ] Fix command processor to support natural language commands and update/add NLP mapping
- [ ] Fix initialization errors for MacDisplayHandler, MacAudioHandler, MacUSBHandler, MacInputHandler (unexpected keyword argument 'config')
- [ ] Fix locale settings error: "unsupported locale setting"
- [ ] Fix command processor to return actual results for basic commands (calculator, weather)
- [ ] Fix Arabic command processing and RTL support
- [ ] Fix weather command processing to actually fetch and return weather data
- [ ] Fix shell handler initialization to properly set environment variables
- [ ] Fix browser command processing to actually open and navigate browsers
- [ ] Fix MacBrowserHandler initialization to properly detect and control browsers

## URGENT
- [ ] Fix circular import issue in platform_manager and handler registration (blocking all command execution)
- [ ] Audit all handler and platform_manager imports in codebase to ensure they are inside functions/methods
- [ ] Fix MacBrowserHandler initialization to properly handle browser detection
- [ ] Fix MacInputHandler initialization to handle AXIsProcessTrusted properly
- [ ] Fix MacNetHandler and MacFSHandler warnings on Darwin platform
- [ ] Fix browser detection and control on macOS
- [ ] Fix browser navigation and URL handling

## Outstanding TODOs
- [ ] All core architecture and import tasks are complete
- [ ] Only ongoing enhancements remain

## New Items
- [ ] Implement Linux browser handler
- [ ] Model selection now remembers user choice in settings.json
- [ ] Add weather API integration and data fetching
- [ ] Add proper error handling for weather command failures
- [ ] Add weather data caching to prevent excessive API calls
- [ ] Add weather command response formatting
- [ ] Add browser command specific error handling
- [ ] Add browser command response validation
- [ ] Add browser command logging
- [ ] Add browser command execution validation

## Platform-Specific Handler Fixes
- [ ] Fix MacDisplayHandler config parameter issue
- [ ] Fix MacAudioHandler config parameter issue
- [ ] Fix MacUSBHandler config parameter issue
- [ ] Fix MacInputHandler config parameter issue
- [ ] Fix MacBrowserHandler support warning
- [ ] Fix MacNetHandler support warning
- [ ] Fix MacFSHandler support warning
- [ ] Fix MacBrowserHandler browser detection
- [ ] Fix MacBrowserHandler browser control
- [ ] Fix MacBrowserHandler URL handling

## Command Processing Improvements
- [ ] Add better error handling for command execution
- [ ] Add user feedback for command status
- [ ] Add command logging
- [ ] Add command execution validation
- [ ] Add weather command specific error handling
- [ ] Add weather command response validation
- [ ] Add browser command specific error handling
- [ ] Add browser command response validation
- [ ] Add browser command execution validation

## Testing and Validation
- [ ] Add unit tests for weather command
- [ ] Add integration tests for weather API
- [ ] Add platform-specific test suite
- [ ] Add weather command response validation tests
- [ ] Add unit tests for browser command
- [ ] Add integration tests for browser control
- [ ] Add browser command response validation tests

## Documentation Updates
- [ ] Add platform-specific setup guides
- [ ] Add command reference documentation
- [ ] Add troubleshooting guides
- [ ] Add weather API integration documentation
- [ ] Add weather command usage examples
- [ ] Add browser command usage examples
- [ ] Add browser control documentation
- [ ] Add browser navigation documentation

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

## Platform-Specific Handler Fixes
- [ ] Fix MacDisplayHandler config parameter issue
- [ ] Fix MacAudioHandler config parameter issue
- [ ] Fix MacUSBHandler config parameter issue
- [ ] Fix MacInputHandler AXIsProcessTrusted error
- [ ] Fix MacBrowserHandler Darwin support
- [ ] Fix MacNetHandler Darwin support
- [ ] Fix MacFSHandler Darwin support
- [ ] Fix shell handler environment variable setting

## Command Processing Improvements
- [ ] Add proper error handling for unsupported commands
- [ ] Add user feedback for command execution status
- [ ] Add command execution logging
- [ ] Add command result validation
- [ ] Add command timeout handling
- [ ] Add command cancellation support
- [ ] Fix command processor not returning actual results
- [ ] Add proper tool action execution
- [ ] Add command result formatting
- [ ] Add command execution progress feedback
- [ ] Fix Arabic command processing
- [ ] Add RTL text support
- [ ] Add Arabic number handling
- [ ] Add Arabic command mapping
- [ ] Fix speech command processing
- [ ] Add audio file handling
- [ ] Add speech recognition support
- [ ] Add text-to-speech support

## Testing and Validation
- [ ] Add unit tests for all handlers
- [ ] Add integration tests for command processing
- [ ] Add platform-specific test suites
- [ ] Add command execution test suite
- [ ] Add error handling test suite
- [ ] Add performance test suite
- [ ] Add command result validation tests
- [ ] Add tool action execution tests
- [ ] Add command format tests
- [ ] Add Arabic command tests
- [ ] Add RTL text tests
- [ ] Add Arabic number tests
- [ ] Add speech command tests
- [ ] Add audio file tests
- [ ] Add speech recognition tests
- [ ] Add text-to-speech tests

## Documentation Updates
- [ ] Add platform-specific setup guides
- [ ] Add command reference documentation
- [ ] Add troubleshooting guide
- [ ] Add API documentation
- [ ] Add development guide
- [ ] Add contribution guide
- [ ] Add command format documentation
- [ ] Add tool action documentation
- [ ] Add error handling documentation
- [ ] Add Arabic command documentation
- [ ] Add RTL text documentation
- [ ] Add Arabic number documentation
- [ ] Add speech command documentation
- [ ] Add audio file documentation
- [ ] Add speech recognition documentation
- [ ] Add text-to-speech documentation

---

## Previous TODOs
- (See previous entries for legacy/structural tasks)

# TODO

## Critical Issues (High Priority)
- [x] Fix system initialization error
  - [x] Create macOS configuration file
  - [x] Implement proper system info gatherer
  - [x] Update platform manager initialization
- [x] Fix platform manager reference error
  - [x] Implement proper system info gatherer
  - [x] Update platform manager to use system info gatherer
- [ ] Add default configuration handling
  - [x] Create default config.json for macOS
  - [ ] Add fallback configuration loading
  - [ ] Add configuration validation

## Platform Support (Medium Priority)
- [ ] Improve platform handler support
  - [ ] Fix MacInputHandler initialization
  - [ ] Fix MacAudioHandler initialization
  - [ ] Fix MacDisplayHandler initialization
  - [ ] Fix MacUSBHandler initialization
- [ ] Add IOKit dependency
  - [ ] Add pyobjc-framework-AppKit to requirements.txt
  - [ ] Add proper error handling for missing dependencies

## Internationalization (Medium Priority)
- [ ] Fix locale settings
  - [ ] Add proper locale detection
  - [ ] Add locale fallback mechanism
  - [ ] Add RTL support configuration

## General Improvements (Medium Priority)
- [ ] Enhance initialization sequence
  - [ ] Add proper error handling
  - [ ] Add graceful degradation
  - [ ] Add initialization logging
- [ ] Improve error handling
  - [ ] Add custom exception classes
  - [ ] Add error recovery mechanisms
  - [ ] Add error reporting
- [ ] Add comprehensive testing
  - [ ] Add unit tests
  - [ ] Add integration tests
  - [ ] Add platform-specific tests

## Documentation
- [ ] Update technical documentation
  - [ ] Add platform-specific setup guides
  - [ ] Add configuration guide
  - [ ] Add troubleshooting guide

## Next Steps
1. Address remaining critical issues:
   - Add fallback configuration loading
   - Add configuration validation
2. Fix platform handler support:
   - Implement proper handler initialization
   - Add dependency management
3. Fix internationalization:
   - Implement proper locale handling
   - Add RTL support
4. Add comprehensive testing:
   - Write unit tests
   - Write integration tests
5. Update documentation:
   - Add setup guides
   - Add configuration guide

## NAMING CONVENTION COMPLIANCE (HIGH PRIORITY)
- [x] Ensure all file and directory names follow kebab-case for rule files and snake_case for Python files
- [x] Update all file names to match their purpose (e.g., `api-validation.mdc`, `dockerfile-best-practices.mdc`)
- [x] Ensure all Python module names use snake_case
- [x] Ensure all Python class names use PascalCase
- [x] Ensure all Python function and variable names use snake_case
- [x] Ensure all constants use UPPER_SNAKE_CASE
- [x] Update all import statements to use proper module naming
- [x] Ensure all documentation files use kebab-case
- [x] Update all references to files in documentation to use correct naming

## STRUCTURAL COMPLIANCE (HIGH PRIORITY)
- [x] Fix directory structure to comply with file-folder-arch.mdc rules:
  - [x] Remove misplaced directories from src/labeeb/:
    - [x] cache/ (removed)
    - [x] endpoints/ (removed)
    - [x] components/ (removed)
    - [x] plugins/ (removed)
    - [x] config/ (removed)
    - [x] core/ (removed)
    - [x] Remove all __pycache__ directories from source tree
  - [x] Reorganize core files:
    - [x] Move browser_handler.py to handlers/
    - [x] Move ai_handler.py to services/
    - [x] Move model_manager.py to models/
    - [x] Move ai_command_interpreter.py to services/
    - [x] Move ai_command_extractor.py to services/
    - [x] Move ai_response_cache.py to services/
    - [x] Move user_interaction_history.py to services/
    - [x] Move error_handler.py to services/
    - [x] Move command_processor.py to services/
  - [x] Update imports in moved files:
    - [x] Update browser_handler.py imports
    - [x] Update ai_handler.py imports
    - [x] Update model_manager.py imports
    - [x] Update ai_command_interpreter.py imports
    - [x] Update ai_command_extractor.py imports
    - [x] Update ai_response_cache.py imports
    - [x] Update user_interaction_history.py imports
    - [x] Update error_handler.py imports
    - [x] Update command_processor.py imports
  - [x] Create proper __init__.py files:
    - [x] Add __init__.py to handlers/
    - [x] Add __init__.py to services/
    - [x] Add __init__.py to models/
  - [x] Service documentation updates:
    - [x] Update command_processor.py documentation
    - [x] Update ai_command_extractor.py documentation
    - [x] Update error_handler.py documentation
    - [x] Update user_interaction_history.py documentation
    - [x] Update ai_response_cache.py documentation
  - [ ] Documentation updates:
    - [ ] Create migration guide for developers
    - [ ] Update API documentation
    - [ ] Update service interaction diagrams
    - [ ] Update deployment guide

## SERVICE ARCHITECTURE COMPLIANCE (HIGH PRIORITY)
- [x] Implement service registry:
  - [x] Create service registration mechanism
  - [x] Add service discovery functionality
  - [x] Implement service health checks
  - [x] Add service monitoring
- [x] Add service interfaces:
  - [x] Define clear input/output contracts
  - [x] Implement service composition
  - [x] Add service orchestration
  - [x] Create service documentation
- [x] Implement service security:
  - [x] Add authentication mechanisms
  - [x] Implement authorization checks
  - [x] Add data encryption
  - [x] Implement secure communication
- [x] Add service testing:
  - [x] Create unit tests
  - [x] Add integration tests
  - [x] Implement performance tests
  - [x] Add security tests

## NEW SERVICE TASKS
- [ ] Implement service composition:
  - [ ] Create service composer class
  - [ ] Add service dependency resolution
  - [ ] Implement service lifecycle management
  - [ ] Add service configuration management
- [ ] Add service monitoring:
  - [ ] Implement service metrics collection
  - [ ] Add service health dashboards
  - [ ] Create service alerting system
  - [ ] Add service logging aggregation
- [ ] Enhance service security:
  - [ ] Add rate limiting
  - [ ] Implement audit logging
  - [ ] Add security headers
  - [ ] Implement CORS policies
- [ ] Improve service testing:
  - [ ] Add load testing
  - [ ] Implement chaos testing
  - [ ] Add security penetration testing
  - [ ] Create end-to-end test suite