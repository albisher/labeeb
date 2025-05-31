#!/usr/bin/env python3
"""
Dependency Security Audit Script

This script analyzes Python project dependencies for known security vulnerabilities
and outdated packages. It uses the Safety database to check for known vulnerabilities
and provides recommendations for secure package versions.
"""

import os
import json
import subprocess
from typing import Dict, List, Set, Tuple
import sys
from pathlib import Path

class DependencyAuditor:
    def __init__(self):
        """Initialize the dependency auditor."""
        self.vulnerable_packages = {}
        self.outdated_packages = {}
        self.requirements_files = []

    def find_requirements_files(self, directory: str) -> List[str]:
        """Find all requirements files in the project."""
        requirements_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file in ['requirements.txt', 'requirements-dev.txt', 'setup.py']:
                    requirements_files.append(os.path.join(root, file))
        return requirements_files

    def get_installed_packages(self) -> Dict[str, str]:
        """Get currently installed packages and their versions using pip."""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'list', '--format=json'],
                capture_output=True,
                text=True
            )
            packages = json.loads(result.stdout)
            return {pkg['name']: pkg['version'] for pkg in packages}
        except Exception as e:
            print(f"Error getting installed packages: {str(e)}")
            return {}

    def check_vulnerabilities(self, packages: Dict[str, str]) -> Dict[str, List[Dict]]:
        """Check packages for known vulnerabilities using Safety."""
        try:
            # Run safety check
            result = subprocess.run(
                ['safety', 'check', '--json'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {}
            
            vulnerabilities = json.loads(result.stdout)
            return vulnerabilities
        except Exception as e:
            print(f"Error checking vulnerabilities: {str(e)}")
            return {}

    def check_outdated_packages(self, packages: Dict[str, str]) -> Dict[str, str]:
        """Check for outdated packages using pip."""
        try:
            # Run pip list --outdated
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'list', '--outdated', '--format=json'],
                capture_output=True,
                text=True
            )
            
            outdated = json.loads(result.stdout)
            return {pkg['name']: pkg['latest_version'] for pkg in outdated}
        except Exception as e:
            print(f"Error checking outdated packages: {str(e)}")
            return {}

    def analyze_requirements_file(self, filepath: str) -> Dict[str, List[str]]:
        """Analyze a requirements file for potential issues."""
        issues = {
            'missing_versions': [],
            'pinned_versions': [],
            'unpinned_versions': [],
            'development_dependencies': []
        }
        
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Check for version pinning
                    if '==' in line:
                        issues['pinned_versions'].append(line)
                    elif '>=' in line or '<=' in line:
                        issues['unpinned_versions'].append(line)
                    else:
                        issues['missing_versions'].append(line)
                    
                    # Check for development dependencies
                    if any(dev_pkg in line.lower() for dev_pkg in ['pytest', 'coverage', 'black', 'flake8']):
                        issues['development_dependencies'].append(line)
        
        except Exception as e:
            print(f"Error analyzing {filepath}: {str(e)}")
        
        return issues

    def audit_project(self, directory: str) -> Dict:
        """Perform a complete dependency audit of the project."""
        # Find requirements files
        self.requirements_files = self.find_requirements_files(directory)
        
        # Get installed packages
        installed_packages = self.get_installed_packages()
        
        # Check for vulnerabilities
        self.vulnerable_packages = self.check_vulnerabilities(installed_packages)
        
        # Check for outdated packages
        self.outdated_packages = self.check_outdated_packages(installed_packages)
        
        # Analyze requirements files
        requirements_analysis = {}
        for req_file in self.requirements_files:
            requirements_analysis[req_file] = self.analyze_requirements_file(req_file)
        
        return {
            'requirements_files': self.requirements_files,
            'installed_packages': installed_packages,
            'vulnerable_packages': self.vulnerable_packages,
            'outdated_packages': self.outdated_packages,
            'requirements_analysis': requirements_analysis
        }

    def generate_report(self, results: Dict, output_file: str):
        """Generate a detailed report of the dependency audit results."""
        report = {
            "audit_summary": {
                "total_requirements_files": len(results['requirements_files']),
                "total_installed_packages": len(results['installed_packages']),
                "vulnerable_packages": len(results['vulnerable_packages']),
                "outdated_packages": len(results['outdated_packages'])
            },
            "detailed_results": results
        }
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Audit project dependencies for security issues')
    parser.add_argument('directory', help='Project directory to audit')
    parser.add_argument('--output', '-o', default='reports/test_results/dependency_audit.json',
                      help='Output report file (default: reports/test_results/dependency_audit.json)')
    
    args = parser.parse_args()
    
    try:
        auditor = DependencyAuditor()
        results = auditor.audit_project(args.directory)
        auditor.generate_report(results, args.output)
        print(f"Dependency audit complete. Report generated at: {args.output}")
    except KeyboardInterrupt:
        print("\nAudit interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error during audit: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 