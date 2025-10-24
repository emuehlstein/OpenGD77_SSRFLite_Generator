# OpenGD77 SSRFLite Generator

A reproducible, data‑driven codeplug builder for radios running OpenGD77. The generator ingests [SSRF-Lite YAML](#ssrf-lite) files and produces OpenGD77‑compatible CSVs (`Channels.csv`, `Contacts.csv`, `TG_Lists.csv`, `Zones.csv`) suitable for import via the CPS.  The generator is opinionated but superuser configurable.

## Overview

```text
┌────────────────┐   ┌────────────────────┐   ┌────────────────────┐
│ SSRF-Lite data │ → │ Profiles (selection│ → │ Policies (opinions │
│ Reference-only │   │ & scoping)         │   │ & rendering rules) │
└────────────────┘   └────────────────────┘   └────────────────────┘
```


The generator assembles a codeplug by reading Profile file, assembling the RF information from our SSRFLite library, and finally applying a Policy which describes the radio's presentation of each channel eg. channel name, scan settings, rx only, etc.

Features:
 - **Library of RF systems and channel plan data** – [Browse SSRF Documentation →](docs/ssrf/README.md)
 - **Example Profiles for various geographies** – [Browse Profile Documentation →](docs/profiles/README.md)

## Quick Start

1. **Install prerequisites** – Make sure Python 3.10+ and the `uv` package manager are available on your system.

1. **Clone the repository and enter it.**

    ```zsh
    git clone https://github.com/emuehlstein/OpenGD77_SSRFLite_Generator.git
    cd OpenGD77_SSRFLite_Generator
    ```

1. **Sync the virtual environment with `uv`.** This creates `.venv/` and installs the generator, Pydantic models, and test tooling.

    ```zsh
    uv sync
    ```

1. **Build the OpenGD77 CSV bundle.** The results land in `opengd77_cps_import_generated/`.

    ```zsh
    uv run python generate_opengd_import.py
    ```

1. **Import into the CPS.** In the OpenGD77 CPS choose **File → CSV → Import CSV**, point at the generated folder, and load the Channels/Contacts/TG Lists/Zones files.

Need another profile? Add flags such as `--profile chicago_amateur` or `--profile gmrs_only`. Add `--tx-service gmrs` (or `--tx-all-services`) when you want transmit enabled beyond the Amateur defaults.

To verify everything after edits, run the smoke tests:

```zsh
uv run python -m pytest tests/test_profiles.py
```

## SSRF‑Lite

This project includes a proposed format for sharing information about RF systems, "SSRF-Lite," which is a simplified and yamlized version of the SSRF format used by the US DoD.

- Project doc: [SSRF‑Lite Spec](./ssrf/_schema/SSRF-Lite-Spec.md)
- Background (NTIA SSRF): [https://www.ntia.gov/publications/2023/standard-spectrum-resource-format-ssrf](https://www.ntia.gov/publications/2023/standard-spectrum-resource-format-ssrf)


## Opinions

A few opinions held by this project:

- **Separation of concerns:** keep RF reference data independent of codeplug presentation so the same facts fuel multiple builds.
- **Layered configuration:** SSRF reference → profile selection → policy overlays, allowing each layer to evolve without breaking the others.
- **Reproducible outputs:** generators run from version-controlled data and deterministic tooling (`uv`) so CSVs can be regenerated and diffed reliably.
- **Safety-first defaults:** transmit remains disabled unless explicitly permitted, reducing the risk of illegal or unintended emissions.
- **Extensibility:** new services, profiles, or radios should drop in via additional SSRF files or policies without refactoring core code.
  
## Profiles & Policies

Profiles provide inclusion filters for SSRF reference data.  Each profile lives in `profiles/<name>.yml` and declares glob patterns plus optional service filters under `profile.include`.

Profiles can now point at one or more **policy** files using the optional `profile.policy` block:

```yaml
profile:
  name: "chicago_amateur"
  include:
    paths:
      - "ssrf/plans/US/amateur/*.yml"
      - "ssrf/systems/US/IL/Cook/Chicago/amateur/*.yml"
  policy:
    files:
      - policies/base.yml
    paths:
      - policies/chicago/**/*.yml
```

To keep overlays composable, larger systems and plans are broken into focused files (for example `policies/ham_fm_simplex.yml` or `policies/marine_vhf.yml`). Profiles opt into the pieces they need, making it straightforward to layer multiple profiles or overlays together in the future.

Policies are simple YAML documents that describe how selected assignments should be rendered. Typical keys include:

- `assignments.<assignment_id>.codeplug.name` – rename channels, mark `rx_only`, choose `preferred_contacts`, etc.
- `assignments.<assignment_id>.zones` – supply zone include/exclude lists.
- `assignments.<assignment_id>.scan` – configure `all_skip`, `zone_skip`, `tot`, `power`, `vox`, and related scan hints.
- `assignments.<assignment_id>.tx` – explicitly disable transmit for receive-only builds.

If a profile omits the `policy` block, the generator will fall back to `policies/<profile>.yml` when present, keeping the flow convenient for small builds.

Available starter profiles:

- `default` – broad build with national plans and Chicago-area systems.
- `chicago_light` – slim scan list focused on GMRS and public safety.
- `chicago_amateur` – Chicago amateur repeaters plus simplex plans.
- `chicago_gmrs` – Chicago GMRS repeaters and national GMRS plan.
- `gmrs_only` – National GMRS plan with policy-tuned GMRS zone layout.

`policies/gmrs_only.yml` keeps the national GMRS plan sorted into `GMRS Simplex`, `GMRS Listen`, and `GMRS Repeaters` zones while leaving the FRS-only interstitials receive-only by default.

Inspect the available profiles:

```zsh
uv run python generate_opengd_import.py --list-profiles
```

Generate with a specific profile:

```zsh
uv run python generate_opengd_import.py --profile chicago_light
uv run python generate_opengd_import.py --profile gmrs_only --tx-service gmrs  # GMRS-only build, TX enabled on GMRS channels
```

Enable transmit on additional services (default is Amateur only):

```zsh
uv run python generate_opengd_import.py --profile chicago_light --tx-service gmrs

# Allow transmit everywhere the radio supports
uv run python generate_opengd_import.py --profile chicago_light --tx-all-services
```

> **GMRS caveat:** The `gmrs_only` profile assumes you hold a valid GMRS license and are programming a radio that is type-accepted for GMRS operation. Do not enable transmit on equipment that lacks the appropriate FCC approval.

Preview the SSRF files a profile would load:

```zsh
uv run python generate_opengd_import.py --profile chicago_light --dry-run
```

## How It Works

The generator loads and merges SSRF‑Lite YAMLs, then:

- Builds `Contacts.csv` from `contacts[]` (only items with numeric IDs are emitted).
- Resolves policy overlays (if any) and merges them with legacy `assignments.codeplug` hints:
  - Policy keys drive channel naming, TX enablement, skip flags, TOT, power level, VOX, APRS, and zone membership.
  - `preferred_contacts` and `default_contact` can reference contact IDs, numbers, or names; the first valid entry sets the default DMR contact/slot.
- Builds `Channels.csv` from `assignments[]`:
  - If `rf_chain_id` is set and the chain is FM or DMR within supported bands, the generator emits Analogue or Digital rows using policy+legacy hints.
  - If `channel_plan_id` is set, the matching plan channel is emitted as Analogue (e.g., NOAA), subject to band filter.
- Builds `TG_Lists.csv` from policy/legacy `preferred_contacts` per assignment (max 32, list name derived from assignment or `codeplug.tg_list_name`).
- Builds `Zones.csv` from policy-derived zone lists (fallback to legacy `assignments[].zones`) with up to 80 channels per zone.

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

Copy the `opengd77_cps_import_generated` folder to a location your OpenGD77 CPS can read (for example, a Documents subfolder or removable media). In the CPS, open **File → CSV → Import CSV**, browse to that folder, and select the generated folder and load that into your codeplug project.

## Documentation

### Profile Documentation

📚 **[Browse All Profile Documentation →](docs/profiles/README.md)**

Generate comprehensive markdown documentation for profiles:

```zsh
# Generate documentation for all profiles
uv run python generate_profile_docs.py

# Generate documentation for a specific profile
uv run python generate_profile_docs.py --profile chicago_amateur

# List available profiles
uv run python generate_profile_docs.py --list-profiles
```

The generated documentation includes channel details, zone organization, contact lists, authorization requirements, and source file references. See the [profile documentation index](docs/profiles/README.md) for a complete overview and comparison of all available profiles.

### SSRF Data Documentation

📡 **[Browse All SSRF Documentation →](docs/ssrf/README.md)**

Generate comprehensive markdown documentation for SSRF files:

```zsh
# Generate documentation for all SSRF files
uv run python generate_ssrf_docs.py

# Generate documentation for a specific SSRF file
uv run python generate_ssrf_docs.py --file ssrf/plans/US/gmrs/gmrs_channels.yml

# List available SSRF files
uv run python generate_ssrf_docs.py --list-files
```

The generated documentation provides detailed views of RF systems, channel plans, assignments, and geographic coverage. Each SSRF file gets its own documentation page with frequency details, service information, and organizational data. See the [SSRF documentation index](docs/ssrf/README.md) for a complete overview and browsable file catalog.

## Data Notes & Conventions

- SSRF‑Lite entities used here: `organizations`, `locations`, `stations`, `antennas`, `rf_chains`, `contacts`, `channel_plans`, `assignments`. These remain reference-only facts.
- Policies (or legacy `assignments.codeplug`) provide rendering instructions: channel names, zone membership, skip flags, TOT, power, VOX, and preferred contacts. Transmit enablement defaults to Amateur-only unless additional services are whitelisted via `--tx-service` or `--tx-all-services`.
- For DMR, `mode.color_code` sets Colour Code; the default Timeslot is derived from policy/legacy preferred contacts (with fallback to global defaults).
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
