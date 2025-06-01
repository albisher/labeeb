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

---

All TODOs are now tracked in this unified checklist. Remove all inline TODOs from code and documentation after adding them here. Mark each as complete with [x] when done.
