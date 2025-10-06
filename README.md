# OpenGD77 SSRFLite Generator

A reproducible, data‑driven codeplug builder for OpenGD77 handhelds. The generator ingests SSRF‑Lite YAML files and produces OpenGD77‑compatible CSVs (`Channels.csv`, `Contacts.csv`, `TG_Lists.csv`, `Zones.csv`) suitable for import via the CPS.

## SSRF‑Lite:

This project includes a proposed format for sharing information about RF systems, "SSRF-Lite," which is a simplified and yamlized version of the SSRF format used by the US DoD.

- Project doc: [SSRF‑Lite Spec](./ssrf_lite_systems/SSRF-Lite-Spec.md)
- Background (NTIA SSRF): [https://www.ntia.gov/publications/2023/standard-spectrum-resource-format-ssrf](https://www.ntia.gov/publications/2023/standard-spectrum-resource-format-ssrf)



## Repository Structure

- `generate_opengd_import.py` – Converts SSRF-Lite YAML inputs into OpenGD77 CPS CSVs.
- `generate_dm32_import.py` – Builds a Baofeng DM-32 CPS CSV bundle. (experimental/bad)
- `ssrf_lite_systems/` – Source SSRF-Lite datasets (`*.yml`) plus `SSRF-Lite-Spec.md` documentation.
- `opengd77_cps_import_generated/` – Committed OpenGD77 CSV outputs (one file per CPS import requirement).
- `dm32_cps_import_generated/` – Committed Baofeng DM-32 CSV outputs generated from the same inputs.
- `DM32_reference/` – Factory DM-32 CPS export kept for column naming and value reference.
- `opengd_import_csv_file_rules.txt` – Notes on column expectations for OpenGD77 imports.
- `pyproject.toml`, `uv.lock` – Project dependencies managed via `uv`.
- `README.md`, `LICENSE`, `NOTICE` – Documentation and licensing.

## SSRF-Lite Systems

All SSRF‑Lite inputs live under `ssrf_lite_systems/`:

- `ssrf_lite_systems/SSRF-Lite-Spec.md`
- `ssrf_lite_systems/cfmc_repeaters.yml`
- `ssrf_lite_systems/chicago_businesses_northside.yml`
- `ssrf_lite_systems/chicago_ems_services.yml`
- `ssrf_lite_systems/chicago_fire_ems_northside.yml`
- `ssrf_lite_systems/chicago_gmrs_repeaters.yml`
- `ssrf_lite_systems/chicago_police_department.yml`
- `ssrf_lite_systems/chicagoland_dmr_system.yml`
- `ssrf_lite_systems/cook_county_interop.yml`
- `ssrf_lite_systems/il_statewide_interop.yml`
- `ssrf_lite_systems/laporte_county_amateur_radio_club.yml`
- `ssrf_lite_systems/n9iaa_aresc_network.yml`
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
- `ssrf_lite_systems/us_mi_kc8brs_four_flags.yml`
- `ssrf_lite_systems/us_murs_channels.yml`
- `ssrf_lite_systems/venues_chicago.yml`

Generated zones now include examples like `Chicago EMS`, `Chicago PD`, `Cook Interop`, `Emergency`, `Fire/EMS`, `GMRS`, `Ham DMR Simplex`, `Ham-DMR`, `Ham-Repeaters`, `Ham UHF`, `Ham VHF`, `IL Interop`, `Local-Commercial`, `Marine`, `MURS`, `NOAA Weather`, `Public Works & Parks`, `Rail AAR`, `Transit & Transport`, `UHF Simplex`, `US Itinerant`, `VHF Simplex`, and `Venues Chicago`.

Emergency zone:

- A compact `Emergency` zone has been added to group practical, licensed‑use calling and assistance channels:
  - Amateur: `CFMC 2m FM`, `CFMC 440 FM`, `K9JSI VHF`, `N9IAA VHF`, `NS9RC 2m FM`, `NS9RC 440`, `KA9HHH VHF`, `KA9HHH UHF`, plus simplex calling channels `2m Call (146.520)` and `70cm Call (446.000)`.
  - GMRS: `GMRS 20 (462.6750)` simplex for cross‑service monitoring when licensed.

Notes:

- Transmit only if you hold the appropriate license (Amateur/GMRS) and follow local coordination and emergency traffic practices.

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
