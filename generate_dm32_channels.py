#!/usr/bin/env python3
"""Convert OpenGD77 channel exports into DM-32 CPS compatible Channels.csv."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List


DM32_HEADER: List[str] = [
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


POWER_MAP: Dict[str, str] = {
    "master": "High",
    "high": "High",
    "low": "Low",
    "mid": "Medium",
    "medium": "Medium",
    "turbo": "Turbo",
}


def _clean(value: str | None) -> str:
    if value is None:
        return ""
    stripped = value.strip()
    return "" if not stripped or stripped.lower() == "none" else stripped


def _format_frequency(value: str | None) -> str:
    cleaned = _clean(value)
    if not cleaned:
        return ""
    try:
        return f"{float(cleaned):.5f}"
    except ValueError:
        raise ValueError(f"Invalid frequency value: {value!r}") from None


def _format_bandwidth(value: str | None, is_digital: bool) -> str:
    cleaned = _clean(value)
    if cleaned:
        try:
            bw = float(cleaned)
            # Preserve trailing .5 while dropping redundant zeros
            bw_str = (f"{bw:.1f}" if bw % 1 else f"{bw:.0f}").rstrip("0").rstrip(".")
            return f"{bw_str}KHz"
        except ValueError:
            pass
    # DM-32 CPS expects 12.5KHz for DMR when unset
    return "12.5KHz" if is_digital else "25KHz"


def _pick_power(value: str | None) -> str:
    cleaned = _clean(value).lower()
    return POWER_MAP.get(cleaned, "High" if not cleaned else cleaned.title())


def _pick_tx_admit(is_digital: bool) -> str:
    return "Always" if is_digital else "Allow TX"


def _pick_squelch_level(raw: str | None, is_digital: bool) -> str:
    cleaned = _clean(raw).lower()
    if cleaned.isdigit():
        return cleaned
    return "3" if is_digital else "2"


def _rx_squelch_mode(rx_tone: str, is_digital: bool) -> str:
    if is_digital:
        return "Carrier/CTC"
    return "Carrier/CTC" if rx_tone else "Carrier"


def _time_slot(raw: str | None) -> str:
    cleaned = _clean(raw)
    return "Slot 2" if cleaned == "2" else "Slot 1"


def _vox_flag(raw: str | None) -> str:
    return "1" if _clean(raw).lower() == "on" else "0"


def build_dm32_row(
    index: int,
    row: Dict[str, str],
    default_dmr_id: str | None,
) -> List[str]:
    channel_type_raw = row.get("Channel Type", "")
    is_digital = channel_type_raw.strip().lower().startswith("digital")
    rx_only = _clean(row.get("Rx Only")).lower() == "yes"

    rx_freq = _format_frequency(row.get("Rx Frequency"))
    tx_freq = _format_frequency(row.get("Tx Frequency")) or rx_freq

    rx_tone = _clean(row.get("RX Tone"))
    tx_tone = _clean(row.get("TX Tone")) or rx_tone

    color_code = _clean(row.get("Colour Code")) if is_digital else "0"
    time_slot = _time_slot(row.get("Timeslot")) if is_digital else "Slot 1"

    dmr_id = _clean(row.get("DMR ID")) or (default_dmr_id or "")

    tx_contact = _clean(row.get("Contact")) or ("None")
    rx_group = _clean(row.get("TG List")) or "None"

    return [
        str(index),
        row.get("Channel Name", ""),
        "Digital" if is_digital else "Analog",
        rx_freq,
        tx_freq,
        _pick_power(row.get("Power")),
        _format_bandwidth(row.get("Bandwidth (kHz)"), is_digital),
        "None",
        _pick_tx_admit(is_digital),
        "None",
        _pick_squelch_level(row.get("Squelch"), is_digital),
        "Digital" if is_digital else "Off",
        "1" if rx_only else "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        tx_contact,
        rx_group,
        color_code or ("1" if is_digital else "0"),
        time_slot,
        "0",
        "None",
        "1",
        "0",
        "0",
        "0",
        dmr_id,
        rx_tone or "None",
        tx_tone or "None",
        "None",
        _rx_squelch_mode(rx_tone, is_digital),
        "None",
        "OFF",
        _vox_flag(row.get("VOX")),
        "0",
    ]


def convert_channels(
    input_path: Path,
    output_path: Path,
    default_dmr_id: str | None,
) -> int:
    with input_path.open("r", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(DM32_HEADER)
        for idx, row in enumerate(rows, start=1):
            writer.writerow(build_dm32_row(idx, row, default_dmr_id))

    return len(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert OpenGD77 Channels.csv into DM-32 CPS format",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("opengd77_cps_import_generated/Channels.csv"),
        help="Path to OpenGD77 Channels.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("dm32_cps_import_generated/Channels.csv"),
        help="Destination DM-32 Channels.csv",
    )
    parser.add_argument(
        "--dmr-id",
        dest="dmr_id",
        help="Fallback DMR ID if the source file omits it",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.input.exists():
        raise SystemExit(f"Input file not found: {args.input}")

    written = convert_channels(args.input, args.output, args.dmr_id)
    print(f"Wrote {written} DM-32 channels to {args.output}")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
