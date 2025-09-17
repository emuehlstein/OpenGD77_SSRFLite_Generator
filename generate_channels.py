#!/usr/bin/env python3
import csv, yaml, math, pathlib

BASE = pathlib.Path(__file__).parent

EXPORT_CHANNELS = BASE / "opengd77_cps_export" / "Channels.csv"
IMPORT_CHANNELS = BASE / "opengd77_cps_import_generated" / "Channels.csv"

YAML_FILES = [
    BASE / "cook_county_conventional.yml",
    BASE / "northside_dmr_repeater_info.yml",
    BASE / "chicago_businesses_rf.yml",
    # Added additional service band files
    BASE / "murs_channels.yml",
    BASE / "noaa_weather.yml",
    BASE / "marine_channels.yml",
    BASE / "ham_simplex.yml",
    BASE / "chicagoland_analog_repeaters.yml",
]

HEADER = [
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

# Simplistic zone assignment mapping by tag/group -> zone name (matching existing Zones.csv names where possible)
ZONE_MAP = {
    "Law Tac": "CityOfChicago",
    "Law Dispatch": "CityOfChicago",
    "Corrections": "CityOfChicago",
    "Interop": "CityOfChicago",
    "Emergency Ops": "CityOfChicago",
    "Fire-Tac": "CityOfChicago",
    "EMS-Tac": "CityOfChicago",
    "Public Works": "CityOfChicago",
    "Security": "CityOfChicago",
    "A/V": "CityOfChicago",
    "Hotel": "CityOfChicago",
    "Hotel/Residential": "CityOfChicago",
    "Retail": "CityOfChicago",
    "Business": "CityOfChicago",
}

# For now we don't embed zone column (zones handled in Zones.csv separately). We'll just create channel rows.


def fmt_freq(v):
    if v is None:
        return ""
    return (
        f"{float(v):.5f}".rstrip("0").rstrip(".")
        if "." in f"{float(v):.5f}"
        else f"{float(v):.5f}"
    )


rows = []
chnum = 1

# Helper to add analogue row


def add_analogue(name, rx, tx=None, tone_rx=None, tone_tx=None, bandwidth=None):
    global chnum
    if tx is None:
        tx = rx
    rows.append(
        [
            chnum,
            name,
            "Analogue",
            fmt_freq(rx),
            fmt_freq(tx),
            (bandwidth or ""),
            "",
            "",
            "None",
            "None",
            "None",
            "Off",
            "Off",
            tone_rx or "None",
            tone_tx or ("None" if tone_rx is None else tone_rx),
            "Disabled",
            "Master",
            "No",
            "No",
            "No",
            0,
            "Off",
            "No",
            "No",
            "None",
            0.128,
            0.008,
        ]
    )
    chnum += 1


# Helper to add digital (repeater/simplex) row


def add_digital(
    name, rx, tx=None, cc=1, ts=1, tg_list="None", contact="None", dmr_id="None"
):
    global chnum
    if tx is None:
        tx = rx
    rows.append(
        [
            chnum,
            name,
            "Digital",
            fmt_freq(rx),
            fmt_freq(tx),
            "",
            cc,
            ts,
            contact,
            tg_list,
            dmr_id,
            "Off",
            "Off",
            "",
            "",
            "",
            "Master",
            "No",
            "No",
            "No",
            0,
            "Off",
            "No",
            "No",
            "None",
            0.128,
            0.008,
        ]
    )
    chnum += 1


# Parse YAMLs
for yf in YAML_FILES:
    with open(yf, "r") as f:
        data = yaml.safe_load(f)
    # determine structure keys
    if "cook_county_conventional" in data:
        for group in data["cook_county_conventional"]["channels"]:
            for e in group["entries"]:
                freq = e["freq_mhz"]
                inp = e.get("input_mhz")
                tone = e.get("tone")
                mode = e.get("mode", "FMN")
                name = e.get("alpha_tag")
                # Determine bandwidth: 12.5 for FMN, 25 for FM, blank for digital
                bw = (
                    "12.5" if "FMN" in mode else ("25" if mode.startswith("FM") else "")
                )
                if mode.startswith("DMR"):
                    # Assume repeater if input provided
                    rx = freq
                    tx = inp if inp else freq
                    cc = 1
                    add_digital(
                        name,
                        rx,
                        tx,
                        cc=cc,
                        ts=1,
                        tg_list="ChicagoLand",
                        contact="CL Local 1",
                    )
                else:
                    rx = freq
                    tx = inp if inp else freq
                    tone_rx = None
                    tone_tx = None
                    if tone and tone != "CSQ":
                        # Support PL vs DPL naming
                        tone_clean = tone.replace(" PL", "").replace(" DPL", "")
                        tone_rx = tone_clean
                        tone_tx = tone_clean if inp else tone_clean
                    add_analogue(name, rx, tx, tone_rx, tone_tx, bandwidth=bw)

    if "dmr_repeaters_chicago" in data:
        for rep in data["dmr_repeaters_chicago"]["repeaters"]:
            rx = rep["output_freq_mhz"]
            tx = rep["input_freq_mhz"]
            cc = rep.get("color_code", 1)
            name = rep.get("channel_name", rep["callsign"])
            # Map network to TG List
            network = rep.get("network", "")
            if (
                "Tri-State" in network
                or "Tri-State" in name
                or "TRISTATE" in name.upper()
            ):
                tg_list = "TriState"
                contact = "TRI AllStates"
            elif "Brand" in network:
                tg_list = "Brandmeister"
                contact = "TG 9-1"
            else:
                tg_list = "ChicagoLand"
                contact = "CL Local 1"
            add_digital(name, rx, tx, cc=cc, ts=1, tg_list=tg_list, contact=contact)

    if "chicago_businesses_rf" in data:
        for group in data["chicago_businesses_rf"]["channels"]:
            for e in group["entries"]:
                mode = e.get("mode", "NFM")
                name_base = e.get("alpha_tag")
                freqs = e.get("freq_mhz", [])
                for fq in freqs:
                    if "DMR" in mode and "NFM" not in mode:
                        add_digital(
                            f"{name_base}",
                            fq,
                            fq,
                            cc=1,
                            ts=1,
                            tg_list="None",
                            contact="None",
                        )
                    else:
                        bw = "12.5"
                        add_analogue(f"{name_base}", fq, fq, bandwidth=bw)

    # MURS channels (analogue simplex)
    if "us_murs_channels" in data:
        for ch in data["us_murs_channels"]["channels"]:
            name = ch.get("channel_name", f"MURS {ch.get('ch')}")
            freq = ch["freq_mhz"]
            # Use bandwidth mapping: 11K2F3E -> 12.5, 20K0F3E -> 25
            bw_mode = ch.get("bandwidth")
            if bw_mode == "11K2F3E":
                bw = "12.5"
            elif bw_mode == "20K0F3E":
                bw = "25"
            else:
                bw = "12.5"
            add_analogue(name, freq, freq, bandwidth=bw)

    # NOAA Weather (receive only) – keep in its own zone later; mark as Rx Only by setting Power Master and Rx Only Yes
    if "us_noaa_weather_radio" in data:
        for wx in data["us_noaa_weather_radio"]["frequencies"]:
            name = wx.get("channel_name") or wx.get("wx_channel")
            freq = wx["freq_mhz"]
            # Temporarily add as analogue; after row appended, flip Rx Only flag
            prev_len = len(rows)
            add_analogue(name, freq, freq, bandwidth="12.5")
            # Set Rx Only = Yes for the just-added row
            rows[-1][17] = "Yes"  # Rx Only column

    # Marine VHF channels
    if "us_marine_vhf_channels" in data:
        for mch in data["us_marine_vhf_channels"]["channels"]:
            name = mch.get("channel_name") or f"MRN {mch.get('ch')}"
            freq = mch["freq_mhz"]
            desc = mch.get("description", "")
            # All FM 16K0F3E -> 25 kHz bandwidth typically; keep 25 to differentiate from narrowband
            bw = "25"
            # Duplex public correspondence channels (24,25,26,27,28,84,85,86,87) have ship TX on lower freq (not provided here).
            # Without input frequency data, treat as simplex RX/TX same.
            add_analogue(name, freq, freq, bandwidth=bw)

    # Ham simplex & APRS
    if "ham_simplex_and_aprs" in data:
        hs = data["ham_simplex_and_aprs"]
        # VHF simplex
        if "voice_simplex_vhf" in hs:
            for e in hs["voice_simplex_vhf"].get("entries", []):
                name = e["channel_name"]
                freq = e["freq_mhz"]
                # Standard FM wide -> 25 kHz (legacy) but often narrow now; use 12.5 for modern narrowband amateur FM below 147 per many rigs
                bw = "25" if freq >= 147 else "25"
                add_analogue(name, freq, freq, bandwidth=bw)

    # Chicagoland analogue ham repeaters
    if "cook_county_ham_repeaters" in data:
        reps = data["cook_county_ham_repeaters"].get("repeaters", [])
        for r in reps:
            name = r.get("channel_name")
            rx = r.get("freq_out_mhz")
            tx = r.get("freq_in_mhz") or rx
            tone_field = r.get("tone", "")
            tone_rx = None
            tone_tx = None
            if tone_field:
                # Normalize tone: expect formats like 'CTCSS 107.2 Hz' or 'DCS 023'
                if tone_field.upper().startswith("CTCSS"):
                    # Extract number
                    parts = tone_field.split()
                    for p in parts:
                        if p.replace(".", "").isdigit():
                            tone_rx = p.rstrip("Hz").rstrip()
                            tone_tx = tone_rx
                elif tone_field.upper().startswith(
                    "DCS"
                ) or tone_field.upper().startswith("DPL"):
                    # Keep numeric code
                    code = (
                        tone_field.split()[1]
                        if len(tone_field.split()) > 1
                        else tone_field.split("DCS")[-1]
                    )
                    tone_rx = code
                    tone_tx = code
            # Amateur FM wide assumed 25 kHz
            add_analogue(name, rx, tx, tone_rx=tone_rx, tone_tx=tone_tx, bandwidth="25")
        # UHF simplex
        if "voice_simplex_uhf" in hs:
            for e in hs["voice_simplex_uhf"].get("entries", []):
                name = e["channel_name"]
                freq = e["freq_mhz"]
                bw = "25"
                add_analogue(name, freq, freq, bandwidth=bw)
        # APRS (treat as receive only if desired? we'll keep TX allowed for flexibility)
        if "aprs" in hs:
            for e in hs["aprs"].get("entries", []):
                name = e["channel_name"]
                freq = e["freq_mhz"]
                bw = "25"
                add_analogue(name, freq, freq, bandwidth=bw)

# Write file
IMPORT_CHANNELS.parent.mkdir(parents=True, exist_ok=True)
with open(IMPORT_CHANNELS, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(HEADER)
    for r in rows:
        w.writerow(r)

print(f"Wrote {len(rows)} channels to {IMPORT_CHANNELS}")
