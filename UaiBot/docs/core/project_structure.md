# Labeeb Project Structure

## Core Components

### Main Application (`src/labeeb/`)
- `__main__.py` - Application entry point
- `ai/` - AI-driven command interpretation and agent logic
- `awareness/` - System and environment awareness
- `command_processing/` - Command processing and execution
- `core/` - Core logic and orchestration
- `data_models/` - Data models and containers
- `exceptions/` - Exception hierarchy
- `platform_services/` - Platform-specific and common services
- `services/` - Service layer
- `tools/` - Atomic, reusable tools
- `ui/` - UI components (CLI, GUI, web)
- `utils/` - Utility functions and helpers

### Configuration (`config/`)
- `command_patterns.json` - Command pattern definitions
- `keys/encrypted_keys.json` - Encrypted keys
- `output_styles.json` - Output styling configuration
- `settings.json` - Application settings

### Utilities (`src/labeeb/utils/`)
- `output_handler.py` - Output handling
- `output_style_manager.py` - Output style management
- `file_utils.py` - File utility functions
- `output_facade.py` - Output formatting facade
- `output_formatter.py` - Output formatting utilities
- `parallel_utils.py` - Parallel processing utilities
- `system_health_check.py` - System health monitoring

### Scripts (`scripts/`)
- `audit_project.py` - Project audit script
- `compile_translations.py` - Translation compilation

### Internationalization (`locales/`)
- `ar/LC_MESSAGES/labeeb.po`/`.mo` - Arabic translations
- `en/LC_MESSAGES/labeeb.po`/`.mo` - English translations

## Testing (`tests/`)
- Mirrors the structure of `src/labeeb/` for unit, integration, and e2e tests
- `fixtures/`, `integration/`, `unit/`, `e2e/`, `test_files/`, `screenshots/`

## Documentation (`docs/`)
- `architecture/`, `features/`, `agents_tools/`, ...
- Only one `research/` directory inside `docs/`

## Reports (`reports/`)
- `coverage/` - Coverage reports (gitignored)
- `test_results/` - Test results (gitignored)

## Todo (`TODO.md` at root)
- The only allowed TODO file

## Directory Organization

The project follows a strict directory structure to maintain organization and clarity:

```
.
├── .git
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── .pre-commit-config.yaml
├── .venv/                # Virtual environment (gitignored)
├── .vscode/              # Optional: Editor settings
├── COMMERCIAL_LICENSE
├── LICENSE
├── README.md
├── TODO.md               # The only allowed file for TODO to be added in.
├── config/
│   ├── command_patterns.json
│   ├── keys/
│   │   └── encrypted_keys.json
│   ├── output_styles.json
│   └── settings.json
├── docs/
│   ├── agents_tools/
│   ├── architecture/
│   ├── features/
│   ├── research/         # Only allowed research directory
│   └── ...
├── locales/
│   ├── ar/
│   │   └── LC_MESSAGES/
│   │       ├── labeeb.mo
│   │       └── labeeb.po
│   └── en/ # etc.
├── pyproject.toml
├── requirements.txt
├── setup.py
├── scripts/
│   ├── audit_project.py
│   ├── compile_translations.py
│   └── ...
├── src/
│   ├── __init__.py
│   └── labeeb/
│       ├── __init__.py
│       ├── __main__.py
│       ├── ai/
│       ├── awareness/
│       ├── command_processing/
│       ├── core/
│       ├── data_models/
│       ├── exceptions/
│       ├── platform_services/
│       ├── services/
│       ├── tools/
│       ├── ui/
│       └── utils/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── fixtures/
│   ├── integration/
│   │   └── labeeb/
│   ├── unit/
│   │   └── labeeb/
│   ├── e2e/
│   ├── test_files/
│   └── screenshots/
└── reports/
    ├── coverage/
    │   ├── htmlcov/
    │   └── coverage.xml
    └── test_results/
```

## Important Notes

1. All Python test files (.py) must be in the `tests/` directory, mirroring `src/labeeb/` structure
2. Human instructions should be written in natural language
3. The project uses Python 3.10+
4. Virtual environment (venv) is required for development
5. Cross-platform compatibility is maintained
6. Only one `TODO.md` at the root is allowed
7. Use only the approved directory structure; no alternative or legacy structures 