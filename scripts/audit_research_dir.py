import os
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
DOCS_RESEARCH = PROJECT_ROOT / 'docs/research'
REPORTS_DIR = PROJECT_ROOT / 'reports'

violations = []

def check_research_dirs():
    found = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        for d in dirs:
            if d == 'research':
                found.append(os.path.join(root, d))
    allowed = str(DOCS_RESEARCH.resolve())
    for d in found:
        if os.path.abspath(d) != allowed:
            violations.append({'path': d, 'message': 'Extra/misplaced research directory'})
    if not os.path.exists(allowed):
        violations.append({'path': allowed, 'message': 'Missing required docs/research/ directory'})

def write_report():
    REPORTS_DIR.mkdir(exist_ok=True)
    report_path = REPORTS_DIR / 'research_dir_audit.json'
    with open(report_path, 'w') as f:
        json.dump({'timestamp': datetime.now().isoformat(), 'violations': violations}, f, indent=2)
    print(f"Research dir audit complete. Results written to {report_path}")

if __name__ == '__main__':
    check_research_dirs()
    write_report() 