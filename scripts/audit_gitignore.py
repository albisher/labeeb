import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
GITIGNORE_FILE = PROJECT_ROOT / '.gitignore'
REPORTS_DIR = PROJECT_ROOT / 'reports'

REQUIRED_PATTERNS = ['.venv', 'reports/', '*.log', '__pycache__', '*.pyc', 'coverage/', 'htmlcov/', 'dist/', 'build/', '*.egg-info']
violations = []

def check_gitignore():
    if not GITIGNORE_FILE.exists():
        violations.append({'path': str(GITIGNORE_FILE), 'message': '.gitignore file missing'})
        return
    content = GITIGNORE_FILE.read_text()
    for pat in REQUIRED_PATTERNS:
        if pat not in content:
            violations.append({'pattern': pat, 'message': f'Missing gitignore pattern: {pat}'})

def write_report():
    REPORTS_DIR.mkdir(exist_ok=True)
    report_path = REPORTS_DIR / 'gitignore_audit.json'
    with open(report_path, 'w') as f:
        json.dump({'timestamp': datetime.now().isoformat(), 'violations': violations}, f, indent=2)
    print(f"Gitignore audit complete. Results written to {report_path}")

if __name__ == '__main__':
    check_gitignore()
    write_report() 