#!/usr/bin/env python3
"""
Generate OpenGD77 CSVs from SSRF-Lite YAML inputs under ssrf_lite_systems/.

Outputs:
  - opengd77_cps_import_generated/Channels.csv
  - opengd77_cps_import_generated/Contacts.csv
  - opengd77_cps_import_generated/TG_Lists.csv
  - opengd77_cps_import_generated/Zones.csv

Notes:
  - Only FM (analogue) and DMR chains are rendered into Channels.csv. Other
    digital modes (D-STAR, C4FM, etc.) are skipped as OpenGD77 does not support them.
  - Zones are taken from assignments[].zones.
  - For DMR, one channel is created per assignment, using the first
    codeplug.preferred_contacts (if provided) as the default Contact and Timeslot,
    with a TG List containing all preferred contacts for that assignment.
"""

import csv
import math
import pathlib
from typing import Dict, List, Optional, Tuple, Union

try:
    import yaml  # type: ignore
except Exception:
    raise SystemExit("PyYAML is required. Install with: pip install pyyaml")

BASE = pathlib.Path(__file__).parent
INPUT_DIR = BASE / "ssrf_lite_systems"
OUT_DIR = BASE / "opengd77_cps_import_generated"

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


def load_dataset() -> Dataset:
    ds = Dataset()
    if not INPUT_DIR.exists():
        raise SystemExit(f"Missing input directory: {INPUT_DIR}")
    for yf in sorted(INPUT_DIR.glob("*.yml")):
        with open(yf, "r") as f:
            doc = yaml.safe_load(f) or {}
        # Some files may put SSRF-Lite arrays at root
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


def build_outputs(ds: Dataset):
    # Prepare Contacts.csv rows and a lookup by id
    contact_rows: List[List[str]] = []
    contact_by_id: Dict[str, Tuple[str, int, Optional[int]]] = {}
    # Prefer consistent ordering by name
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
            zones.setdefault(zn, []).append(channel_name)

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

    for asg in ds.assignments:
        codeplug = asg.get("codeplug", {}) or {}
        # Ensure a non-empty string for channel name
        asg_name = codeplug.get("name") or asg.get("id") or f"Ch{channel_num}"
        zone_names: List[str] = asg.get("zones", []) or []
        rx_only = bool(codeplug.get("rx_only", False)) or (
            asg.get("usage") == "receive-only"
        )

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
                pref_ids: List[str] = codeplug.get("preferred_contacts", []) or []
                # Resolve names for TG List
                pref_names: List[str] = []
                default_contact_name = "None"
                default_ts = 1
                for pcid in pref_ids:
                    if pcid in contact_by_id:
                        nm, _, ts = contact_by_id[pcid]
                        pref_names.append(nm)
                if pref_ids:
                    # pick first valid preferred contact as default
                    for pcid in pref_ids:
                        if pcid in contact_by_id:
                            nm, _, ts = contact_by_id[pcid]
                            default_contact_name = nm
                            if ts in (1, 2):
                                default_ts = ts
                            break
                # TG List name derived from assignment name (limit 15 chars per rules)
                tgl_name = (asg_name or "DMR").replace("/", "-")[:15]
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
                    "",
                    "Master",
                    "Yes" if rx_only else "No",
                    "No",
                    "No",
                    0,
                    "Off",
                    "No",
                    "No",
                    "None",
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
                    "Disabled",
                    "Master",
                    "Yes" if rx_only else "No",
                    "No",
                    "No",
                    0,
                    "Off",
                    "No",
                    "No",
                    "None",
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
            if isinstance(plan.get("channels"), list):
                for ch in plan["channels"]:
                    if ch.get("name") == ch_name:
                        freq = ch.get("freq_mhz")
                        break
            lat_s, lon_s = ("0", "0")
            row = [
                channel_num,
                asg_name,
                "Analogue",
                fmt_freq(freq),
                fmt_freq(freq),
                "12.5",  # defaults narrowband for NOAA etc.
                "",
                "",
                "None",
                "None",
                "None",
                "Off",
                "Off",
                "None",
                "None",
                "Disabled",
                "Master",
                "Yes" if rx_only else "No",
                "No",
                "No",
                0,
                "Off",
                "No",
                "No",
                "None",
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
        row = [zname] + unique_members + [""] * (80 - len(unique_members))
        zone_rows.append(row)

    return contact_rows, channels_rows, tg_list_rows, zone_rows


def main():
    ds = load_dataset()
    contacts, channels, tg_lists, zones = build_outputs(ds)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Write Contacts.csv
    with open(OUT_DIR / "Contacts.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(CONTACTS_HEADER)
        for r in contacts:
            w.writerow(r)

    # Write Channels.csv
    with open(OUT_DIR / "Channels.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(CHANNELS_HEADER)
        for r in channels:
            w.writerow(r)

    # Write TG_Lists.csv
    with open(OUT_DIR / "TG_Lists.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(TG_LISTS_HEADER)
        for r in tg_lists:
            w.writerow(r)

    # Write Zones.csv
    with open(OUT_DIR / "Zones.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(ZONES_HEADER)
        for r in zones:
            w.writerow(r)

    print(
        f"Wrote {len(channels)} channels, {len(contacts)} contacts, {len(tg_lists)} TG lists, and {len(zones)} zones to {OUT_DIR}"
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

    validate_csv(OUT_DIR / "Contacts.csv", CONTACTS_HEADER)
    validate_csv(OUT_DIR / "Channels.csv", CHANNELS_HEADER)
    validate_csv(OUT_DIR / "TG_Lists.csv", TG_LISTS_HEADER)
    validate_csv(OUT_DIR / "Zones.csv", ZONES_HEADER)
    print("CSV validation: PASS (headers and column counts correct)")


if __name__ == "__main__":
    main()
