import os
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
DOCS_RESEARCH = PROJECT_ROOT / 'docs/research'
REPORTS_DIR = PROJECT_ROOT / 'reports' / 'test_results'

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
            violations.append({
                'type': 'misplaced_research_directory',
                'path': str(Path(d).relative_to(PROJECT_ROOT)),
                'message': 'Extra/misplaced research directory (only docs/research/ allowed)'
            })
    if not os.path.exists(allowed):
        violations.append({
            'type': 'missing_directory',
            'path': str(DOCS_RESEARCH.relative_to(PROJECT_ROOT)),
            'message': 'Missing required docs/research/ directory'
        })

def write_report():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / 'research_dir_audit.json'
    report = {
        'timestamp': datetime.now().isoformat(),
        'success': len(violations) == 0,
        'violations': violations
    }
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Research dir audit complete. Results written to {report_path}")

if __name__ == '__main__':
    check_research_dirs()
    write_report() 