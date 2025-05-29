# Project File and Folder Architecture

This document defines and enforces the required file and folder structure for the project. All contributors and auditing scripts must follow these rules. No alternative architectures are permitted.

## Visual Directory Structure

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
├── config/               # Configuration files
│   ├── command_patterns.json
│   ├── keys/
│   │   └── encrypted_keys.json
│   ├── output_styles.json
│   └── settings.json
├── docs/                 # Documentation
│   ├── agents_tools/
│   ├── architecture/
│   ├── features/
│   ├── research/         # Only allowed research directory
│   └── ...
├── locales/              # Internationalization (i18n)
│   ├── ar/
│   │   └── LC_MESSAGES/
│   │       ├── labeeb.mo
│   │       └── labeeb.po
│   └── en/ # etc.
├── pyproject.toml
├── requirements.txt
├── setup.py
├── scripts/              # Utility scripts
│   ├── audit_project.py
│   ├── compile_translations.py
│   └── ...
├── src/                  # Main source code
│   ├── __init__.py
│   └── labeeb/           # Main application package (renamed from 'app')
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
├── tests/                # All tests (mirrors src/labeeb/ structure)
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
└── reports/              # Gitignored: test results, coverage reports
    ├── coverage/
    │   ├── htmlcov/
    │   └── coverage.xml
    └── test_results/
```

## Explicit Placement Rules

- **No Backups or Redundant Files:**

  - Remove all `.backup` directories and `.bak` files. Use Git for all history and backup needs.
- **Consolidate Research:**

  - Only one `research/` directory is allowed, and it must be inside `docs/` if it contains documentation.
- **Gitignore Enforcement:**

  - All generated files, logs, caches, coverage reports, and virtual environments must be listed in `.gitignore`.
  - Example entries:
    ```
    .venv/
    .cache/
    .coverage
    coverage.xml
    htmlcov/
    logs/
    dist/
    build/
    *.bak
    reports/
    ```
- **Standard Directory Locations:**

  - `src/` for all source code.
  - `src/labeeb/` (rename from `src/app/`) as the main package.
  - No logs or tests inside `src/`. Place logs at the top level (gitignored) and tests in the top-level `tests/` directory.
  - Utilities and helpers go in `src/labeeb/utils/` or `src/utils/` as appropriate.
  - Documentation in `docs/`, with research consolidated inside.
  - Config files in `config/`.
  - Scripts in `scripts/`.
  - Internationalization files in `locales/`.
  - Test results and coverage reports in a gitignored `reports/` directory.
- **Naming Conventions:**

  - Use English for folder and file names unless the project is strictly for a non-English-speaking team.
- **No Symlinks for Source Files:**

  - Physically move files to their intended locations and update imports accordingly. Do not use symlinks for source files.
- **Tests Mirror Source Structure:**

  - Tests in `tests/` must mirror the internal structure of `src/labeeb/`.

## Documentation and Reference Updates

- All documentation, rules, and auditing scripts must reference only this structure. Remove any mention of alternative or legacy structures.
- Update `README.md` and `TODO.md` to reflect only the approved directory structure and rules.

## Auditing and Enforcement

- All audit scripts must check for and enforce this architecture only. Remove or update any scripts that reference deprecated or alternative layouts.

## Strict Compliance

- No alternative file or folder organization methods are allowed. This is the only approved structure for the project.

## Example Implementation Steps (for Contributors)

1. **Clean Up:**
   - Remove all `.bak` files and `.backup` directories.
2. **Move/Rename Folders:**
   - Move `src/app/` to `src/labeeb/`.
   - Move all tests to the top-level `tests/` directory.
3. **Update .gitignore:**
   - Add all required patterns as shown above.
4. **Update Imports and References:**
   - Update all imports and references to match the new structure.
5. **Update Documentation and Scripts:**
   - Ensure all documentation and scripts reference only the new structure.
6. **Run Audit Scripts:**
   - Run audit scripts to verify compliance before every commit.
