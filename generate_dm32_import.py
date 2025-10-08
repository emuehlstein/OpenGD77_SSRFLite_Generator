#!/usr/bin/env python3
"""
Generate Baofeng DM-32 CPS CSVs from SSRF-Lite YAML inputs under ssrf/.

Outputs (written to dm32_cps_import_generated/):
  - DM32_TalkGroups.csv
  - DM32_Contacts.csv
  - DM32_RXGroupList.csv
  - DM32_Channels.csv
  - DM32_Zone.csv
  - DM32_Scan.csv

Notes and mapping choices:
  - SSRF-Lite contacts with kind "Group" (or missing kind) are exported as TalkGroups (Type = Group Call).
  - SSRF-Lite contacts with kind "Private" are exported to DM32_Contacts.csv (Type = Private Call). If none exist, the file will contain only the header row.
  - For each DMR assignment, we build an RX Group List from codeplug.preferred_contacts and select the first valid one
    as the channel TX Contact; its default_timeslot becomes the channel Time Slot.
  - Channels are created for supported modes: DMR as "Digital"; FM as "Analog". Unsupported modes are skipped.
  - Per-channel Scan List is set to a scan list derived from the first zone (if any). For simplicity, we generate one scan list per zone
    using the zone's membership; otherwise, we set the channel Scan List to "None".
  - Many DM32 CPS columns are set to conservative default values matching the factory export examples or safe import defaults.

Ambiguities (flagged for review):
  - DM32 "DMR ID" column appears to reference a named Radio ID (e.g., "Radio 1") in factory export. We set this to "0" as a neutral default
    since SSRF-Lite does not carry radio identity; you may wish to change this post-import.
  - DM32 APRS-related fields are set to Off/0 and not used.
  - Scan lists are heuristically generated per zone; if you prefer a different policy (none or custom lists), adjust below.
"""

import csv
import pathlib
from typing import Dict, List, Optional, Tuple

try:
    import yaml  # type: ignore
except Exception:
    raise SystemExit("PyYAML is required. Install with: pip install pyyaml")

BASE = pathlib.Path(__file__).parent
SSRF_ROOT = BASE / "ssrf"
OUT_DIR = BASE / "dm32_cps_import_generated"


# Helpers shared with the OpenGD77 generator (duplicated here for isolation)
FORBIDDEN_CHARS = set([",", ";", '"', "'", "<", ">", "\\", "(", ")", "–"])  # noqa: W605


def sanitize_name(name: str) -> str:
    if not isinstance(name, str):
        name = str(name)
    cleaned = "".join(ch for ch in name if ch not in FORBIDDEN_CHARS)
    cleaned = " ".join(cleaned.split())
    return cleaned.strip()


def fmt_freq_mhz(v: Optional[float]) -> str:
    if v is None:
        return ""
    return f"{float(v):.5f}"


def fmt_bw_khz_label(
    emission: Optional[str], fallback_khz: Optional[float], is_dmr: bool
) -> str:
    # DM32 expects e.g., "12.5KHz" or "25KHz"
    if is_dmr:
        return "12.5KHz"
    if fallback_khz:
        val = str(fallback_khz).rstrip("0").rstrip(".")
        return f"{val}KHz"
    if not emission:
        return "12.5KHz"
    e = emission.upper()
    if e.startswith("16K0") or ("F3E" in e and "16K0" in e):
        return "25KHz"
    if e.startswith("11K") or e.startswith("8K50"):
        return "12.5KHz"
    if e.startswith("7K60") or "DMR" in e:
        return "12.5KHz"
    return "12.5KHz"


def fmt_tone(value: Optional[float | str]) -> str:
    if value is None:
        return "None"
    try:
        f = float(value)
        s = f"{f:.1f}"
        return s.rstrip("0").rstrip(".") if "." in s else s
    except Exception:
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
    if not SSRF_ROOT.exists():
        raise SystemExit(f"Missing SSRF root: {SSRF_ROOT}")
    for yf in sorted(
        p
        for p in SSRF_ROOT.rglob("*.yml")
        if "_schema" not in p.parts and p.name != "_defaults.yml"
    ):
        with open(yf, "r") as f:
            doc = yaml.safe_load(f) or {}
        ds.merge(doc)
    return ds


def is_supported_mode(mode: str) -> bool:
    return mode in {"DMR", "FM"}


def in_supported_bands(rx: Optional[float], tx: Optional[float]) -> bool:
    def in_band(f: Optional[float]) -> bool:
        if f is None:
            return False
        return (136.0 <= f <= 174.0) or (400.0 <= f <= 480.0)

    return in_band(rx) and in_band(tx if tx is not None else rx)


def station_latlon(
    ds: Dataset, station_id: Optional[str]
) -> Tuple[Optional[float], Optional[float]]:
    if not station_id:
        return (None, None)
    st = ds.stations.get(station_id)
    if not st:
        return (None, None)
    loc_id = st.get("location_id")
    loc = ds.locations.get(loc_id) if isinstance(loc_id, str) else None
    if not loc:
        return (None, None)
    lat = loc.get("lat")
    lon = loc.get("lon")
    try:
        return (float(lat), float(lon))  # type: ignore
    except Exception:
        return (None, None)


def build_dm32(ds: Dataset):
    # Split contacts into talkgroups (group call) and private contacts
    talkgroups: List[tuple[str, int, str]] = []  # (name, id, type)
    priv_contacts: List[tuple[int, str]] = []  # (id, name)
    contact_lookup: Dict[str, dict] = {}

    for cid, c in sorted(ds.contacts.items(), key=lambda kv: kv[1].get("name", "")):
        name = sanitize_name(c.get("name") or cid)
        number = c.get("number")
        if number is None:
            continue
        kind = (c.get("kind") or "Group").strip().lower()
        if kind == "private":
            priv_contacts.append((int(number), name))
        else:
            # Map kind -> DM32 type label
            tg_type = "Group Call" if kind != "allcall" else "All Call"
            talkgroups.append((name, int(number), tg_type))
        contact_lookup[cid] = c

    # Create RX Group Lists per DMR assignment
    rx_groups: Dict[str, List[str]] = {}

    # Channels and Zones
    channels: List[List[str]] = []
    zones: Dict[str, List[str]] = {}
    scan_lists: Dict[str, List[str]] = (
        {}
    )  # zone-based scan lists: name -> channel names

    ch_no = 1

    for asg in ds.assignments:
        codeplug = asg.get("codeplug", {}) or {}
        asg_name = sanitize_name(codeplug.get("name") or asg.get("id") or f"Ch{ch_no}")
        # DM32 constraint: channel names max 16 chars
        channel_display = asg_name[:16]
        zone_names: List[str] = asg.get("zones", []) or []
        rx_only = bool(codeplug.get("rx_only", False)) or (
            asg.get("usage") == "receive-only"
        )

        # Record zones membership
        for zn in zone_names:
            if not zn:
                continue
            zn_clean = sanitize_name(zn)
            # Use truncated channel name for membership so Zone/Scan match channel label
            zones.setdefault(zn_clean, []).append(channel_display)

        if asg.get("rf_chain_id"):
            chain = ds.rf_chains.get(asg["rf_chain_id"], {})
            mode = (chain.get("mode") or {}).get("type", "").upper()
            tx = (chain.get("tx") or {}).get("freq_mhz")
            rx = (chain.get("rx") or {}).get("freq_mhz")
            if not is_supported_mode(mode) or not in_supported_bands(rx, tx):
                continue

            # Default values common to both types
            power = "High"
            scan_list_name = "None"
            if zone_names:
                scan_list_name = f"Scan {sanitize_name(zone_names[0])[:30]}"
                # We'll populate scan_lists later after all channels are known

            if mode == "DMR":
                # Resolve preferred contacts
                pref_ids: List[str] = codeplug.get("preferred_contacts", []) or []
                pref_names: List[str] = []
                default_contact_name = ""
                default_ts_label = "Slot 1"
                for pcid in pref_ids:
                    c = contact_lookup.get(pcid)
                    if not c or c.get("number") is None:
                        continue
                    if (c.get("kind") or "Group").strip().lower() == "private":
                        continue  # RX Group members should be talkgroups
                    pref_names.append(
                        sanitize_name(c.get("name") or str(c.get("number")))
                    )
                if pref_ids:
                    for pcid in pref_ids:
                        c = contact_lookup.get(pcid)
                        if not c or c.get("number") is None:
                            continue
                        if (c.get("kind") or "Group").strip().lower() == "private":
                            continue
                        default_contact_name = sanitize_name(
                            c.get("name") or str(c.get("number"))
                        )
                        ts = c.get("default_timeslot")
                        if ts in (1, 2):
                            default_ts_label = f"Slot {ts}"
                        break
                if not default_contact_name:
                    # fallback to Site Local if present
                    for name, _, _ in talkgroups:
                        if name.lower() in {"site local", "tg9", "talkaround"}:
                            default_contact_name = name
                            default_ts_label = "Slot 1"
                            break

                # RX Group for this channel/assignment
                if pref_names:
                    rxg_name = f"RXG {asg_name[:26]}"  # aim to keep name short
                    existing = rx_groups.setdefault(rxg_name, [])
                    for nm in pref_names:
                        if nm not in existing:
                            existing.append(nm)
                else:
                    rxg_name = "None"

                bw = fmt_bw_khz_label(
                    (chain.get("tx") or {}).get("emission"),
                    (chain.get("tx") or {}).get("bandwidth_khz"),
                    True,
                )

                row = [
                    ch_no,
                    channel_display,
                    "Digital",
                    fmt_freq_mhz(tx if tx is not None else rx),
                    fmt_freq_mhz(rx),
                    power,
                    bw,
                    scan_list_name,
                    "Always",  # TX Admit
                    "None",  # Emergency System
                    3,  # Squelch Level
                    "Off",  # APRS Report Type
                    1 if rx_only else 0,  # Forbid TX
                    0,  # APRS Receive
                    0,  # Forbid Talkaround
                    0,  # Auto Scan
                    0,  # Lone Work
                    0,  # Emergency Indicator
                    0,  # Emergency ACK
                    0,  # Analog APRS PTT Mode
                    0,  # Digital APRS PTT Mode
                    default_contact_name or "None",  # TX Contact (by name)
                    rxg_name,  # RX Group List (by name)
                    (chain.get("mode") or {}).get("color_code", 1) or 1,
                    default_ts_label,
                    0,  # Encryption
                    "None",  # Encryption ID
                    0,  # APRS Report Channel
                    0,  # Direct Dual Mode
                    0,  # Private Confirm
                    0,  # Short Data Confirm
                    0,  # DMR ID (we don't set a radio id selection)
                    "None",  # CTC/DCS Decode (N/A for DMR)
                    "None",  # CTC/DCS Encode (N/A for DMR)
                    "None",  # Scramble
                    "Carrier/CTC",  # RX Squelch Mode
                    "None",  # Signaling Type
                    "OFF",  # PTT ID
                    0,  # VOX Function
                    0,  # PTT ID Display
                ]
                channels.append(row)
                ch_no += 1

            elif mode == "FM":
                tx_dict = chain.get("tx") or {}
                tones = chain.get("mode") or {}
                ctcss_rx = tones.get("ctcss_rx_hz")
                ctcss_tx = tones.get("ctcss_tx_hz")
                dcs_rx = tones.get("dcs_rx_code")
                dcs_tx = tones.get("dcs_tx_code")
                rx_tone = fmt_tone(ctcss_rx if ctcss_rx is not None else dcs_rx)
                tx_tone = fmt_tone(ctcss_tx if ctcss_tx is not None else dcs_tx)
                bw = fmt_bw_khz_label(
                    tx_dict.get("emission"), tx_dict.get("bandwidth_khz"), False
                )

                row = [
                    ch_no,
                    channel_display,
                    "Analog",
                    fmt_freq_mhz(tx if tx is not None else rx),
                    fmt_freq_mhz(rx),
                    power,
                    bw,
                    scan_list_name,
                    "Allow TX",  # TX Admit
                    "None",  # Emergency System
                    3,  # Squelch Level
                    "Off",  # APRS Report Type
                    1 if rx_only else 0,  # Forbid TX
                    0,  # APRS Receive
                    0,  # Forbid Talkaround
                    0,  # Auto Scan
                    0,  # Lone Work
                    0,  # Emergency Indicator
                    0,  # Emergency ACK
                    0,  # Analog APRS PTT Mode
                    0,  # Digital APRS PTT Mode
                    "None",  # TX Contact
                    "None",  # RX Group List
                    1,  # Color Code (unused)
                    "Slot 1",  # Time Slot (unused)
                    0,  # Encryption
                    "None",  # Encryption ID
                    0,  # APRS Report Channel
                    0,  # Direct Dual Mode
                    0,  # Private Confirm
                    0,  # Short Data Confirm
                    0,  # DMR ID
                    rx_tone,  # CTC/DCS Decode
                    tx_tone if tx_tone != "None" else rx_tone,  # CTC/DCS Encode
                    "None",  # Scramble
                    "Carrier/CTC",  # RX Squelch Mode
                    "None",  # Signaling Type
                    "OFF",  # PTT ID
                    0,  # VOX Function
                    0,  # PTT ID Display
                ]
                channels.append(row)
                ch_no += 1

        # Assignment via channel plan (analog simplex or plan-defined channels)
        elif asg.get("channel_plan_id"):
            plan = ds.channel_plans.get(asg["channel_plan_id"], {})
            ch_name = asg.get("channel_name")
            ch_obj = None
            if isinstance(plan.get("channels"), list):
                for ch in plan["channels"]:
                    if ch.get("name") == ch_name:
                        ch_obj = ch
                        break
            if not ch_obj:
                continue
            freq = ch_obj.get("freq_mhz")
            # Skip if out of supported bands
            if not in_supported_bands(freq, freq):
                continue
            tx_dict = {
                "emission": ch_obj.get("emission"),
                "bandwidth_khz": ch_obj.get("bandwidth_khz"),
            }
            bw = fmt_bw_khz_label(
                tx_dict.get("emission"), tx_dict.get("bandwidth_khz"), False
            )
            power = "High"
            scan_list_name = "None"
            if zone_names:
                scan_list_name = f"Scan {sanitize_name(zone_names[0])[:30]}"

            row = [
                ch_no,
                channel_display,
                "Analog",
                fmt_freq_mhz(freq),
                fmt_freq_mhz(freq),
                power,
                bw,
                scan_list_name,
                "Allow TX",
                "None",
                3,
                "Off",
                1 if rx_only else 0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                "None",
                "None",
                1,
                "Slot 1",
                0,
                "None",
                0,
                0,
                0,
                0,
                0,
                "None",
                "None",
                "None",
                "Carrier/CTC",
                "None",
                "OFF",
                0,
                0,
            ]
            channels.append(row)
            ch_no += 1

    # After creating channels, build zone-based scan lists and update them
    for zname, members in zones.items():
        scan_lists[f"Scan {zname[:30]}"] = list(
            dict.fromkeys(members)
        )  # de-dupe, keep order

    return talkgroups, priv_contacts, rx_groups, channels, zones, scan_lists


def write_csvs(
    talkgroups: List[tuple[str, int, str]],
    priv_contacts: List[tuple[int, str]],
    rx_groups: Dict[str, List[str]],
    channels: List[List[str]],
    zones: Dict[str, List[str]],
    scan_lists: Dict[str, List[str]],
):
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # DM32_TalkGroups.csv
    tg_header = ["No.,Name,ID,Type"]
    # We'll write with csv writer for consistency; but header contains commas
    with open(OUT_DIR / "DM32_TalkGroups.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["No.", "Name", "ID", "Type"])
        for i, (name, tg_id, tg_type) in enumerate(talkgroups, start=1):
            w.writerow([i, name, tg_id, tg_type])

    # DM32_Contacts.csv (Private calls)
    with open(OUT_DIR / "DM32_Contacts.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "No.",
                "ID",
                "Repeater",
                "Name",
                "City",
                "Province",
                "Country",
                "Remark",
                "Type",
                "Alert Call",
            ]
        )
        for i, (cid, name) in enumerate(priv_contacts, start=1):
            w.writerow([i, cid, "", name, "", "", "", "", "Private Call", 0])

    # DM32_RXGroupList.csv
    with open(OUT_DIR / "DM32_RXGroupList.csv", "w", newline="") as f:
        # sample shows "csv (pipe)" comment; we just write CSV with pipe-separated member field
        w = csv.writer(f)
        w.writerow(["No.", "RX Group Name", "Contact Members"])
        for i, (name, members) in enumerate(
            sorted(rx_groups.items(), key=lambda kv: kv[0]), start=1
        ):
            members_s = "|".join(members) + ("|" if members else "")
            w.writerow([i, name, members_s])

    # DM32_Channels.csv
    ch_header = [
        "No.",
        "Channel Name",
        "Channel Type",
        "RX Frequency[MHz]",
        "TX Frequency[MHz]",
        "Power",
        "Band Width",
        "Scan List",
        "TX Admit",
        "Emergency System",
        "Squelch Level",
        "APRS Report Type",
        "Forbid TX",
        "APRS Receive",
        "Forbid Talkaround",
        "Auto Scan",
        "Lone Work",
        "Emergency Indicator",
        "Emergency ACK",
        "Analog APRS PTT Mode",
        "Digital APRS PTT Mode",
        "TX Contact",
        "RX Group List",
        "Color Code",
        "Time Slot",
        "Encryption",
        "Encryption ID",
        "APRS Report Channel",
        "Direct Dual Mode",
        "Private Confirm",
        "Short Data Confirm",
        "DMR ID",
        "CTC/DCS Decode",
        "CTC/DCS Encode",
        "Scramble",
        "RX Squelch Mode",
        "Signaling Type",
        "PTT ID",
        "VOX Function",
        "PTT ID Display",
    ]
    with open(OUT_DIR / "DM32_Channels.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(ch_header)
        for row in channels:
            # Ensure exact number of columns
            if len(row) != len(ch_header):
                raise SystemExit(
                    f"Channel row has {len(row)} columns, expected {len(ch_header)}: {row}"
                )
            w.writerow(row)

    # DM32_Zone.csv
    with open(OUT_DIR / "DM32_Zone.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["No.", "Zone Name", "Channel Members"])
        for i, (zname, members) in enumerate(
            sorted(zones.items(), key=lambda kv: kv[0]), start=1
        ):
            unique = list(dict.fromkeys(members))
            members_s = "|".join(unique)
            w.writerow([i, sanitize_name(zname), members_s])

    # DM32_Scan.csv
    with open(OUT_DIR / "DM32_Scan.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "No.",
                "Scan Name",
                "CTC Scan Mode",
                "Scan Tx Mode",
                "Hang Time",
                "Priority Channel 1",
                "Priority Channel 2",
                "Designed Channel",
                "Priority Sweep Time",
                "Talkback",
                "Channel Members",
            ]
        )
        for i, (sname, members) in enumerate(
            sorted(scan_lists.items(), key=lambda kv: kv[0]), start=1
        ):
            unique = list(dict.fromkeys(members))
            designed = unique[0] if unique else "None"
            members_s = "|".join(unique) + ("|" if unique else "")
            w.writerow(
                [
                    i,
                    sname,
                    "Detection CTC",
                    "Current Channel",
                    3.0,
                    "None",
                    "None",
                    designed,
                    500,
                    0,
                    members_s,
                ]
            )


def main():
    ds = load_dataset()
    talkgroups, priv_contacts, rx_groups, channels, zones, scan_lists = build_dm32(ds)
    write_csvs(talkgroups, priv_contacts, rx_groups, channels, zones, scan_lists)
    print(
        f"Wrote {len(channels)} channels, {len(talkgroups)} talkgroups, {len(priv_contacts)} private contacts, "
        f"{len(rx_groups)} RX groups, {len(zones)} zones, {len(scan_lists)} scan lists to {OUT_DIR}"
    )


if __name__ == "__main__":
    main()
