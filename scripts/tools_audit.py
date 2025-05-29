import os
import importlib.util
import inspect
from pathlib import Path
import sys
import json
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
TOOLS_DIR = PROJECT_ROOT / 'src/labeeb/tools'
REPORTS_DIR = PROJECT_ROOT / 'reports'
TODO_FILE = PROJECT_ROOT / 'TODO.md'

results = []

def get_docstring(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    doc = None
    if lines and lines[0].strip().startswith('"""'):
        doc = lines[0].strip().strip('"')
    return doc

def import_tool_class(file_path):
    module_name = file_path.stem
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        return None, f"Import error: {e}"
    # Find the main class (ending with Tool)
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if name.lower().endswith('tool') and obj.__module__ == module.__name__:
            return obj, None
    return None, "No tool class found"

def check_tool_requirements(file, tool_cls):
    findings = []
    # Check for explicit input/output (look for type hints on main method)
    if tool_cls:
        main_methods = [m for m in ['execute', 'run', '__call__'] if hasattr(tool_cls, m)]
        if not main_methods:
            findings.append("No main execution method (execute/run/__call__) found.")
        else:
            for m in main_methods:
                method = getattr(tool_cls, m)
                if not hasattr(method, '__annotations__') or not method.__annotations__:
                    findings.append(f"Method '{m}' missing type hints for input/output.")
        # Check for statelessness (no instance attributes set outside __init__)
        if hasattr(tool_cls, '__init__'):
            src = inspect.getsource(tool_cls.__init__)
            if any('self.' in line and not line.strip().startswith('self.') for line in src.splitlines()):
                findings.append("Potential stateful behavior in __init__.")
    # Versioning (look for __version__ attribute)
    if not hasattr(tool_cls, '__version__'):
        findings.append("No __version__ attribute found.")
    return findings

def audit_tools():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    for file in TOOLS_DIR.glob('*.py'):
        if file.name == '__init__.py':
            continue
        doc = get_docstring(file)
        doc_ok = bool(doc and len(doc) > 10 and 'tool' in doc.lower())
        tool_cls, import_err = import_tool_class(file)
        findings = []
        if tool_cls:
            findings.extend(check_tool_requirements(file, tool_cls))
        else:
            findings.append(import_err or "No tool class found")
        results.append({
            'file': file.name,
            'doc_ok': doc_ok,
            'doc': doc,
            'tool_cls': tool_cls.__name__ if tool_cls else None,
            'findings': findings
        })
    # Write audit results to reports/tools_audit.json
    report_path = REPORTS_DIR / 'tools_audit.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({'timestamp': datetime.now().isoformat(), 'results': results}, f, indent=2)
    print(f"Audit complete. Results written to {report_path}")

audit_tools() 