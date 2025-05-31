import os
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
REPORTS_DIR = PROJECT_ROOT / 'reports' / 'test_results'
TESTS_RESULTS = PROJECT_ROOT / 'tests/results'
violations = []

def check_reports_location():
    if TESTS_RESULTS.exists():
        for f in TESTS_RESULTS.rglob('*'):
            if f.is_file():
                violations.append({
                    'type': 'misplaced_report',
                    'path': str(f.relative_to(PROJECT_ROOT)),
                    'message': 'Test/audit result file not in reports/ (should be moved)'
                })

def write_report():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / 'reports_location_audit.json'
    report = {
        'timestamp': datetime.now().isoformat(),
        'success': len(violations) == 0,
        'violations': violations
    }
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Reports location audit complete. Results written to {report_path}")

if __name__ == '__main__':
    check_reports_location()
    write_report() 