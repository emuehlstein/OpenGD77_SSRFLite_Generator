# OpenGD77 SSRFLite Generator

A reproducible, data‑driven codeplug builder for OpenGD77 handhelds. The generator ingests SSRF‑Lite YAML files and produces OpenGD77‑compatible CSVs (`Channels.csv`, `Contacts.csv`, `TG_Lists.csv`, `Zones.csv`) suitable for import via the CPS.

## SSRF‑Lite

This project includes a proposed format for sharing information about RF systems, "SSRF-Lite," which is a simplified and yamlized version of the SSRF format used by the US DoD.

- Project doc: [SSRF‑Lite Spec](./ssrf/_schema/SSRF-Lite-Spec.md)
- Background (NTIA SSRF): [https://www.ntia.gov/publications/2023/standard-spectrum-resource-format-ssrf](https://www.ntia.gov/publications/2023/standard-spectrum-resource-format-ssrf)



## Repository Structure

- `generate_opengd_import.py` – Converts SSRF-Lite YAML inputs into OpenGD77 CPS CSVs (now profile-aware).
- `generate_dm32_import.py` – Builds a Baofeng DM-32 CPS CSV bundle. (experimental/bad)
- `ssrf/` – SSRF-Lite content split into reusable channel plans and location-bound systems.
- `opengd77_cps_import_generated/` – Committed OpenGD77 CSV outputs (one file per CPS import requirement).
- `dm32_cps_import_generated/` – Committed Baofeng DM-32 CSV outputs generated from the same inputs.
- `DM32_reference/` – Factory DM-32 CPS export kept for column naming and value reference.
- `opengd_import_csv_file_rules.txt` – Notes on column expectations for OpenGD77 imports.
- `pyproject.toml`, `uv.lock` – Project dependencies managed via `uv`.
- `README.md`, `LICENSE`, `NOTICE` – Documentation and licensing.

## SSRF Data Layout

```text
ssrf/
  _schema/                # Docs/specs (SSRF-Lite-Spec.md)
  _defaults.yml           # Reserved for future inheritance defaults
  plans/                  # Portable channel plans (country-agnostic except naming)
    gmrs/
      gmrs_channels.yml
    amateur/
      ham_vhf_simplex.yml
      ham_uhf_simplex.yml
      ham_dmr_simplex.yml
    murs/
      murs_channels.yml
    marine/
      marine_vhf_channels.yml
    business/
      itinerant_business.yml
    weather/
      noaa_weather.yml
    rail/
      rail_aar_scan.yml
  systems/                # Location-bound systems organised by country/state/county/city
    US/
      IL/
        Cook/
          Chicago/
            amateur/
            gmrs/
            public_safety/
            business/
            public_works/
            transit/
          _Countywide/
            public_safety/
      IN/
        LaPorte/LaPorte/amateur/
        Northwest/Regional/amateur/
      MI/
        Berrien/Niles/amateur/
```

Channel content is unchanged—files were simply moved into the new hierarchy to clarify what is reusable (plans) versus location-bound (systems). File names keep their descriptive prefixes so the prior naming references still make sense.

Generated zones now include examples like `Chicago EMS`, `Chicago PD`, `Cook Interop`, `Emergency`, `Fire/EMS`, `GMRS`, `Ham DMR Simplex`, `Ham-DMR`, `Ham-Repeaters`, `Ham UHF`, `Ham VHF`, `IL Interop`, `Local-Commercial`, `Marine`, `MURS`, `NOAA Weather`, `Public Works & Parks`, `Rail AAR`, `Transit & Transport`, `UHF Simplex`, `US Itinerant`, `VHF Simplex`, and `Venues Chicago`.

Generated zones now include examples like `Chicago EMS`, `Chicago PD`, `Cook Interop`, `Emergency`, `Fire/EMS`, `GMRS`, `Ham DMR Simplex`, `Ham-DMR`, `Ham-Repeaters`, `Ham UHF`, `Ham VHF`, `IL Interop`, `Local-Commercial`, `Marine`, `MURS`, `NOAA Weather`, `Public Works & Parks`, `Rail AAR`, `Transit & Transport`, `UHF Simplex`, `US Itinerant`, `VHF Simplex`, and `Venues Chicago`.

Emergency zone:

- A compact `Emergency` zone has been added to group practical, licensed‑use calling and assistance channels:
  - Amateur: `CFMC 2m FM`, `CFMC 440 FM`, `K9JSI VHF`, `N9IAA VHF`, `NS9RC 2m FM`, `NS9RC 440`, `KA9HHH VHF`, `KA9HHH UHF`, plus simplex calling channels `2m Call (146.520)` and `70cm Call (446.000)`.
  - GMRS: `GMRS 20 (462.6750)` simplex for cross‑service monitoring when licensed.

Notes:

- Transmit only if you hold the appropriate license (Amateur/GMRS) and follow local coordination and emergency traffic practices.

## Profiles (Basic)

Profiles provide simple selectors for subsets of SSRF files (no inheritance or overrides yet). Each profile lives in `profiles/<name>.yml` and declares glob patterns plus optional service filters.

Available starter profiles:

- `default` – broad build with national plans and Chicago-area systems.
- `chicago_light` – slim scan list focused on GMRS and public safety.
- `chicago_amateur` – Chicago amateur repeaters plus simplex plans.
- `chicago_gmrs` – Chicago GMRS repeaters and national GMRS plan.

Inspect the available profiles:

```zsh
uv run python generate_opengd_import.py --list-profiles
```

Generate with a specific profile:

```zsh
uv run python generate_opengd_import.py --profile chicago_light
```

Preview the SSRF files a profile would load:

```zsh
uv run python generate_opengd_import.py --profile chicago_light --dry-run
```

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

Install dependencies and run (default profile = `default`):

```zsh
uv sync
uv run python generate_opengd_import.py --profile default
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

## Limitations

- Only FM and DMR within 136–174 & 400–480 MHz are emitted.
- Other digital modes (D‑STAR, C4FM) aren’t exported to OpenGD77 CSVs.
- TG lists are derived per assignment; project‑wide curated lists can be added later.
- Additional SSRF‑Lite systems can be dropped into the appropriate folder under `ssrf/systems/` and will be included automatically by the default profile.

## Roadmap

- **Profile Inheritance & Per-System Overrides** *(planned)*
  Future profiles will allow:
  - Inheritance/defaults (e.g., `rx_only`, `all_skip`, `zone_cap`)
  - Per-system override files `<system_id>.overrides.yml` under `profiles/<name>/overrides/`
    using native SSRF schema, merging channel lists by `name`.
  - `--strict` for unknown keys or ambiguous matches.
  - `--explain` to show provenance of each final value.

## Safety / Compliance

- Monitor public safety and business frequencies only if permitted; transmit only where licensed/authorized.
- Verify tones, offsets, and activity; data may change.

## Contributing

1. Create a branch
2. Edit or add SSRF‑Lite YAML in `ssrf/` (plans or systems)
3. `uv run python generate_opengd_import.py` and review diffs
4. Update docs/tests as needed and open a PR

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](./LICENSE) file for details.

## Attribution

Thanks to local clubs/directories and NTIA SSRF as a reference model.
