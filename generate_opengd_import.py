#!/usr/bin/env python3
"""
Generate OpenGD77 CSVs from SSRF-Lite YAML inputs selected via profiles.

Outputs:
    - opengd77_cps_import_generated/Channels.csv
    - opengd77_cps_import_generated/Contacts.csv
    - opengd77_cps_import_generated/TG_Lists.csv
    - opengd77_cps_import_generated/Zones.csv

Notes:
    - Only FM (analogue) and DMR chains are rendered into Channels.csv. Other
        digital modes (D-STAR, C4FM, etc.) are skipped as OpenGD77 does not support them.
    - Zone membership, scan behavior, and transmit defaults come from the policy layer
        declared by the active profile (legacy assignment fields remain supported during migration).
    - For DMR, one channel is created per assignment, using policy-provided preferred
        contacts to choose default Contact/Timeslot. Legacy assignment codeplug helpers are still
        honoured if present.
    - Input files are chosen by profile patterns declared in profiles/*.yml. Profiles may also
        declare policy overlays (glob patterns or explicit files).
"""

import argparse
import copy
import csv
import pathlib
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple, Union

try:
    import yaml  # type: ignore
except Exception:
    raise SystemExit("PyYAML is required. Install with: pip install pyyaml")

BASE = pathlib.Path(__file__).parent
SSRF_ROOT = BASE / "ssrf"
DEFAULT_PROFILES_DIR = BASE / "profiles"
DEFAULT_POLICIES_DIR = BASE / "policies"
DEFAULT_PROFILE_NAME = "default"
DEFAULT_OUT_DIR = BASE / "opengd77_cps_import_generated"


def load_profile(
    profile_name: str, profiles_dir: Union[str, pathlib.Path] = DEFAULT_PROFILES_DIR
) -> dict:
    """Load a profile YAML by name."""

    directory = pathlib.Path(profiles_dir)
    if not directory.exists():
        raise SystemExit(f"Profiles directory not found: {directory}")

    profile_path = directory / f"{profile_name}.yml"
    if not profile_path.exists():
        available = ", ".join(sorted(p.stem for p in directory.glob("*.yml")))
        raise SystemExit(
            f"Profile '{profile_name}' not found in {directory}. Available profiles: {available or 'none'}"
        )

    with open(profile_path, "r") as fh:
        data = yaml.safe_load(fh) or {}

    if not isinstance(data, dict) or "profile" not in data:
        raise SystemExit(
            f"Profile file {profile_path} is missing top-level 'profile' key"
        )

    return data


def _detect_services(path: pathlib.Path) -> Set[str]:
    services: Set[str] = set()
    try:
        with open(path, "r") as fh:
            doc = yaml.safe_load(fh) or {}
    except FileNotFoundError:
        return services

    if isinstance(doc, dict):
        for node in doc.get("stations", []) or []:
            svc = node.get("service")
            if svc:
                services.add(str(svc).lower())
        for node in doc.get("authorizations", []) or []:
            svc = node.get("service")
            if svc:
                services.add(str(svc).lower())

    if services:
        return services

    parts = [segment.lower() for segment in path.parts]
    if "plans" in parts:
        idx = parts.index("plans")
        remainder = parts[idx + 1 :]
        for segment in remainder:
            if segment.endswith(".yml"):
                break
            if len(segment) in {2, 3} and segment.isalpha():
                continue
            services.add(segment)
            break
    elif "systems" in parts and len(parts) >= 2:
        services.add(parts[-2])

    return services


def resolve_ssrf_files(
    profile: dict, base_dir: Union[str, pathlib.Path] = BASE
) -> List[str]:
    """Resolve SSRF YAML files for the given profile definition."""

    profile_block = profile.get("profile") if isinstance(profile, dict) else None
    if not isinstance(profile_block, dict):
        raise SystemExit("Malformed profile: expected 'profile' mapping")

    include_block = profile_block.get("include") or {}
    patterns: Iterable[str] = include_block.get("paths", []) or []
    service_filters = [str(s).lower() for s in (include_block.get("services") or [])]
    base_path = pathlib.Path(base_dir)

    if not patterns:
        return []

    resolved: List[str] = []
    seen: Set[pathlib.Path] = set()
    service_cache: Dict[pathlib.Path, Set[str]] = {}

    for pattern in patterns:
        for match in sorted(base_path.glob(pattern)):
            if not match.is_file() or match in seen:
                continue
            if service_filters:
                services = service_cache.get(match)
                if services is None:
                    services = _detect_services(match)
                    service_cache[match] = services
                if not services.intersection(service_filters):
                    continue
            seen.add(match)
            resolved.append(str(match))

    return resolved


def resolve_policy_files(
    profile: dict, base_dir: Union[str, pathlib.Path] = BASE
) -> List[pathlib.Path]:
    """Resolve policy files declared by the profile.

    Profiles may specify:

    ```yaml
    profile:
      policy:
        files:
          - policies/base.yml
        paths:
          - policies/chicago/**/*.yml
    ```

    The order of files is preserved; later files may override earlier ones.
    """

    profile_block = profile.get("profile") if isinstance(profile, dict) else None
    if not isinstance(profile_block, dict):
        return []

    policy_block = profile_block.get("policy") or {}
    if not isinstance(policy_block, dict):
        return []

    base_path = pathlib.Path(base_dir)
    resolved: List[pathlib.Path] = []
    seen: Set[pathlib.Path] = set()

    explicit_files: Iterable[str] = policy_block.get("files", []) or []
    for rel in explicit_files:
        candidate = pathlib.Path(rel)
        if not candidate.is_absolute():
            candidate = base_path / candidate
        if candidate.is_file() and candidate not in seen:
            resolved.append(candidate)
            seen.add(candidate)

    patterns: Iterable[str] = policy_block.get("paths", []) or []
    for pattern in patterns:
        for match in sorted(base_path.glob(pattern)):
            if match.is_file() and match not in seen:
                resolved.append(match)
                seen.add(match)

    return resolved


def list_profiles(
    profiles_dir: Union[str, pathlib.Path] = DEFAULT_PROFILES_DIR,
) -> List[str]:
    directory = pathlib.Path(profiles_dir)
    if not directory.exists():
        return []
    return sorted(p.stem for p in directory.glob("*.yml"))


def _deep_merge_dict(target: Dict[str, Any], source: Dict[str, Any]) -> None:
    for key, value in source.items():
        if key in target and isinstance(target[key], dict) and isinstance(value, dict):
            _deep_merge_dict(target[key], value)
        else:
            target[key] = copy.deepcopy(value)


class PolicySet:
    """Container for policy directives keyed by assignment ID."""

    def __init__(self) -> None:
        self.assignment_rules: Dict[str, Dict[str, Any]] = {}

    def merge_document(self, document: Dict[str, Any]) -> None:
        block: Any = document
        if isinstance(document, dict):
            if isinstance(document.get("policy"), dict):
                block = document["policy"]
            elif isinstance(document.get("policies"), dict):
                block = document["policies"]
        if not isinstance(block, dict):
            return

        assignments = block.get("assignments")
        if not isinstance(assignments, dict):
            return

        for assignment_id, payload in assignments.items():
            if not isinstance(payload, dict):
                continue
            dest = self.assignment_rules.setdefault(str(assignment_id), {})
            _deep_merge_dict(dest, payload)

    def get_assignment(self, assignment_id: Optional[str]) -> Dict[str, Any]:
        if not assignment_id:
            return {}
        rules = self.assignment_rules.get(str(assignment_id))
        return copy.deepcopy(rules) if isinstance(rules, dict) else {}


def load_policy_documents(paths: Sequence[pathlib.Path]) -> PolicySet:
    policy_set = PolicySet()
    for path in paths:
        if not path.exists():
            raise SystemExit(f"Policy file not found: {path}")
        with path.open("r") as fh:
            doc = yaml.safe_load(fh) or {}
        if isinstance(doc, dict):
            policy_set.merge_document(doc)
    return policy_set


# CSV headers based on OpenGD77 importer
CHANNELS_HEADER = [
    "Channel Number",
    "Channel Name",
    "Channel Type",
    "Rx Frequency",
    "Tx Frequency",
    "Bandwidth (kHz)",
    "Colour Code",
    "Timeslot",
    "Contact",
    "TG List",
    "DMR ID",
    "TS1_TA_Tx",
    "TS2_TA_Tx ID",
    "RX Tone",
    "TX Tone",
    "Squelch",
    "Power",
    "Rx Only",
    "Zone Skip",
    "All Skip",
    "TOT",
    "VOX",
    "No Beep",
    "No Eco",
    "APRS",
    "Latitude",
    "Longitude",
]

CONTACTS_HEADER = ["Contact Name", "ID", "ID Type", "TS Override"]

# TG_Lists: name + 32 contacts
TG_LISTS_HEADER = ["TG List Name"] + [f"Contact{i}" for i in range(1, 33)]

# Zones: name + 80 channels
ZONES_HEADER = ["Zone Name"] + [f"Channel{i}" for i in range(1, 81)]


# CSV rules: sanitize names to exclude: , ; " ' < > \ ( )
FORBIDDEN_CHARS = set([",", ";", '"', "'", "<", ">", "\\", "(", ")", "–"])  # noqa: W605


def sanitize_name(name: str) -> str:
    """Remove forbidden characters and normalize whitespace.

    Applies to Channel names, Zone names, and TG List names.
    """
    if not isinstance(name, str):
        name = str(name)
    # Remove forbidden characters
    cleaned = "".join(ch for ch in name if ch not in FORBIDDEN_CHARS)
    # Collapse excessive whitespace
    cleaned = " ".join(cleaned.split())
    return cleaned.strip()


def fmt_freq(v: Optional[float]) -> str:
    if v is None:
        return ""
    s = f"{float(v):.5f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def fmt_tone(value: Optional[Union[float, str]]) -> str:
    if value is None:
        return "None"
    # If numeric CTCSS (Hz) -> 1 decimal place typical (e.g., 114.8)
    try:
        f = float(value)
        return (f"{f:.1f}").rstrip("0").rstrip(".") if "." in f"{f:.1f}" else f"{f:.1f}"
    except Exception:
        # Treat as DCS code string, zero-pad common 3-digit formats
        s = str(value).strip()
        if s.isdigit() and len(s) < 3:
            s = s.zfill(3)
        return s


class Dataset:
    def __init__(self):
        self.contacts: Dict[str, dict] = {}
        self.rf_chains: Dict[str, dict] = {}
        self.assignments: List[dict] = []
        self.channel_plans: Dict[str, dict] = {}
        self.stations: Dict[str, dict] = {}
        self.locations: Dict[str, dict] = {}
        self.authorizations: Dict[str, dict] = {}

    def merge(self, doc: dict):
        # Accept either with or without top-level "ssrf_lite" wrapper
        top = doc
        if isinstance(doc, dict) and "ssrf_lite" in doc:
            # keep references if needed, but real data blocks are at root in examples
            pass
        for key in [
            "contacts",
            "rf_chains",
            "assignments",
            "channel_plans",
            "stations",
            "locations",
            "authorizations",
        ]:
            if key in doc and isinstance(doc[key], list):
                for item in doc[key]:
                    if not isinstance(item, dict):
                        continue
                    item_id = item.get("id")
                    if key == "assignments":
                        self.assignments.append(item)
                    elif item_id:
                        getattr(self, key)[item_id] = item


def load_dataset(file_paths: Sequence[pathlib.Path]) -> Dataset:
    ds = Dataset()
    for yf in file_paths:
        if not yf.exists():
            raise SystemExit(f"SSRF file not found: {yf}")
        with open(yf, "r") as f:
            doc = yaml.safe_load(f) or {}
        ds.merge(doc)
    return ds


def emission_to_bw_khz(emission: Optional[str], fallback: Optional[float]) -> str:
    # Use explicit bandwidth_khz if available; otherwise derive from emission if possible
    if fallback:
        return str(fallback).rstrip("0").rstrip(".")
    if not emission:
        return ""
    e = emission.upper()
    # Common heuristics
    if e.startswith("16K0") or "F3E" in e and "16K0" in e:
        return "25"
    if e.startswith("11K"):  # narrow FM
        return "12.5"
    if e.startswith("7K60") or "DMR" in e:
        return "12.5"
    if e.startswith("8K50"):
        return "12.5"
    return ""


def build_outputs(
    ds: Dataset,
    policies: Optional[PolicySet] = None,
    allowed_tx_services: Optional[Set[str]] = None,
):
    # Prepare Contacts.csv rows and a lookup by id
    contact_rows: List[List[str]] = []
    contact_by_id: Dict[str, Tuple[str, int, Optional[int]]] = {}
    # Prefer consistent ordering by name
    contact_number_lookup: Dict[str, Tuple[str, int, Optional[int]]] = {}

    for cid, c in sorted(ds.contacts.items(), key=lambda kv: kv[1].get("name", "")):
        name = c.get("name") or cid
        number = c.get("number")
        if number is None:
            # Skip contacts without numeric IDs (not usable in codeplug)
            continue
        id_type = c.get("kind", "Group") or "Group"
        ts_override = c.get("default_timeslot")  # optional
        ts_s = str(ts_override) if ts_override in (1, 2) else ""
        contact_rows.append([name, str(number), id_type, ts_s])
        contact_by_id[cid] = (
            name,
            int(number),
            ts_override if ts_override in (1, 2) else None,
        )
        contact_number_lookup[str(number)] = contact_by_id[cid]

    contact_name_lookup: Dict[str, Tuple[str, int, Optional[int]]] = {}
    for cid, (name, number, ts_override) in contact_by_id.items():
        normalized = sanitize_name(name).lower()
        contact_name_lookup[normalized] = (name, number, ts_override)

    # Channels and Zones
    channels_rows: List[List[str]] = []
    zones: Dict[str, List[str]] = {}
    channel_num = 1

    # TG Lists aggregation: name -> ordered list of contact names (max 32)
    tg_lists: Dict[str, List[str]] = {}

    # Helpers to resolve lat/lon from station/location
    def station_latlon(station_id: Optional[str]) -> Tuple[str, str]:
        if not station_id:
            return ("0", "0")
        st = ds.stations.get(station_id)
        if not st:
            return ("0", "0")
        loc_id = st.get("location_id")
        loc = ds.locations.get(loc_id) if isinstance(loc_id, str) else None
        if not loc:
            return ("0", "0")
        lat = loc.get("lat")
        lon = loc.get("lon")
        if lat is None or lon is None:
            return ("0", "0")
        try:
            return (str(float(lat)), str(float(lon)))
        except Exception:
            return ("0", "0")

    def add_zone_members(zone_names: List[str], channel_name: str):
        for zn in zone_names or []:
            if not zn:
                continue
            zn_clean = sanitize_name(zn)
            zones.setdefault(zn_clean, []).append(channel_name)

    # Band/mode filter helpers
    def is_supported_mode(mode: str) -> bool:
        return mode in {"DMR", "FM"}

    def in_supported_bands(rx: Optional[float], tx: Optional[float]) -> bool:
        # OpenGD77 supports approx 136-174 MHz and 400-480 MHz
        def in_band(f: Optional[float]) -> bool:
            if f is None:
                return False
            return (136.0 <= f <= 174.0) or (400.0 <= f <= 480.0)

        return in_band(rx) and in_band(tx if tx is not None else rx)

    def resolve_policy_overlay(asg: dict) -> Dict[str, Any]:
        policy_data: Dict[str, Any] = {}
        assignment_id = asg.get("id")
        if assignment_id and policies is not None:
            policy_overlay = policies.get_assignment(str(assignment_id))
            if isinstance(policy_overlay, dict):
                policy_data = policy_overlay
        return policy_data

    def resolve_zone_names(asg: dict, policy: Dict[str, Any]) -> List[str]:
        zone_block = policy.get("zones")
        base: List[str] = []

        if isinstance(zone_block, dict):
            include = zone_block.get("include", []) or []
            exclude = set(zone_block.get("exclude", []) or [])
            base.extend(asg.get("zones", []) or [])
            for entry in include:
                if entry not in base:
                    base.append(entry)
            zone_list = [z for z in base if z not in exclude]
        elif isinstance(zone_block, list):
            zone_list = zone_block
        elif isinstance(zone_block, str):
            zone_list = [zone_block]
        else:
            zone_list = asg.get("zones", []) or []

        return [str(z) for z in zone_list if z]

    def infer_assignment_service(asg: dict) -> Optional[str]:
        svc = asg.get("service")
        if isinstance(svc, str) and svc.strip():
            return svc.strip().lower()

        auth_id = asg.get("authorization_id")
        if isinstance(auth_id, str):
            auth = ds.authorizations.get(auth_id)
            if isinstance(auth, dict):
                svc = auth.get("service")
                if isinstance(svc, str) and svc.strip():
                    return svc.strip().lower()

        chain_id = asg.get("rf_chain_id")
        if isinstance(chain_id, str):
            chain = ds.rf_chains.get(chain_id) or {}
            station_id = chain.get("station_id")
            if isinstance(station_id, str):
                station = ds.stations.get(station_id) or {}
                svc = station.get("service")
                if isinstance(svc, str) and svc.strip():
                    return svc.strip().lower()

        plan_id = asg.get("channel_plan_id")
        if isinstance(plan_id, str):
            plan = ds.channel_plans.get(plan_id) or {}
            svc = plan.get("service")
            if isinstance(svc, str) and svc.strip():
                return svc.strip().lower()

        return None

    for asg in ds.assignments:
        policy_overlay = resolve_policy_overlay(asg)
        codeplug_policy = policy_overlay.get("codeplug")
        if not isinstance(codeplug_policy, dict):
            codeplug_policy = {}
        # Legacy support
        legacy_codeplug = asg.get("codeplug", {}) or {}
        codeplug = copy.deepcopy(legacy_codeplug)
        _deep_merge_dict(codeplug, codeplug_policy)
        preferred_override = policy_overlay.get("preferred_contacts")
        if isinstance(preferred_override, list):
            codeplug["preferred_contacts"] = preferred_override
        zone_names: List[str] = resolve_zone_names(asg, policy_overlay)
        scan_block = (
            policy_overlay.get("scan")
            if isinstance(policy_overlay.get("scan"), dict)
            else {}
        )
        tx_block = (
            policy_overlay.get("tx")
            if isinstance(policy_overlay.get("tx"), dict)
            else {}
        )
        # Ensure a non-empty string for channel name
        asg_name = codeplug.get("name") or asg.get("id") or f"Ch{channel_num}"
        asg_name = sanitize_name(asg_name)
        rx_only = bool(codeplug.get("rx_only", False)) or (
            asg.get("usage") == "receive-only"
        )
        if codeplug.get("tx_enabled") is False:
            rx_only = True
        if isinstance(tx_block, dict) and tx_block.get("enabled") is False:
            rx_only = True

        service = infer_assignment_service(asg)
        normalized_service = service.lower() if isinstance(service, str) else None
        if allowed_tx_services is not None:
            can_tx = False
            if normalized_service and normalized_service in allowed_tx_services:
                can_tx = True
            elif normalized_service is None and "amateur" in allowed_tx_services:
                can_tx = True
            if not can_tx:
                rx_only = True

        zone_skip_flag = bool(
            codeplug.get("zone_skip")
            or (scan_block.get("zone_skip") if isinstance(scan_block, dict) else False)
        )
        all_skip = bool(
            codeplug.get("all_skip")
            or (scan_block.get("all_skip") if isinstance(scan_block, dict) else False)
        )
        tot_raw = None
        for key in ("tot_seconds", "tot"):
            value = codeplug.get(key)
            if value is not None:
                tot_raw = value
                break
        if tot_raw is None and isinstance(scan_block, dict):
            tot_raw = scan_block.get("tot")
        try:
            tot_value = int(float(tot_raw)) if tot_raw is not None else 0
        except (TypeError, ValueError):
            tot_value = 0

        raw_power = codeplug.get("power")
        if raw_power is None and isinstance(scan_block, dict):
            raw_power = scan_block.get("power")
        power_setting = sanitize_name(str(raw_power)) if raw_power else "Master"

        raw_squelch = codeplug.get("squelch")
        if raw_squelch is None and isinstance(scan_block, dict):
            raw_squelch = scan_block.get("squelch")
        squelch_setting = sanitize_name(str(raw_squelch)) if raw_squelch else ""

        vox_enabled = bool(
            codeplug.get("vox")
            or (scan_block.get("vox") if isinstance(scan_block, dict) else False)
        )
        vox_setting = "On" if vox_enabled else "Off"

        raw_aprs = codeplug.get("aprs")
        if raw_aprs is None and isinstance(scan_block, dict):
            raw_aprs = scan_block.get("aprs")
        aprs_setting = sanitize_name(str(raw_aprs)) if raw_aprs else "None"

        no_beep_setting = "Yes" if codeplug.get("no_beep") else "No"
        no_eco_setting = "Yes" if codeplug.get("no_eco") else "No"

        # Channel via rf_chain
        if asg.get("rf_chain_id"):
            chain = ds.rf_chains.get(asg["rf_chain_id"]) or {}
            mode = (chain.get("mode") or {}).get("type", "").upper()
            tx = (chain.get("tx") or {}).get("freq_mhz")
            rx = (chain.get("rx") or {}).get("freq_mhz")
            lat_s, lon_s = station_latlon(chain.get("station_id"))

            # Filter: only FM or DMR and within supported bands
            if not is_supported_mode(mode):
                continue
            # For DMR and FM, require frequencies to be in supported bands
            if not in_supported_bands(rx, tx):
                continue

            if mode == "DMR":
                # Determine default contact and timeslot from preferred list
                pref_ids_raw = codeplug.get("preferred_contacts", [])
                if isinstance(pref_ids_raw, list):
                    pref_ids = pref_ids_raw
                elif pref_ids_raw:
                    pref_ids = [pref_ids_raw]
                else:
                    pref_ids = []
                # Resolve names for TG List
                pref_names: List[str] = []
                resolved_prefs: List[Tuple[str, int, Optional[int]]] = []
                default_contact_name = "None"
                default_ts = 1
                for pref in pref_ids:
                    resolved = None
                    if pref in contact_by_id:
                        resolved = contact_by_id[pref]
                    elif isinstance(pref, (int, float)):
                        resolved = contact_number_lookup.get(str(int(pref)))
                    elif isinstance(pref, str) and pref.isdigit():
                        resolved = contact_number_lookup.get(pref)
                    if resolved is None and isinstance(pref, str):
                        normalized = sanitize_name(pref).lower()
                        resolved = contact_name_lookup.get(normalized)
                    if resolved:
                        resolved_prefs.append(resolved)
                        pref_names.append(resolved[0])

                if resolved_prefs:
                    first_name, _, first_ts = resolved_prefs[0]
                    default_contact_name = first_name
                    if first_ts in (1, 2):
                        default_ts = first_ts
                default_contact_override = codeplug.get("default_contact")
                if isinstance(default_contact_override, str):
                    override_value = default_contact_override
                else:
                    override_value = default_contact_override

                if override_value is not None:
                    resolved_override = None
                    if override_value in contact_by_id:
                        resolved_override = contact_by_id[override_value]
                    elif isinstance(override_value, (int, float)):
                        resolved_override = contact_number_lookup.get(
                            str(int(override_value))
                        )
                    elif isinstance(override_value, str) and override_value.isdigit():
                        resolved_override = contact_number_lookup.get(override_value)
                    if resolved_override is None:
                        normalized_override = sanitize_name(str(override_value)).lower()
                        resolved_override = contact_name_lookup.get(normalized_override)

                    if resolved_override:
                        nm, _, ts = resolved_override
                        default_contact_name = nm
                        if ts in (1, 2):
                            default_ts = ts

                # TG List name derived from assignment name (limit 15 chars per rules)
                tgl_name = sanitize_name(
                    codeplug.get("tg_list_name") or asg_name or "DMR"
                )[:15]
                # Store TG list membership (max 32)
                if pref_names:
                    existing = tg_lists.setdefault(tgl_name, [])
                    for nm in pref_names:
                        if nm not in existing and len(existing) < 32:
                            existing.append(nm)
                else:
                    # If no preferred list, default to Site Local if available
                    if "Site Local" in [c[0] for c in contact_by_id.values()]:
                        tg_lists.setdefault(tgl_name, ["Site Local"])  # minimal
                        default_contact_name = "Site Local"
                        default_ts = 1
                    else:
                        tgl_name = "None"
                        default_contact_name = "None"
                        default_ts = 1

                cc = (chain.get("mode") or {}).get("color_code", 1) or 1
                bw = ""  # DMR leaves bandwidth blank in importer

                row = [
                    channel_num,
                    asg_name,
                    "Digital",
                    fmt_freq(rx),
                    fmt_freq(tx) if tx is not None else fmt_freq(rx),
                    bw,
                    cc,
                    default_ts,
                    default_contact_name,
                    tgl_name,
                    "None",  # DMR ID
                    "Off",
                    "Off",
                    "",
                    "",
                    squelch_setting,
                    power_setting,
                    "Yes" if rx_only else "No",
                    "Yes" if zone_skip_flag else "No",
                    "Yes" if all_skip else "No",
                    tot_value,
                    vox_setting,
                    no_beep_setting,
                    no_eco_setting,
                    aprs_setting,
                    lat_s,
                    lon_s,
                ]
                channels_rows.append(row)
                add_zone_members(zone_names, str(asg_name))
                channel_num += 1

            elif mode in {"FM", "APRS", "PACKET", "CW"}:
                tx_dict = chain.get("tx") or {}
                bw = emission_to_bw_khz(
                    tx_dict.get("emission"), tx_dict.get("bandwidth_khz")
                )
                tones = chain.get("mode") or {}
                ctcss_rx = tones.get("ctcss_rx_hz")
                ctcss_tx = tones.get("ctcss_tx_hz")
                dcs_rx = tones.get("dcs_rx_code")
                dcs_tx = tones.get("dcs_tx_code")
                rx_tone = fmt_tone(ctcss_rx if ctcss_rx is not None else dcs_rx)
                tx_tone = fmt_tone(ctcss_tx if ctcss_tx is not None else dcs_tx)

                row = [
                    channel_num,
                    asg_name,
                    "Analogue",
                    fmt_freq(rx),
                    fmt_freq(tx) if tx is not None else fmt_freq(rx),
                    bw,
                    "",
                    "",
                    "None",
                    "None",
                    "None",
                    "Off",
                    "Off",
                    rx_tone,
                    tx_tone if tx_tone != "None" else rx_tone,
                    squelch_setting or "Disabled",
                    power_setting,
                    "Yes" if rx_only else "No",
                    "Yes" if zone_skip_flag else "No",
                    "Yes" if all_skip else "No",
                    tot_value,
                    vox_setting,
                    no_beep_setting,
                    no_eco_setting,
                    aprs_setting,
                    lat_s,
                    lon_s,
                ]
                channels_rows.append(row)
                add_zone_members(zone_names, str(asg_name))
                channel_num += 1
            else:
                # Unsupported mode for OpenGD77 (e.g., D-STAR, C4FM) — skip
                pass

        # Channel via channel_plan
        elif asg.get("channel_plan_id"):
            plan = ds.channel_plans.get(asg["channel_plan_id"]) or {}
            ch_name = asg.get("channel_name")
            # find the channel by name in plan
            freq = None
            bw = "12.5"
            ch_obj = None
            if isinstance(plan.get("channels"), list):
                for ch in plan["channels"]:
                    if ch.get("name") == ch_name:
                        ch_obj = ch
                        freq = ch.get("freq_mhz")
                        break
            # Skip plan channels that lack a usable frequency or fall outside radio bands
            try:
                freq_val = float(freq) if freq is not None else None
            except (TypeError, ValueError):
                freq_val = None
            if freq_val is None or not in_supported_bands(freq_val, freq_val):
                continue
            if ch_obj is not None:
                bw_calc = emission_to_bw_khz(
                    ch_obj.get("emission"), ch_obj.get("bandwidth_khz")
                )
                if bw_calc:
                    bw = bw_calc
            lat_s, lon_s = ("0", "0")
            row = [
                channel_num,
                asg_name,
                "Analogue",
                fmt_freq(freq_val),
                fmt_freq(freq_val),
                bw,  # default narrowband unless specified per channel
                "",
                "",
                "None",
                "None",
                "None",
                "Off",
                "Off",
                "None",
                "None",
                squelch_setting or "Disabled",
                power_setting,
                "Yes" if rx_only else "No",
                "Yes" if zone_skip_flag else "No",
                "Yes" if all_skip else "No",
                tot_value,
                vox_setting,
                no_beep_setting,
                no_eco_setting,
                aprs_setting,
                lat_s,
                lon_s,
            ]
            channels_rows.append(row)
            add_zone_members(zone_names, str(asg_name))
            channel_num += 1

    # Build TG_Lists rows
    tg_list_rows: List[List[str]] = []
    for name in sorted(tg_lists.keys()):
        contacts = tg_lists[name][:32]
        row = [name] + contacts + [""] * (32 - len(contacts))
        tg_list_rows.append(row)

    # Build Zones rows
    zone_rows: List[List[str]] = []
    for zname, members in sorted(zones.items(), key=lambda kv: kv[0]):
        # keep first 80 unique members by insertion order
        unique_members: List[str] = []
        for m in members:
            if m not in unique_members and len(unique_members) < 80:
                unique_members.append(m)
        row = (
            [sanitize_name(zname)] + unique_members + [""] * (80 - len(unique_members))
        )
        zone_rows.append(row)

    return contact_rows, channels_rows, tg_list_rows, zone_rows


def main(argv: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser(
        description="Generate OpenGD77 CSVs from SSRF-Lite data"
    )
    parser.add_argument(
        "--profile", default=DEFAULT_PROFILE_NAME, help="Profile name to load"
    )
    parser.add_argument(
        "--profiles-dir",
        default=str(DEFAULT_PROFILES_DIR),
        help="Directory containing profile YAML files",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUT_DIR),
        help="Directory for generated CSV files",
    )
    parser.add_argument(
        "--list-profiles",
        action="store_true",
        help="List available profiles and exit",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show matched SSRF files for the selected profile and exit",
    )
    parser.add_argument(
        "--tx-service",
        dest="tx_services",
        action="append",
        default=None,
        help=(
            "Allow transmit on the specified service (can be repeated). "
            "Defaults to amateur only."
        ),
    )
    parser.add_argument(
        "--tx-all-services",
        action="store_true",
        help="Allow transmit on every service represented in the data",
    )

    args = parser.parse_args(argv)

    profiles_dir = pathlib.Path(args.profiles_dir)

    if args.list_profiles:
        names = list_profiles(profiles_dir)
        if not names:
            print(f"No profiles found in {profiles_dir}")
        else:
            print("Available profiles:")
            for name in names:
                print(f"  - {name}")
        return

    profile = load_profile(args.profile, profiles_dir)
    matched_files = resolve_ssrf_files(profile)

    if not matched_files:
        raise SystemExit(f"Profile '{args.profile}' matched no SSRF files")

    if args.dry_run:
        print(
            f"Profile '{profile['profile'].get('name', args.profile)}' resolved {len(matched_files)} file(s):"
        )
        for path in matched_files:
            print(f"  - {path}")
        return

    policy_paths = resolve_policy_files(profile)
    if not policy_paths:
        fallback_policy = DEFAULT_POLICIES_DIR / f"{args.profile}.yml"
        if fallback_policy.exists():
            policy_paths = [fallback_policy]

    policy_set: Optional[PolicySet] = None
    if policy_paths:
        policy_set = load_policy_documents(policy_paths)

    if args.tx_all_services:
        allowed_tx_services = None
    else:
        allowed_tx_services = {"amateur"}
        extra_services = args.tx_services or []
        for svc in extra_services:
            if svc is None:
                continue
            allowed_tx_services.add(str(svc).strip().lower())

    ssrf_paths = [pathlib.Path(p) for p in matched_files]
    ds = load_dataset(ssrf_paths)
    contacts, channels, tg_lists, zones = build_outputs(
        ds, policy_set, allowed_tx_services
    )

    output_dir = pathlib.Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write Contacts.csv
    with open(output_dir / "Contacts.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(CONTACTS_HEADER)
        for r in contacts:
            w.writerow(r)

    # Write Channels.csv
    with open(output_dir / "Channels.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(CHANNELS_HEADER)
        for r in channels:
            w.writerow(r)

    # Write TG_Lists.csv
    with open(output_dir / "TG_Lists.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(TG_LISTS_HEADER)
        for r in tg_lists:
            w.writerow(r)

    # Write Zones.csv
    with open(output_dir / "Zones.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(ZONES_HEADER)
        for r in zones:
            w.writerow(r)

    print(
        f"Wrote {len(channels)} channels, {len(contacts)} contacts, {len(tg_lists)} TG lists, and {len(zones)} zones to {output_dir}"
    )

    # Post-write validation for column counts and headers
    def validate_csv(path: pathlib.Path, expected_header: List[str]):
        with open(path, "r", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header != expected_header:
                raise SystemExit(
                    f"Validation failed for {path.name}: header mismatch (got {header}, expected {expected_header})"
                )
            for i, row in enumerate(reader, start=2):
                if len(row) != len(expected_header):
                    raise SystemExit(
                        f"Validation failed for {path.name}: row {i} has {len(row)} cols, expected {len(expected_header)}"
                    )

    validate_csv(output_dir / "Contacts.csv", CONTACTS_HEADER)
    validate_csv(output_dir / "Channels.csv", CHANNELS_HEADER)
    validate_csv(output_dir / "TG_Lists.csv", TG_LISTS_HEADER)
    validate_csv(output_dir / "Zones.csv", ZONES_HEADER)
    print("CSV validation: PASS (headers and column counts correct)")


if __name__ == "__main__":
    main()
