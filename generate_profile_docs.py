#!/usr/bin/env python3
"""
Generate markdown documentation for each profile describing the channels, zones, contacts, etc.

This script loads each profile and generates a comprehensive markdown document that shows:
- Profile overview (name, description, included files)
- Channel summary (total counts by service, mode, usage)
- Detailed channel listing with frequencies, tones, notes
- Zone organization
- Contact listings (for DMR)
- Authorization requirements
- Geographic coverage
"""

import argparse
import pathlib
from typing import Dict, List, Set, Optional, Any, Tuple
from collections import defaultdict, Counter
import yaml

# Import from the existing generator
import generate_opengd_import as gen
from ssrf import load_ssrf_document

BASE = pathlib.Path(__file__).parent
DEFAULT_PROFILES_DIR = BASE / "profiles"
DEFAULT_DOCS_DIR = BASE / "docs" / "profiles"


def format_frequency(freq_mhz: Optional[float]) -> str:
    """Format frequency for display."""
    if freq_mhz is None:
        return "N/A"
    return f"{freq_mhz:.4f} MHz"


def format_tone(tone: Optional[float], dcs_code: Optional[str] = None) -> str:
    """Format tone/DCS for display."""
    if dcs_code:
        return f"DCS {dcs_code}"
    elif tone:
        return f"{tone:.1f} Hz"
    else:
        return "None"


def get_channel_display_name(
    assignment, policy_overlay: Dict[str, Any], rf_chain=None, channel_plan_entry=None
) -> str:
    """Get the display name for a channel considering policy overlays."""
    codeplug = policy_overlay.get("codeplug", {})
    if isinstance(codeplug, dict) and codeplug.get("name"):
        return codeplug["name"]

    # Fall back to assignment or RF chain name
    if rf_chain:
        return rf_chain.station_id or assignment.id
    elif channel_plan_entry:
        return channel_plan_entry["name"]
    else:
        return assignment.id


def analyze_profile_data(
    profile_name: str, profiles_dir: pathlib.Path
) -> Dict[str, Any]:
    """Analyze profile data and return structured information."""

    # Load profile
    profile = gen.load_profile(profile_name, profiles_dir)

    # Get matched SSRF files
    matched_files = gen.resolve_ssrf_files(profile)
    ssrf_paths = [pathlib.Path(p) for p in matched_files]

    # Load dataset
    ds = gen.load_dataset(ssrf_paths)

    # Load policies
    policy_paths = gen.resolve_policy_files(profile)
    if not policy_paths:
        fallback_policy = gen.DEFAULT_POLICIES_DIR / f"{profile_name}.yml"
        if fallback_policy.exists():
            policy_paths = [fallback_policy]

    policy_set = None
    if policy_paths:
        policy_set = gen.load_policy_documents(policy_paths)

    # Analyze data
    analysis = {
        "profile": profile["profile"],
        "ssrf_files": matched_files,
        "policy_files": [str(p) for p in policy_paths] if policy_paths else [],
        "organizations": [],
        "locations": list(ds.locations.values()),
        "authorizations": list(ds.authorizations.values()),
        "contacts": list(ds.contacts.values()),
        "channel_plans": list(ds.channel_plans.values()),
        "assignments": [],
        "zones": defaultdict(list),
        "services": set(),
        "modes": Counter(),
        "usage_types": Counter(),
        "frequency_bands": Counter(),
    }

    # Extract organizations from stations (since Dataset doesn't have organizations directly)
    org_ids = set()
    for station in ds.stations.values():
        if station.organization_id:
            org_ids.add(station.organization_id)

    # We'll need to get organizations from the raw SSRF files
    organizations_found = []
    for ssrf_path in ssrf_paths:
        try:
            reference = load_ssrf_document(ssrf_path)
            for org in reference.organizations:
                if org.id in org_ids:
                    organizations_found.append(org)
        except Exception:
            continue
    analysis["organizations"] = organizations_found

    # Helper functions (same as main generator)
    def is_supported_mode(mode: str) -> bool:
        return mode in {"DMR", "FM"}

    def in_supported_bands(rx: Optional[float], tx: Optional[float]) -> bool:
        # OpenGD77 supports approx 136-174 MHz and 400-480 MHz
        def in_band(f: Optional[float]) -> bool:
            if f is None:
                return False
            return (136.0 <= f <= 174.0) or (400.0 <= f <= 480.0)

        return in_band(rx) and in_band(tx if tx is not None else rx)

    # Process assignments
    for assignment in ds.assignments:
        policy_overlay = policy_set.get_assignment(assignment.id) if policy_set else {}

        channel_info = {
            "assignment": assignment,
            "policy": policy_overlay,
            "rf_chain": None,
            "channel_plan_entry": None,
            "display_name": "",
            "frequencies": {"rx": None, "tx": None},
            "mode": "Unknown",
            "tones": {
                "ctcss_tx": None,
                "ctcss_rx": None,
                "dcs_tx": None,
                "dcs_rx": None,
            },
            "service": assignment.service or "unknown",
            "usage": assignment.usage or "unknown",
            "zones": [],
            "notes": assignment.notes or "",
            "location": None,
            "tx_enabled": True,
        }

        # Get RF chain or channel plan data
        if assignment.rf_chain_id:
            rf_chain = ds.rf_chains.get(assignment.rf_chain_id)
            if rf_chain:
                channel_info["rf_chain"] = rf_chain
                channel_info["frequencies"]["rx"] = (
                    rf_chain.rx.freq_mhz if rf_chain.rx else None
                )
                channel_info["frequencies"]["tx"] = (
                    rf_chain.tx.freq_mhz if rf_chain.tx else None
                )
                channel_info["mode"] = (
                    rf_chain.mode.type if rf_chain.mode else "Unknown"
                )

                if rf_chain.mode:
                    channel_info["tones"]["ctcss_tx"] = rf_chain.mode.ctcss_tx_hz
                    channel_info["tones"]["ctcss_rx"] = rf_chain.mode.ctcss_rx_hz
                    channel_info["tones"]["dcs_tx"] = rf_chain.mode.dcs_tx_code
                    channel_info["tones"]["dcs_rx"] = rf_chain.mode.dcs_rx_code

                # Get location info and service from station
                if rf_chain.station_id:
                    station = ds.stations.get(rf_chain.station_id)
                    if station:
                        if station.service:
                            channel_info["service"] = station.service
                        if station.location_id:
                            location = ds.locations.get(station.location_id)
                            if location:
                                channel_info["location"] = location

        elif assignment.channel_plan_id and assignment.channel_name:
            channel_plan = ds.channel_plans.get(assignment.channel_plan_id)
            if channel_plan:
                for ch in channel_plan.channels:
                    if ch.name == assignment.channel_name:
                        channel_info["channel_plan_entry"] = ch
                        channel_info["frequencies"]["rx"] = ch.freq_mhz
                        channel_info["frequencies"]["tx"] = ch.freq_mhz  # Simplex
                        channel_info["mode"] = "FM"  # Default for channel plans
                        # Try to infer service from assignment or authorization
                        if assignment.service:
                            channel_info["service"] = assignment.service
                        elif assignment.authorization_id:
                            auth = ds.authorizations.get(assignment.authorization_id)
                            if auth and auth.service:
                                channel_info["service"] = auth.service
                        break

        # Apply policy overlays
        codeplug = policy_overlay.get("codeplug", {})
        if isinstance(codeplug, dict):
            if "rx_only" in codeplug:
                channel_info["tx_enabled"] = not codeplug["rx_only"]

        # Apply OpenGD77 filtering - skip unsupported modes and out-of-band frequencies
        mode = channel_info["mode"]
        rx_freq = channel_info["frequencies"]["rx"]
        tx_freq = channel_info["frequencies"]["tx"]

        if not is_supported_mode(mode):
            continue  # Skip unsupported modes (D-STAR, C4FM, etc.)

        if not in_supported_bands(rx_freq, tx_freq):
            continue  # Skip out-of-band frequencies

        # Get display name
        channel_info["display_name"] = get_channel_display_name(
            assignment,
            policy_overlay,
            channel_info["rf_chain"],
            channel_info["channel_plan_entry"],
        )

        # Get zones
        zone_block = policy_overlay.get("zones", [])
        if isinstance(zone_block, dict):
            zones = zone_block.get("include", [])
        elif isinstance(zone_block, list):
            zones = zone_block
        elif isinstance(zone_block, str):
            zones = [zone_block]
        else:
            zones = []

        channel_info["zones"] = zones
        for zone in zones:
            analysis["zones"][zone].append(channel_info["display_name"])

        # Update counters
        analysis["services"].add(channel_info["service"])
        analysis["modes"][channel_info["mode"]] += 1
        analysis["usage_types"][channel_info["usage"]] += 1

        # Determine frequency band
        rx_freq = channel_info["frequencies"]["rx"]
        if rx_freq:
            if 136 <= rx_freq <= 174:
                analysis["frequency_bands"]["VHF (136-174 MHz)"] += 1
            elif 400 <= rx_freq <= 480:
                analysis["frequency_bands"]["UHF (400-480 MHz)"] += 1
            elif rx_freq < 136:
                analysis["frequency_bands"]["HF/VLF (<136 MHz)"] += 1
            else:
                analysis["frequency_bands"]["Other (>480 MHz)"] += 1

        analysis["assignments"].append(channel_info)

    # Sort assignments by frequency for display
    analysis["assignments"].sort(key=lambda x: x["frequencies"]["rx"] or 0)

    return analysis


def generate_index_readme(profile_summaries: List[Dict[str, Any]]) -> str:
    """Generate index README with profile summaries."""

    md = []

    # Header
    md.append("# Profile Documentation")
    md.append("")
    md.append(
        "This directory contains automatically generated markdown documentation for each profile in the OpenGD77 SSRF-Lite Generator project."
    )
    md.append("")

    # Quick stats
    total_profiles = len(profile_summaries)
    total_assignments = sum(p["total_assignments"] for p in profile_summaries)
    all_services = set()
    all_modes = set()
    for p in profile_summaries:
        all_services.update(p["services"])
        all_modes.update(p["modes"].keys())

    md.append("## Quick Statistics")
    md.append("")
    md.append(f"- **Total Profiles:** {total_profiles}")
    md.append(f"- **Total Assignments:** {total_assignments:,}")
    md.append(f"- **Services Covered:** {len(all_services)}")
    md.append(f"- **Modes Supported:** {', '.join(sorted(all_modes))}")
    md.append("")

    # Profile comparison table
    md.append("## Profile Comparison")
    md.append("")
    md.append("| Profile | Description | Channels | Services | Zones | Contacts |")
    md.append("|---------|-------------|----------|----------|-------|----------|")

    for profile in sorted(profile_summaries, key=lambda x: x["name"]):
        # Use the filename for display to avoid duplicates
        name_link = f"[{profile['name']}]({profile['name']}.md)"
        description = (
            profile["description"][:60] + "..."
            if len(profile["description"]) > 60
            else profile["description"]
        )
        services = ", ".join(profile["services"][:3])  # Show first 3 services
        if len(profile["services"]) > 3:
            services += f" (+{len(profile['services'])-3} more)"

        md.append(
            f"| {name_link} | {description} | {profile['total_assignments']} | {services} | {profile['zones']} | {profile['contacts']} |"
        )

    md.append("")

    # Detailed profile listing
    md.append("## Available Profiles")
    md.append("")

    for profile in sorted(profile_summaries, key=lambda x: x["name"]):
        md.append(f"### [{profile['name']}]({profile['name']}.md)")
        md.append("")
        if profile["description"]:
            md.append(f"**Description:** {profile['description']}")
            md.append("")

        # Quick stats for this profile
        md.append("**Key Statistics:**")
        md.append(f"- **Channels:** {profile['total_assignments']}")
        md.append(f"- **Services:** {', '.join(profile['services'])}")
        if profile["modes"]:
            mode_summary = ", ".join(
                f"{mode} ({count})"
                for mode, count in list(profile["modes"].items())[:3]
            )
            md.append(f"- **Modes:** {mode_summary}")
        md.append(f"- **Zones:** {profile['zones']}")
        if profile["contacts"] > 0:
            md.append(f"- **Contacts:** {profile['contacts']} (DMR talkgroups)")
        md.append("")

    # Usage instructions
    md.append("## How to Use")
    md.append("")
    md.append("### Generate Codeplug CSV Files")
    md.append("```bash")
    md.append("# Generate with default profile")
    md.append("uv run python generate_opengd_import.py")
    md.append("")
    md.append("# Generate with specific profile")
    md.append("uv run python generate_opengd_import.py --profile chicago_amateur")
    md.append("")
    md.append("# Enable TX on additional services (default is amateur only)")
    md.append(
        "uv run python generate_opengd_import.py --profile chicago_gmrs --tx-service gmrs"
    )
    md.append("```")
    md.append("")

    md.append("### Regenerate This Documentation")
    md.append("```bash")
    md.append("# Generate documentation for all profiles")
    md.append("uv run python generate_profile_docs.py")
    md.append("")
    md.append("# Generate documentation for a specific profile")
    md.append("uv run python generate_profile_docs.py --profile chicago_amateur")
    md.append("```")
    md.append("")

    # Important notes
    md.append("## Important Notes")
    md.append("")
    md.append(
        "- **OpenGD77 Compatibility:** Only FM and DMR modes within 136-174 MHz and 400-480 MHz bands are included"
    )
    md.append(
        "- **Licensing:** Ensure you have appropriate licenses (Amateur, GMRS, etc.) before transmitting"
    )
    md.append(
        "- **Verification:** Always verify frequencies, tones, and permissions before use"
    )
    md.append(
        "- **Updates:** Documentation reflects the current state of SSRF files and policies"
    )
    md.append("")

    md.append("## Profile Selection Guide")
    md.append("")
    md.append("Choose a profile based on your needs:")
    md.append("")
    md.append(
        "- **New to radio programming?** Start with `gmrs_only` or `chicago_light`"
    )
    md.append(
        "- **Amateur radio operator in Chicago?** Use `chicago_amateur` or `chicago_amateur_w_gmrs`"
    )
    md.append("- **GMRS license holder?** Try `chicago_gmrs` or `gmrs_only`")
    md.append("- **Want comprehensive coverage?** Use `default` (largest selection)")
    md.append(
        "- **Specific geographic area?** Check `rolling_prairie_in` or `st_pete_fl` for examples"
    )
    md.append("")

    return "\n".join(md)


def generate_profile_markdown(analysis: Dict[str, Any]) -> str:
    """Generate markdown documentation for a profile."""

    profile_info = analysis["profile"]
    md = []

    # Header
    md.append(f"# Profile: {profile_info.get('name', 'Unknown')}")
    md.append("")

    if profile_info.get("description"):
        md.append(f"**Description:** {profile_info['description']}")
        md.append("")

    # Overview section
    md.append("## Overview")
    md.append("")
    md.append(f"- **Total Assignments:** {len(analysis['assignments'])}")
    md.append(f"- **Services:** {', '.join(sorted(analysis['services']))}")
    md.append(f"- **SSRF Files:** {len(analysis['ssrf_files'])}")
    md.append(f"- **Policy Files:** {len(analysis['policy_files'])}")
    md.append(f"- **Organizations:** {len(analysis['organizations'])}")
    md.append(f"- **Locations:** {len(analysis['locations'])}")
    md.append(f"- **Contacts:** {len(analysis['contacts'])}")
    md.append("")

    # Statistics
    md.append("## Statistics")
    md.append("")

    md.append("### By Mode")
    for mode, count in analysis["modes"].most_common():
        md.append(f"- **{mode}:** {count}")
    md.append("")

    md.append("### By Usage Type")
    for usage, count in analysis["usage_types"].most_common():
        md.append(f"- **{usage.title()}:** {count}")
    md.append("")

    md.append("### By Frequency Band")
    for band, count in analysis["frequency_bands"].most_common():
        md.append(f"- **{band}:** {count}")
    md.append("")

    # Zones
    if analysis["zones"]:
        md.append("## Zones")
        md.append("")
        for zone_name, channels in sorted(analysis["zones"].items()):
            md.append(f"### {zone_name}")
            md.append(f"*{len(channels)} channels*")
            md.append("")
            for channel in channels:
                md.append(f"- {channel}")
            md.append("")

    # Contacts (DMR)
    if analysis["contacts"]:
        md.append("## Contacts")
        md.append("")
        md.append("| Name | ID | Type | Default Slot | Notes |")
        md.append("|------|----|----- |------------- |-------|")

        for contact in sorted(analysis["contacts"], key=lambda x: x.name or ""):
            name = contact.name or "N/A"
            contact_id = contact.number if contact.number is not None else "N/A"
            kind = contact.kind or "Group"
            slot = contact.default_timeslot or "N/A"
            notes = contact.notes or ""
            md.append(f"| {name} | {contact_id} | {kind} | {slot} | {notes} |")
        md.append("")

    # Channel Details
    md.append("## Channel Details")
    md.append("")

    # Group by service
    by_service = defaultdict(list)
    for assignment in analysis["assignments"]:
        by_service[assignment["service"]].append(assignment)

    for service in sorted(by_service.keys()):
        assignments = by_service[service]
        md.append(f"### {service.title()} Service")
        md.append(f"*{len(assignments)} channels*")
        md.append("")

        md.append(
            "| Channel | RX Freq | TX Freq | Mode | Tone | Usage | TX | Zones | Location |"
        )
        md.append(
            "|---------|---------|---------|------|------|-------|----| ------|----------|"
        )

        for assignment in assignments:
            name = assignment["display_name"]
            rx_freq = format_frequency(assignment["frequencies"]["rx"])
            tx_freq = format_frequency(assignment["frequencies"]["tx"])
            mode = assignment["mode"]

            # Format tones
            tone_info = []
            if assignment["tones"]["ctcss_tx"] or assignment["tones"]["ctcss_rx"]:
                tx_tone = (
                    assignment["tones"]["ctcss_tx"] or assignment["tones"]["ctcss_rx"]
                )
                tone_info.append(f"{tx_tone:.1f} Hz")
            if assignment["tones"]["dcs_tx"] or assignment["tones"]["dcs_rx"]:
                dcs_code = (
                    assignment["tones"]["dcs_tx"] or assignment["tones"]["dcs_rx"]
                )
                tone_info.append(f"DCS {dcs_code}")
            tone = ", ".join(tone_info) if tone_info else "None"

            usage = assignment["usage"].title()
            tx_status = "✓" if assignment["tx_enabled"] else "RX Only"
            zones = ", ".join(assignment["zones"]) if assignment["zones"] else ""

            location_str = ""
            if assignment["location"]:
                loc = assignment["location"]
                location_str = f"{loc.name}"
                if loc.lat and loc.lon:
                    location_str += f" ({loc.lat:.4f}, {loc.lon:.4f})"

            md.append(
                f"| {name} | {rx_freq} | {tx_freq} | {mode} | {tone} | {usage} | {tx_status} | {zones} | {location_str} |"
            )

        md.append("")

    # Organizations
    if analysis["organizations"]:
        md.append("## Organizations")
        md.append("")
        for org in sorted(analysis["organizations"], key=lambda x: x.name or ""):
            md.append(f"- **{org.name}** (`{org.id}`)")
        md.append("")

    # Authorizations
    if analysis["authorizations"]:
        md.append("## Authorization Requirements")
        md.append("")
        for auth in sorted(analysis["authorizations"], key=lambda x: x.service or ""):
            md.append(f"### {auth.service or 'Unknown'}")
            md.append(f"- **Authority:** {auth.authority or 'N/A'}")
            if auth.class_:
                md.append(f"- **Class:** {auth.class_}")
            if auth.identifier:
                md.append(f"- **Identifier:** {auth.identifier}")
            if auth.notes:
                md.append(f"- **Notes:** {auth.notes}")
            md.append("")

    # Source Files
    md.append("## Source Files")
    md.append("")

    md.append("### SSRF Files")
    for file_path in analysis["ssrf_files"]:
        rel_path = pathlib.Path(file_path).relative_to(BASE)
        md.append(f"- `{rel_path}`")
    md.append("")

    if analysis["policy_files"]:
        md.append("### Policy Files")
        for file_path in analysis["policy_files"]:
            rel_path = pathlib.Path(file_path).relative_to(BASE)
            md.append(f"- `{rel_path}`")
        md.append("")

    # Notes section
    md.append("## Notes")
    md.append("")
    md.append(
        "- This documentation is automatically generated from SSRF-Lite data and policy files"
    )
    md.append(
        "- **OpenGD77 Filtering Applied**: Only FM and DMR modes within 136-174 MHz and 400-480 MHz bands are included"
    )
    md.append(
        "- Unsupported modes (D-STAR, C4FM, APRS, etc.) and out-of-band frequencies are excluded"
    )
    md.append(
        "- TX enablement depends on profile settings and `--tx-service` flags used during generation"
    )
    md.append(
        "- Frequencies, tones, and other technical details should be verified before use"
    )
    md.append("- Geographic coordinates are approximate and for reference only")
    md.append("")

    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(
        description="Generate markdown documentation for profiles"
    )
    parser.add_argument(
        "--profiles-dir",
        type=pathlib.Path,
        default=DEFAULT_PROFILES_DIR,
        help="Directory containing profile YAML files",
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        default=DEFAULT_DOCS_DIR,
        help="Directory for generated markdown files",
    )
    parser.add_argument(
        "--profile", help="Generate documentation for specific profile only"
    )
    parser.add_argument(
        "--list-profiles", action="store_true", help="List available profiles and exit"
    )

    args = parser.parse_args()

    if args.list_profiles:
        profiles = gen.list_profiles(args.profiles_dir)
        if not profiles:
            print(f"No profiles found in {args.profiles_dir}")
        else:
            print("Available profiles:")
            for profile in profiles:
                print(f"  - {profile}")
        return

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Get profiles to process
    if args.profile:
        profiles = [args.profile]
    else:
        profiles = gen.list_profiles(args.profiles_dir)

    if not profiles:
        print(f"No profiles found in {args.profiles_dir}")
        return

    # Collect profile summaries for index
    profile_summaries = []

    # Process each profile
    for profile_name in profiles:
        print(f"Generating documentation for profile: {profile_name}")

        try:
            analysis = analyze_profile_data(profile_name, args.profiles_dir)
            markdown = generate_profile_markdown(analysis)

            output_file = args.output_dir / f"{profile_name}.md"
            with output_file.open("w") as f:
                f.write(markdown)

            print(f"  → {output_file}")

            # Collect summary for index
            profile_info = analysis["profile"]
            profile_summaries.append(
                {
                    "name": profile_name,
                    "display_name": profile_info.get("name", profile_name),
                    "description": profile_info.get("description", ""),
                    "total_assignments": len(analysis["assignments"]),
                    "services": sorted(analysis["services"]),
                    "modes": dict(analysis["modes"].most_common()),
                    "ssrf_files": len(analysis["ssrf_files"]),
                    "zones": len(analysis["zones"]),
                    "contacts": len(analysis["contacts"]),
                }
            )

        except Exception as e:
            print(f"  ✗ Error processing {profile_name}: {e}")
            continue

    # Generate index README
    if profile_summaries:
        index_readme = generate_index_readme(profile_summaries)
        index_file = args.output_dir / "README.md"
        with index_file.open("w") as f:
            f.write(index_readme)
        print(f"  → {index_file}")

    print(f"\nDocumentation generated in: {args.output_dir}")


if __name__ == "__main__":
    main()
