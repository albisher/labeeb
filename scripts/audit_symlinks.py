import os
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / 'src'
REPORTS_DIR = PROJECT_ROOT / 'reports'

violations = []

def check_symlinks():
    for root, dirs, files in os.walk(SRC_DIR):
        for name in files + dirs:
            path = Path(root) / name
            if path.is_symlink():
                violations.append({'path': str(path.relative_to(PROJECT_ROOT)), 'message': 'Symlink found in src/ (not allowed)'})

def write_report():
    REPORTS_DIR.mkdir(exist_ok=True)
    report_path = REPORTS_DIR / 'symlinks_audit.json'
    with open(report_path, 'w') as f:
        json.dump({'timestamp': datetime.now().isoformat(), 'violations': violations}, f, indent=2)
    print(f"Symlink audit complete. Results written to {report_path}")

if __name__ == '__main__':
    check_symlinks()
    write_report() 