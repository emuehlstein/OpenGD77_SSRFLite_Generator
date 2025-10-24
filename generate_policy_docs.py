#!/usr/bin/env python3
"""
Generate markdown documentation for policy files.

This script analyzes policy YAML files and generates comprehensive documentation
including assignment overrides, zone configurations, scan settings, and more.
"""

import argparse
import pathlib
import yaml
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional, Set


# Paths
POLICIES_ROOT = pathlib.Path("policies")
DEFAULT_DOCS_DIR = pathlib.Path("docs/policies")


def load_yaml_file(file_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """Load and parse a YAML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None


def analyze_policy_file(file_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    """Analyze a single policy file and extract key information."""
    data = load_yaml_file(file_path)
    if not data:
        return None
    
    # Extract policy data
    policy = data.get('policy', {})
    assignments = policy.get('assignments', {})
    
    analysis = {
        'file_path': file_path,
        'filename': file_path.name,
        'name': file_path.stem,
        'assignments': assignments,
        'assignment_count': len(assignments),
        'zones': set(),
        'rx_only_assignments': [],
        'tx_enabled_assignments': [],
        'scan_enabled_assignments': [],
        'scan_disabled_assignments': [],
        'custom_names': {},
        'zone_assignments': defaultdict(list),
        'has_scan_config': False,
        'has_zone_config': False,
        'has_codeplug_config': False,
        'has_tx_config': False,
    }
    
    # Analyze each assignment
    for assignment_id, config in assignments.items():
        codeplug = config.get('codeplug', {})
        zones = config.get('zones', {})
        scan = config.get('scan', {})
        tx = config.get('tx', {})
        
        # Track configuration types
        if codeplug:
            analysis['has_codeplug_config'] = True
        if zones:
            analysis['has_zone_config'] = True
        if scan:
            analysis['has_scan_config'] = True  
        if tx:
            analysis['has_tx_config'] = True
        
        # Custom names
        custom_name = codeplug.get('name')
        if custom_name:
            analysis['custom_names'][assignment_id] = custom_name
        
        # RX/TX settings
        rx_only = codeplug.get('rx_only')
        if rx_only is True:
            analysis['rx_only_assignments'].append(assignment_id)
        elif rx_only is False:
            analysis['tx_enabled_assignments'].append(assignment_id)
        
        # TX settings
        tx_enabled = tx.get('enabled')
        if tx_enabled is True:
            analysis['tx_enabled_assignments'].append(assignment_id)
        elif tx_enabled is False:
            analysis['rx_only_assignments'].append(assignment_id)
        
        # Scan settings
        all_skip = scan.get('all_skip')
        zone_skip = scan.get('zone_skip')
        if all_skip is False or zone_skip is False:
            analysis['scan_enabled_assignments'].append(assignment_id)
        elif all_skip is True or zone_skip is True:
            analysis['scan_disabled_assignments'].append(assignment_id)
        
        # Zone memberships
        zone_includes = zones.get('include', [])
        zone_excludes = zones.get('exclude', [])
        
        for zone in zone_includes:
            analysis['zones'].add(zone)
            analysis['zone_assignments'][zone].append(assignment_id)
    
    # Remove duplicates
    analysis['rx_only_assignments'] = list(set(analysis['rx_only_assignments']))
    analysis['tx_enabled_assignments'] = list(set(analysis['tx_enabled_assignments']))
    analysis['scan_enabled_assignments'] = list(set(analysis['scan_enabled_assignments']))
    analysis['scan_disabled_assignments'] = list(set(analysis['scan_disabled_assignments']))
    
    return analysis


def generate_policy_documentation(analysis: Dict[str, Any]) -> str:
    """Generate markdown documentation for a single policy file."""
    
    doc = []
    
    # Header
    doc.append(f"# {analysis['name']}")
    doc.append("")
    doc.append(f"**File:** `{analysis['filename']}`  ")
    doc.append(f"**Path:** `policies/{analysis['filename']}`  ")
    doc.append("")
    
    # Overview
    doc.append("## Overview")
    doc.append("")
    doc.append(f"- **Assignment Overrides:** {analysis['assignment_count']}")
    doc.append(f"- **Zone Definitions:** {len(analysis['zones'])}")
    doc.append(f"- **Custom Names:** {len(analysis['custom_names'])}")
    doc.append(f"- **RX-Only Assignments:** {len(analysis['rx_only_assignments'])}")
    doc.append(f"- **TX-Enabled Assignments:** {len(analysis['tx_enabled_assignments'])}")
    doc.append(f"- **Scan-Enabled Assignments:** {len(analysis['scan_enabled_assignments'])}")
    doc.append("")
    
    # Configuration Types
    doc.append("### Configuration Types")
    doc.append("")
    config_types = []
    if analysis['has_codeplug_config']:
        config_types.append("**Codeplug:** Channel names, RX/TX settings")
    if analysis['has_zone_config']:
        config_types.append("**Zones:** Zone membership and exclusions")
    if analysis['has_scan_config']:
        config_types.append("**Scan:** Skip settings and scan behavior")
    if analysis['has_tx_config']:
        config_types.append("**TX:** Transmit enable/disable")
    
    for config_type in config_types:
        doc.append(f"- {config_type}")
    
    if not config_types:
        doc.append("- *No configuration overrides*")
    
    doc.append("")
    
    # Zone Organization
    if analysis['zones']:
        doc.append("## Zone Organization")
        doc.append("")
        
        zone_stats = []
        for zone in sorted(analysis['zones']):
            count = len(analysis['zone_assignments'][zone])
            zone_stats.append((zone, count))
        
        doc.append("| Zone | Assignments |")
        doc.append("|------|-------------|")
        for zone, count in zone_stats:
            doc.append(f"| {zone} | {count} |")
        doc.append("")
    
    # Custom Names
    if analysis['custom_names']:
        doc.append("## Custom Channel Names")
        doc.append("")
        doc.append("| Assignment ID | Custom Name |")
        doc.append("|---------------|-------------|")
        for assignment_id in sorted(analysis['custom_names'].keys()):
            custom_name = analysis['custom_names'][assignment_id]
            doc.append(f"| `{assignment_id}` | {custom_name} |")
        doc.append("")
    
    # TX/RX Configuration
    if analysis['rx_only_assignments'] or analysis['tx_enabled_assignments']:
        doc.append("## TX/RX Configuration")
        doc.append("")
        
        if analysis['rx_only_assignments']:
            doc.append("### RX-Only Assignments")
            doc.append("")
            for assignment_id in sorted(analysis['rx_only_assignments']):
                doc.append(f"- `{assignment_id}`")
            doc.append("")
        
        if analysis['tx_enabled_assignments']:
            doc.append("### TX-Enabled Assignments")
            doc.append("")
            for assignment_id in sorted(analysis['tx_enabled_assignments']):
                doc.append(f"- `{assignment_id}`")
            doc.append("")
    
    # Scan Configuration
    if analysis['scan_enabled_assignments'] or analysis['scan_disabled_assignments']:
        doc.append("## Scan Configuration")
        doc.append("")
        
        if analysis['scan_enabled_assignments']:
            doc.append("### Scan-Enabled Assignments")
            doc.append("")
            for assignment_id in sorted(analysis['scan_enabled_assignments']):
                doc.append(f"- `{assignment_id}`")
            doc.append("")
        
        if analysis['scan_disabled_assignments']:
            doc.append("### Scan-Disabled Assignments")
            doc.append("")
            for assignment_id in sorted(analysis['scan_disabled_assignments']):
                doc.append(f"- `{assignment_id}`")
            doc.append("")
    
    # Detailed Assignment Configuration
    if analysis['assignments']:
        doc.append("## Assignment Details")
        doc.append("")
        
        for assignment_id in sorted(analysis['assignments'].keys()):
            config = analysis['assignments'][assignment_id]
            doc.append(f"### `{assignment_id}`")
            doc.append("")
            
            # Codeplug settings
            codeplug = config.get('codeplug', {})
            if codeplug:
                doc.append("**Codeplug:**")
                for key, value in sorted(codeplug.items()):
                    doc.append(f"- `{key}`: {value}")
                doc.append("")
            
            # Zone settings
            zones = config.get('zones', {})
            if zones:
                doc.append("**Zones:**")
                includes = zones.get('include', [])
                excludes = zones.get('exclude', [])
                if includes:
                    doc.append(f"- Include: {', '.join(includes)}")
                if excludes:
                    doc.append(f"- Exclude: {', '.join(excludes)}")
                doc.append("")
            
            # Scan settings
            scan = config.get('scan', {})
            if scan:
                doc.append("**Scan:**")
                for key, value in sorted(scan.items()):
                    doc.append(f"- `{key}`: {value}")
                doc.append("")
            
            # TX settings
            tx = config.get('tx', {})
            if tx:
                doc.append("**TX:**")
                for key, value in sorted(tx.items()):
                    doc.append(f"- `{key}`: {value}")
                doc.append("")
    
    # Usage Information
    doc.append("## Usage")
    doc.append("")
    doc.append("This policy can be used in profiles to override assignment behavior:")
    doc.append("")
    doc.append("```yaml")
    doc.append("profile:")
    doc.append("  policy:")
    doc.append("    files:")
    doc.append(f"      - policies/{analysis['filename']}")
    doc.append("```")
    doc.append("")
    
    return "\n".join(doc)


def generate_index_documentation(policy_analyses: List[Dict[str, Any]]) -> str:
    """Generate an index README for all policy files."""
    
    md = []
    
    # Header
    md.append("# Policy Documentation")
    md.append("")
    md.append("This directory contains automatically generated documentation for all policy files in the project.")
    md.append("")
    
    # Quick Statistics
    total_policies = len(policy_analyses)
    total_assignments = sum(p['assignment_count'] for p in policy_analyses)
    total_zones = len(set().union(*(p['zones'] for p in policy_analyses)))
    total_custom_names = sum(len(p['custom_names']) for p in policy_analyses)
    
    md.append("## Quick Statistics")
    md.append("")
    md.append(f"- **Total Policies:** {total_policies}")
    md.append(f"- **Total Assignment Overrides:** {total_assignments}")
    md.append(f"- **Unique Zones:** {total_zones}")  
    md.append(f"- **Custom Names:** {total_custom_names}")
    md.append("")
    
    # Policy Overview Table
    md.append("## Policy Overview")
    md.append("")
    md.append("| Policy | Assignment Overrides | Zones | Custom Names | Configuration Types |")
    md.append("|--------|---------------------|-------|--------------|-------------------|")
    
    for p in sorted(policy_analyses, key=lambda x: x['name']):
        config_types = []
        if p['has_codeplug_config']:
            config_types.append("Codeplug")
        if p['has_zone_config']:
            config_types.append("Zones")
        if p['has_scan_config']:
            config_types.append("Scan")
        if p['has_tx_config']:
            config_types.append("TX")
        
        config_str = ", ".join(config_types) if config_types else "*None*"
        
        md.append(f"| [{p['name']}]({p['name']}.md) | {p['assignment_count']} | {len(p['zones'])} | {len(p['custom_names'])} | {config_str} |")
    
    md.append("")
    
    # Zone Usage Analysis
    md.append("## Zone Usage Analysis")
    md.append("")
    
    zone_usage = Counter()
    for p in policy_analyses:
        for zone in p['zones']:
            zone_usage[zone] += len(p['zone_assignments'][zone])
    
    if zone_usage:
        md.append("| Zone | Usage Count | Policies |")
        md.append("|------|-------------|----------|")
        
        for zone, count in zone_usage.most_common():
            policies_using_zone = [p['name'] for p in policy_analyses if zone in p['zones']]
            policies_str = ", ".join(policies_using_zone[:3])
            if len(policies_using_zone) > 3:
                policies_str += f" (+{len(policies_using_zone) - 3} more)"
            
            md.append(f"| {zone} | {count} | {policies_str} |")
        
        md.append("")
    
    # Configuration Patterns
    md.append("## Configuration Patterns")
    md.append("")
    
    # Group by configuration types
    codeplug_policies = [p for p in policy_analyses if p['has_codeplug_config']]
    zone_policies = [p for p in policy_analyses if p['has_zone_config']]
    scan_policies = [p for p in policy_analyses if p['has_scan_config']]
    tx_policies = [p for p in policy_analyses if p['has_tx_config']]
    
    if codeplug_policies:
        md.append(f"### Codeplug Configuration ({len(codeplug_policies)} policies)")
        md.append("Policies that modify channel names, RX/TX settings:")
        md.append("")
        for p in codeplug_policies[:10]:  # Show top 10
            md.append(f"- [{p['name']}]({p['name']}.md) ({p['assignment_count']} assignments)")
        if len(codeplug_policies) > 10:
            md.append(f"- *...and {len(codeplug_policies) - 10} more*")
        md.append("")
    
    if zone_policies:
        md.append(f"### Zone Configuration ({len(zone_policies)} policies)")
        md.append("Policies that organize assignments into zones:")
        md.append("")
        for p in zone_policies[:10]:  # Show top 10
            md.append(f"- [{p['name']}]({p['name']}.md) ({len(p['zones'])} zones)")
        if len(zone_policies) > 10:
            md.append(f"- *...and {len(zone_policies) - 10} more*")
        md.append("")
    
    if scan_policies:
        md.append(f"### Scan Configuration ({len(scan_policies)} policies)")
        md.append("Policies that modify scan behavior:")
        md.append("")
        for p in scan_policies[:10]:  # Show top 10
            scan_count = len(p['scan_enabled_assignments']) + len(p['scan_disabled_assignments'])
            md.append(f"- [{p['name']}]({p['name']}.md) ({scan_count} assignments)")
        if len(scan_policies) > 10:
            md.append(f"- *...and {len(scan_policies) - 10} more*")
        md.append("")
    
    # Usage Guide
    md.append("## Using Policies")
    md.append("")
    md.append("Policies provide assignment-level overrides for codeplug generation. They can be used in profiles:")
    md.append("")
    md.append("### Single Policy File")
    md.append("```yaml")
    md.append("profile:")
    md.append("  policy:")
    md.append("    files:")
    md.append("      - policies/gmrs_only.yml")
    md.append("```")
    md.append("")
    md.append("### Multiple Policy Files")
    md.append("```yaml")
    md.append("profile:")
    md.append("  policy:")
    md.append("    files:")
    md.append("      - policies/default.yml")
    md.append("      - policies/chicago_gmrs_repeaters.yml")
    md.append("    paths:")
    md.append("      - policies/chicago/**/*.yml")
    md.append("```")
    md.append("")
    md.append("### Legacy Policy Support")
    md.append("```yaml")
    md.append("# If profile omits policy block, generator looks for:")
    md.append("# policies/<profile_name>.yml")
    md.append("```")
    md.append("")
    
    # Policy Types
    md.append("## Policy Configuration Reference")
    md.append("")
    md.append("### Assignment Overrides")
    md.append("```yaml")
    md.append("policy:")
    md.append("  assignments:")
    md.append("    assignment_id:")
    md.append("      codeplug:")
    md.append("        name: \"Custom Name\"")
    md.append("        rx_only: true/false")
    md.append("        preferred_contacts: [contact_id, ...]")
    md.append("      zones:")
    md.append("        include: [\"Zone 1\", \"Zone 2\"]")
    md.append("        exclude: [\"Zone 3\"]")
    md.append("      scan:")
    md.append("        all_skip: true/false")
    md.append("        zone_skip: true/false")
    md.append("        tot: 30")
    md.append("        power: \"High\"")
    md.append("        vox: true/false")
    md.append("      tx:")
    md.append("        enabled: true/false")
    md.append("```")
    md.append("")
    
    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(
        description="Generate markdown documentation for policy files"
    )
    parser.add_argument(
        "--policies-dir",
        type=pathlib.Path,
        default=POLICIES_ROOT,
        help="Directory containing policy YAML files"
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        default=DEFAULT_DOCS_DIR,
        help="Directory for generated markdown files"
    )
    parser.add_argument(
        "--file",
        help="Generate documentation for specific policy file only"
    )
    parser.add_argument(
        "--list-files",
        action="store_true",
        help="List all available policy files and exit"
    )
    
    args = parser.parse_args()
    
    # Find all policy files
    policy_files = []
    for yml_file in args.policies_dir.glob("*.yml"):
        policy_files.append(yml_file)
    
    if args.list_files:
        # List all available policy files
        print(f"Available policy files ({len(policy_files)} total):")
        print()
        
        # Group by type for better organization
        service_policies = []
        geographic_policies = []
        special_policies = []
        
        for file in sorted(policy_files):
            name = file.stem
            if name in ['default', 'gmrs_only']:
                special_policies.append(file)
            elif any(geo in name for geo in ['chicago', 'berrien', 'laporte', 'tampa', 'florida']):
                geographic_policies.append(file)
            else:
                service_policies.append(file)
        
        if special_policies:
            print("🎯 Special Purpose Policies:")
            for file in special_policies:
                print(f"   {file.name}")
            print()
        
        if geographic_policies:
            print("🌍 Geographic Policies:")
            for file in geographic_policies:
                print(f"   {file.name}")
            print()
        
        if service_policies:
            print("📡 Service/System Policies:")
            for file in service_policies:
                print(f"   {file.name}")
            print()
        
        return
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.file:
        # Generate documentation for specific file
        file_path = args.policies_dir / args.file
        if not file_path.exists():
            file_path = pathlib.Path(args.file)
            if not file_path.exists():
                print(f"Policy file not found: {args.file}")
                print(f"Tried: {args.policies_dir / args.file}")
                if args.file != str(file_path):
                    print(f"Tried: {file_path}")
                return
        
        print(f"Analyzing 1 policy file...")
        analysis = analyze_policy_file(file_path)
        if analysis:
            doc_content = generate_policy_documentation(analysis)
            output_path = args.output_dir / f"{analysis['name']}.md"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(doc_content)
            
            print(f"  → {output_path}")
        else:
            print(f"Failed to analyze {file_path}")
        return
    
    # Generate documentation for all policy files
    print(f"Analyzing {len(policy_files)} policy files...")
    
    policy_analyses = []
    for policy_file in sorted(policy_files):
        print(f"  Analyzing {policy_file.name}")
        analysis = analyze_policy_file(policy_file)
        if analysis:
            policy_analyses.append(analysis)
            
            # Generate individual documentation
            doc_content = generate_policy_documentation(analysis)
            output_path = args.output_dir / f"{analysis['name']}.md"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(doc_content)
            
            print(f"    → {output_path}")
    
    # Generate index documentation
    if policy_analyses:
        index_doc = generate_index_documentation(policy_analyses)
        index_path = args.output_dir / "README.md"
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_doc)
        
        print(f"  → {index_path}")
    
    print(f"\nPolicy documentation generated in: {args.output_dir}")


if __name__ == "__main__":
    main()