import os
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
SRC_LABEEB = PROJECT_ROOT / 'src/labeeb'
TESTS_UNIT_LABEEB = PROJECT_ROOT / 'tests/unit/labeeb'
REPORTS_DIR = PROJECT_ROOT / 'reports' / 'test_results'

violations = []

def check_mirror():
    if not SRC_LABEEB.exists():
        violations.append({
            'type': 'missing_directory',
            'path': str(SRC_LABEEB.relative_to(PROJECT_ROOT)),
            'message': 'src/labeeb/ does not exist'
        })
        return
    for sub in SRC_LABEEB.iterdir():
        if sub.is_dir():
            test_sub = TESTS_UNIT_LABEEB / sub.name
            if not test_sub.exists():
                violations.append({
                    'type': 'missing_test_directory',
                    'path': str(test_sub.relative_to(PROJECT_ROOT)),
                    'message': f'Missing test directory for src/labeeb/{sub.name}'
                })

def write_report():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / 'test_structure_audit.json'
    report = {
        'timestamp': datetime.now().isoformat(),
        'success': len(violations) == 0,
        'violations': violations
    }
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Test structure audit complete. Results written to {report_path}")

if __name__ == '__main__':
    check_mirror()
    write_report() 