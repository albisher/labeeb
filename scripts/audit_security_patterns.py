#!/usr/bin/env python3
"""
Security Pattern Audit Script

This script analyzes code for potential security vulnerabilities and patterns
based on MITRE ATT&CK tactics. It performs static analysis to identify
potentially dangerous code patterns and security anti-patterns.
"""

import os
import re
import ast
from typing import Dict, List, Set, Tuple
import json
from pathlib import Path

class SecurityPatternAuditor:
    def __init__(self):
        """Initialize the security pattern auditor with predefined patterns."""
        self.patterns = {
            'execution': {
                'os.system': 'Direct system command execution',
                'subprocess.call': 'Subprocess execution',
                'eval(': 'Dynamic code evaluation',
                'exec(': 'Dynamic code execution',
                'pickle.loads': 'Unsafe deserialization',
            },
            'persistence': {
                'crontab': 'Cron job modification',
                'startup': 'Startup script modification',
                'registry': 'Registry modification',
            },
            'privilege_escalation': {
                'sudo': 'Sudo command usage',
                'su ': 'User switching',
                'chmod': 'Permission modification',
                'chown': 'Ownership modification',
            },
            'defense_evasion': {
                'rm -rf': 'Recursive deletion',
                'chattr': 'File attribute modification',
                'iptables': 'Firewall modification',
            },
            'credential_access': {
                'password': 'Password handling',
                'secret': 'Secret handling',
                'key': 'Key handling',
                'token': 'Token handling',
            },
            'discovery': {
                'netstat': 'Network connection discovery',
                'ps aux': 'Process discovery',
                'ls -la': 'File system discovery',
            },
            'lateral_movement': {
                'ssh': 'SSH connection',
                'scp': 'Secure copy',
                'rsync': 'Remote sync',
            },
            'collection': {
                'keyboard': 'Keyboard input',
                'clipboard': 'Clipboard access',
                'screenshot': 'Screenshot capture',
            },
            'command_and_control': {
                'socket': 'Network socket',
                'http': 'HTTP connection',
                'dns': 'DNS query',
            },
            'exfiltration': {
                'ftp': 'FTP transfer',
                'sftp': 'SFTP transfer',
                'upload': 'File upload',
            },
            'impact': {
                'delete': 'Data deletion',
                'encrypt': 'Data encryption',
                'overwrite': 'Data overwrite',
            }
        }

    def analyze_file(self, filepath: str) -> Dict[str, List[Tuple[str, str]]]:
        """Analyze a single file for security patterns."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the file to get line numbers
            tree = ast.parse(content)
            line_numbers = {node.lineno: node for node in ast.walk(tree)}
            
            results = {}
            for tactic, patterns in self.patterns.items():
                tactic_matches = []
                for pattern, description in patterns.items():
                    # Search for pattern in content
                    for i, line in enumerate(content.split('\n'), 1):
                        if pattern.lower() in line.lower():
                            # Get context (3 lines before and after)
                            start = max(1, i - 3)
                            end = min(len(content.split('\n')), i + 4)
                            context = '\n'.join(content.split('\n')[start-1:end])
                            
                            tactic_matches.append((
                                f"Line {i}: {line.strip()}",
                                description,
                                context
                            ))
                
                if tactic_matches:
                    results[tactic] = tactic_matches
            
            return results
        except Exception as e:
            print(f"Error analyzing {filepath}: {str(e)}")
            return {}

    def audit_directory(self, directory: str, extensions: List[str] = ['.py']) -> Dict[str, Dict[str, List[Tuple[str, str, str]]]]:
        """Audit all files in a directory for security patterns."""
        results = {}
        
        for root, _, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    filepath = os.path.join(root, file)
                    matches = self.analyze_file(filepath)
                    if matches:
                        results[filepath] = matches
        
        return results

    def generate_report(self, results: Dict[str, Dict[str, List[Tuple[str, str, str]]]], output_file: str):
        """Generate a detailed report of the security audit results."""
        report = {
            "audit_summary": {
                "total_files_analyzed": len(results),
                "files_with_issues": len([f for f in results if results[f]]),
                "total_issues_found": sum(
                    len(matches)
                    for file_matches in results.values()
                    for tactic_matches in file_matches.values()
                    for _ in tactic_matches
                )
            },
            "detailed_results": results
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Audit code for security patterns')
    parser.add_argument('directory', help='Directory to audit')
    parser.add_argument('--output', '-o', default='reports/test_results/security_patterns_audit.json',
                      help='Output report file (default: reports/test_results/security_patterns_audit.json)')
    parser.add_argument('--extensions', '-e', nargs='+', default=['.py'],
                      help='File extensions to analyze (default: .py)')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    auditor = SecurityPatternAuditor()
    results = auditor.audit_directory(args.directory, args.extensions)
    auditor.generate_report(results, args.output)
    
    print(f"Security audit complete. Report generated at: {args.output}")

if __name__ == '__main__':
    main() 