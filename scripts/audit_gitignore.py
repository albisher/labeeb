import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
GITIGNORE_FILE = PROJECT_ROOT / '.gitignore'
REPORTS_DIR = PROJECT_ROOT / 'reports' / 'test_results'

REQUIRED_PATTERNS = ['.venv', 'reports/', '*.log', '__pycache__', '*.pyc', 'coverage/', 'htmlcov/', 'dist/', 'build/', '*.egg-info']
violations = []

def check_gitignore():
    if not GITIGNORE_FILE.exists():
        violations.append({'type': 'missing_file', 'path': str(GITIGNORE_FILE), 'message': '.gitignore file missing'})
        return
    content = GITIGNORE_FILE.read_text()
    for pat in REQUIRED_PATTERNS:
        if pat not in content:
            violations.append({'type': 'gitignore_pattern', 'path': pat, 'message': f'Missing gitignore pattern: {pat}'})

def write_report():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / 'gitignore_audit.json'
    report = {
        'timestamp': datetime.now().isoformat(),
        'success': len(violations) == 0,
        'violations': violations
    }
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Gitignore audit complete. Results written to {report_path}")

if __name__ == '__main__':
    check_gitignore()
    write_report() 