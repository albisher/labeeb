#!/usr/bin/env python3
"""
MITRE ATT&CK Code Audit Script

This script analyzes code files against MITRE ATT&CK techniques to identify potential
security patterns and coverage gaps. It uses the mitreattack-python library to access
MITRE ATT&CK data and performs static analysis on Python files.
"""

import os
import re
from typing import Dict, List, Set, Tuple
from mitreattack.stix20 import MitreAttackData
import ast
import json
from pathlib import Path
import tempfile
import requests
import time
from tqdm import tqdm
import sys

class MitreAttackAuditor:
    def __init__(self):
        """Initialize the MITRE ATT&CK auditor with STIX data."""
        print("Initializing MITRE ATT&CK auditor...")
        # Download the latest STIX data if not available
        stix_file = self._get_stix_data()
        self.mitre_data = MitreAttackData(stix_file)
        self.techniques = self.mitre_data.get_techniques(remove_revoked_deprecated=True)
        self.technique_patterns = self._build_technique_patterns()
        print(f"Loaded {len(self.techniques)} MITRE ATT&CK techniques")

    def _get_stix_data(self) -> str:
        """Download the latest MITRE ATT&CK STIX data."""
        stix_url = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json"
        temp_dir = tempfile.gettempdir()
        stix_file = os.path.join(temp_dir, "enterprise-attack.json")
        
        if not os.path.exists(stix_file):
            print("Downloading MITRE ATT&CK STIX data...")
            response = requests.get(stix_url)
            response.raise_for_status()
            with open(stix_file, 'wb') as f:
                f.write(response.content)
            print("Download complete")
        
        return stix_file

    def _build_technique_patterns(self) -> Dict[str, List[str]]:
        """Build regex patterns for each technique based on its description and name."""
        print("Building technique patterns...")
        patterns = {}
        for technique in self.techniques:
            technique_id = technique.external_references[0].external_id
            name = technique.name.lower()
            description = technique.description.lower()
            
            # Extract key terms from name and description
            terms = set(re.findall(r'\b\w{4,}\b', f"{name} {description}"))
            patterns[technique_id] = list(terms)
        
        return patterns

    def analyze_file(self, filepath: str) -> Dict[str, List[str]]:
        """Analyze a single file for MITRE ATT&CK technique patterns."""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            content = None
            
            for encoding in encodings:
                try:
                    with open(filepath, 'r', encoding=encoding) as f:
                        content = f.read().lower()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                print(f"Warning: Could not decode {filepath} with any supported encoding. Skipping file.")
                return {}
            
            # Parse the file to get function and class names
            try:
                tree = ast.parse(content)
                code_elements = []
                
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                        code_elements.append(node.name.lower())
            except SyntaxError:
                # If file is not valid Python, just use the content
                code_elements = []
            
            # Find matches between code elements and technique patterns
            matches = {}
            for technique_id, patterns in self.technique_patterns.items():
                technique_matches = []
                for pattern in patterns:
                    if pattern in content or any(pattern in elem for elem in code_elements):
                        technique_matches.append(pattern)
                if technique_matches:
                    matches[technique_id] = technique_matches
            
            return matches
        except Exception as e:
            print(f"Error analyzing {filepath}: {str(e)}")
            return {}

    def audit_directory(self, directory: str, extensions: List[str] = ['.py']) -> Dict[str, Dict[str, List[str]]]:
        """Audit all files in a directory against MITRE ATT&CK techniques."""
        results = {}
        
        # Get list of files to analyze
        files_to_analyze = []
        for root, _, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    filepath = os.path.join(root, file)
                    files_to_analyze.append(filepath)
        
        print(f"Found {len(files_to_analyze)} files to analyze")
        
        # Analyze files with progress bar
        for filepath in tqdm(files_to_analyze, desc="Analyzing files"):
            matches = self.analyze_file(filepath)
            if matches:
                results[filepath] = matches
            time.sleep(0.01)  # Small delay to prevent overwhelming the system
        
        return results

    def generate_report(self, results: Dict[str, Dict[str, List[str]]], output_file: str):
        """Generate a detailed report of the audit results."""
        print("Generating report...")
        report = {
            "audit_summary": {
                "total_files_analyzed": len(results),
                "files_with_matches": len([f for f in results if results[f]]),
                "total_techniques_found": len(set(
                    technique_id 
                    for file_matches in results.values() 
                    for technique_id in file_matches
                ))
            },
            "detailed_results": results
        }
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report generated at: {output_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Audit code against MITRE ATT&CK techniques')
    parser.add_argument('directory', help='Directory to audit')
    parser.add_argument('--output', '-o', default='reports/test_results/mitre_attack_audit.json',
                      help='Output report file (default: reports/test_results/mitre_attack_audit.json)')
    parser.add_argument('--extensions', '-e', nargs='+', default=['.py'],
                      help='File extensions to analyze (default: .py)')
    
    args = parser.parse_args()
    
    try:
        auditor = MitreAttackAuditor()
        results = auditor.audit_directory(args.directory, args.extensions)
        auditor.generate_report(results, args.output)
    except KeyboardInterrupt:
        print("\nAudit interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error during audit: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 