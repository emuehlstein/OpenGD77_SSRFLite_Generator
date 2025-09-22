# OpenGD77 SSRFLite Generator

A reproducible, data‑driven codeplug builder for OpenGD77 handhelds. The generator ingests SSRF‑Lite YAML files and produces OpenGD77‑compatible CSVs (`Channels.csv`, `Contacts.csv`, `TG_Lists.csv`, `Zones.csv`) suitable for import via the CPS.

Important:

- Receive‑only monitoring of public safety is emphasized. Transmitting where you’re not authorized is illegal. Always follow regulations and owner policies.
- Only modes and bands the OpenGD77 supports are emitted: FM and DMR within 136–174 MHz and 400–480 MHz. Other modes (e.g., D‑STAR, C4FM) and out‑of‑band items are ignored.

SSRF‑Lite reference:

- Project doc: [SSRF‑Lite Spec](./ssrf_lite_systems/SSRF-Lite-Spec.md)
- Background (NTIA SSRF): [https://www.ntia.gov/publications/2023/standard-spectrum-resource-format-ssrf](https://www.ntia.gov/publications/2023/standard-spectrum-resource-format-ssrf)

## What’s New (current state)

- Inputs migrated to SSRF‑Lite under `ssrf_lite_systems/` (assignments, rf_chains, contacts, channel_plans, stations, locations).
- uv is used for dependency management and isolated runs.
- Generator now produces all four CSVs: Channels, Contacts, TG Lists, and Zones.
- Mode/band filtering: only FM/DMR within 136–174 and 400–480 MHz are included.
- Zones are built from `assignments[].zones` in the SSRF‑Lite data.

## Repository Structure

```text
.
├── generate_opengd_import.py            # Main generator: SSRF‑Lite → OpenGD77 CSVs
├── pyproject.toml                       # Dependencies (managed with uv)
├── ssrf_lite_systems/                   # All SSRF‑Lite inputs (YAML) and spec
│   ├── ns9rc_repeaters.yml
│   ├── chicagoland_dmr_system.yml
│   ├── cfmc_repeaters.yml
│   ├── sara_repeaters.yml
│   ├── us_gmrs_channels.yml
│   ├── us_murs_channels.yml
│   ├── us_ham_vhf_simplex.yml           # 2m simplex + calling
│   ├── us_ham_uhf_simplex.yml           # 70cm simplex + calling
│   ├── us_marine_vhf_channels.yml       # US Marine VHF channel plan + assignments
│   ├── noaa_weather.yml                 # NOAA Weather WX1–WX7 (RX-only)
│   ├── il_statewide_interop.yml         # IL interop (IFERN/IREACH/ISPERN/VCALL/VTAC/UCALL/UTAC), RX-only
│   ├── rail_aar_scan.yml                # Railroads – AAR VHF scan set (RX-only)
│   ├── rosehill_cemetery_dmr.yml        # Rosehill Cemetery DMR (RX-only pending verification)
│   └── chicago_police_department.yml    # CPD analogue Citywide + VHF c2c (RX-only)
│   ├── cook_county_interop.yml          # Cook County Interop VHF/UHF (RX-only)
│   └── chicago_fire_ems_northside.yml   # CFD analogue + Northside Fire/EMS (RX-only)
│   └── chicago_businesses_northside.yml  # curated northside business/property ops
│   └── us_itinerant_business.yml         # US common itinerant/business FM simplex (RX-only)
│   └── venues_chicago.yml                # Venues – Chicago (RX-only)
│   └── public_works_parks.yml            # Public Works & Parks (RX-only)
│   └── transit_transport.yml             # Transit & Transport (RX-only)
├── opengd77_cps_import_generated/       # Fresh CSV outputs from the generator
```

## SSRF-Lite Systems

All SSRF‑Lite inputs live under `ssrf_lite_systems/`:

- `ssrf_lite_systems/SSRF-Lite-Spec.md`
- `ssrf_lite_systems/cfmc_repeaters.yml`
- `ssrf_lite_systems/chicago_businesses_northside.yml`
- `ssrf_lite_systems/chicago_fire_ems_northside.yml`
- `ssrf_lite_systems/chicago_police_department.yml`
- `ssrf_lite_systems/chicagoland_dmr_system.yml`
- `ssrf_lite_systems/cook_county_interop.yml`
- `ssrf_lite_systems/il_statewide_interop.yml`
- `ssrf_lite_systems/noaa_weather.yml`
- `ssrf_lite_systems/ns9rc_repeaters.yml`
- `ssrf_lite_systems/public_works_parks.yml`
- `ssrf_lite_systems/rail_aar_scan.yml`
- `ssrf_lite_systems/rosehill_cemetery_dmr.yml`
- `ssrf_lite_systems/sara_repeaters.yml`
- `ssrf_lite_systems/transit_transport.yml`
- `ssrf_lite_systems/us_gmrs_channels.yml`
- `ssrf_lite_systems/us_ham_dmr_simplex.yml`
- `ssrf_lite_systems/us_ham_uhf_simplex.yml`
- `ssrf_lite_systems/us_ham_vhf_simplex.yml`
- `ssrf_lite_systems/us_itinerant_business.yml`
- `ssrf_lite_systems/us_marine_vhf_channels.yml`
- `ssrf_lite_systems/us_murs_channels.yml`
- `ssrf_lite_systems/venues_chicago.yml`

Generated zones now include examples like `Marine`, `Ham VHF`, `Ham UHF`, `Ham-Repeaters`, `GMRS`, `MURS`, `NOAA Weather`, `IL Interop`, `Rail – AAR`, `Local-Commercial`, `Chicago PD`, `Cook Interop`, `Fire/EMS`, `US Itinerant`, `Ham DMR Simplex`, `Venues – Chicago`, `Public Works & Parks`, and `Transit & Transport`.

## How It Works

The generator loads and merges SSRF‑Lite YAMLs, then:

- Builds `Contacts.csv` from `contacts[]` (only items with numeric IDs are emitted).
- Builds `Channels.csv` from `assignments[]`:
  - If `rf_chain_id` is set and the chain is FM or DMR, within supported bands:
    - FM/APRS/Packet/CW are emitted as Analogue channels. CTCSS/DCS are mapped to `RX Tone`/`TX Tone`. Bandwidth derived from `tx.bandwidth_khz` or from emission.
    - DMR chains are emitted as Digital channels with Colour Code and a default Timeslot. If `codeplug.preferred_contacts` exists, the first valid one becomes the default Contact/TS.
  - If `channel_plan_id` is set, the matching plan channel is emitted as Analogue (e.g., NOAA), subject to band filter.
- Builds `TG_Lists.csv` from `codeplug.preferred_contacts` per assignment (max 32, list name derived from assignment name).
- Builds `Zones.csv` from `assignments[].zones` (max 80 channels per zone).

Unsupported modes (e.g., D‑STAR, C4FM) and out‑of‑band items are skipped.

## Setup and Usage (uv)

Requirements:

- Python 3.10+
- uv installed (Homebrew or official installer)

Install dependencies and run:

```zsh
uv sync
uv run python generate_opengd_import.py
```

Expected output:

```text
Wrote <channels> channels, <contacts> contacts, <tg_lists> TG lists, and <zones> zones to opengd77_cps_import_generated
CSV validation: PASS (headers and column counts correct)
```

Import the generated CSVs into OpenGD77 CPS.

## Data Notes & Conventions

- SSRF‑Lite entities used here: `organizations`, `locations`, `stations`, `antennas`, `rf_chains`, `contacts`, `channel_plans`, `assignments`.
- `assignments.codeplug.name` becomes the channel name. `assignments.zones` populate `Zones.csv`.
- For DMR, `mode.color_code` sets Colour Code; default Timeslot derived from the first preferred contact’s TS if present.
- Latitude/Longitude is taken from the channel’s station → location linkage if available.
- DCS codes are normalized to numeric; we can preserve leading zeros (e.g., 073) if desired.

## Limitations / Roadmap

- Only FM and DMR within 136–174 & 400–480 MHz are emitted.
- Other digital modes (D‑STAR, C4FM) aren’t exported to OpenGD77 CSVs.
- TG lists are derived per assignment; project‑wide curated lists can be added later.
- Additional SSRF‑Lite systems can be dropped into `ssrf_lite_systems/` and will be included automatically.

## Safety / Compliance

- Monitor public safety and business frequencies only if permitted; transmit only where licensed/authorized.
- Verify tones, offsets, and activity; data may change.

## Contributing

1. Create a branch
2. Edit or add SSRF‑Lite YAML in `ssrf_lite_systems/`
3. `uv run python generate_opengd_import.py` and review diffs
4. Update docs/tests as needed and open a PR

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](./LICENSE) file for details.

## Attribution

Thanks to local clubs/directories and NTIA SSRF as a reference model.
