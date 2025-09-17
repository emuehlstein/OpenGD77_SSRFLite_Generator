# Chicago OpenGD77 Generator

A data-driven channel and zone generator for an OpenGD77 / DMR handheld codeplug focused on Chicago & Cook County (public safety monitoring, local amateur repeaters, GMRS, MURS, NOAA Weather, Marine VHF, business / hospitality, and simplex). YAML source files describe frequencies, tones, and repeater metadata; a Python script converts these into OpenGD77-compatible CSV files you can import via the CPS.

> NOTE: Receive-only monitoring of public safety is emphasized. Transmitting on any frequency for which you are not licensed or authorized is illegal. Always verify current regulations and repeater owner policies.

> ⚠️ Project Status / Incomplete Generator: The `generate_channels.py` script does NOT yet recreate every channel found in `opengd77_cps_import_generated/Channels.csv`. Several channel groups (e.g., GMRS, some business/hospitality entries, and manually curated additions) plus many CTCSS/DCS tones and DMR attributes (Colour Codes, Time Slots, Talkgroup/contact specifics) are still missing or defaulted. Treat the current CSV set as a work-in-progress snapshot rather than a fully reproducible build artifact. Regenerating now will yield a reduced / partially populated channel list until parsing logic and data normalization are expanded.

## Repository Structure

```text
.
├── generate_channels.py            # Main generator script (reads YAML -> Channels.csv)
├── cook_county_conventional.yml    # Conventional (public safety / interoperability) channels
├── northside_dmr_repeater_info.yml # DMR amateur repeaters (digital)
├── chicago_businesses_rf.yml       # Business / retail / hospitality analog + some DMR
├── murs_channels.yml               # US MURS channel plan
├── noaa_weather.yml                # NOAA weather frequencies (Rx only in Zones)
├── marine_channels.yml             # US marine VHF plan subset used locally
├── ham_simplex.yml                 # Amateur VHF/UHF simplex + APRS
├── chicagoland_analog_repeaters.yml# Analog amateur repeaters
├── gmrs_repeaters_chicago.yml      # (Manual) GMRS repeaters + channel plan (currently NOT auto-ingested)
├── opengd77_cps_export/            # (Optional) Reference export (original dataset)
└── opengd77_cps_import_generated/  # Generated import CSVs (Channels/Contacts/Zones/etc.)
```

Key generated files of interest:

- `opengd77_cps_import_generated/Channels.csv` – All synthesized channels
- `opengd77_cps_import_generated/Zones.csv` – Zone organization (currently maintained manually + post-generation additions like GMRS)

## Data Flow

1. Edit YAML source definitions (see below for conventions).
1. Run the generator:

  ```bash
  python3 generate_channels.py
  ```

1. Script writes a fresh `Channels.csv` under `opengd77_cps_import_generated/`.
1. Zones (`Zones.csv`) are presently curated manually (script does not build zones yet).
1. Import the generated CSVs with the OpenGD77 CPS (or compatible tools) to update your radio codeplug.

## YAML Conventions

Each YAML file has a root key providing a namespace (e.g., `cook_county_conventional`, `dmr_repeaters_chicago`, `chicago_businesses_rf`). Within those:

- `channels` or `repeaters` arrays contain structured entries.
- Field names typically used by the script:
  - `alpha_tag` / `channel_name`
  - `freq_mhz`, `freq_out_mhz`, `freq_in_mhz`, `input_mhz` / `input_freq_mhz`
  - `tone` (supports CTCSS (`107.2 PL`) or DCS (`023 DPL`))
  - `mode` (e.g., `FMN`, `FM`, `DMR`)
  - DMR-specific: `color_code`, network cues (for talkgroup mapping heuristics)

If adding new categories:

- Follow an existing file’s structure.
- Maintain MHz float values (not strings) for frequency fields.
- Use consistent key names; the script performs simple key lookups and light normalization.

## Channel Field Mapping

The generator normalizes to the OpenGD77 CSV header defined in `generate_channels.py` (`HEADER` list). Highlights:

- Analogue: `Bandwidth (kHz)` set to `12.5` (narrow) or `25` (wide) based on mode/plan.
- Digital (DMR): Leaves bandwidth blank; sets Colour Code = 1 (unless extended later), Timeslot = 1.
- Tones: CTCSS/DCS duplicated to RX/TX if repeater (unless input-only tone logic needed later).
- Rx Only: NOAA weather channels flagged `Yes` (others default `No`). GMRS interstitial low-power channels (8–14) may optionally be flagged Rx Only if desired—currently some are flagged in manual additions.

## Zones

`Zones.csv` groups channels logically:

- GMRS, MURS, Marine, NOAA Weather, Ham Simplex, Ham Repeaters
- CityOfChicago (municipal services & public works)
- LEO / Fire / Interagency (monitoring groupings)
- Hotels / Retail / Restaurants / OtherUnknown (monitoring business & venue ops)

GMRS channels (simplex + repeater pairs + local repeaters) were appended manually to `Channels.csv` after script generation – the generator does not yet ingest `gmrs_repeaters_chicago.yml`.

### Planned Automation Ideas

- Auto-build `Zones.csv` from tags in YAML (introduce a `zone` or `groups` field per entry).
- Ingest GMRS YAML automatically and unify naming (e.g., `GMRS 01` vs canonical numbering).
- Validate duplicates (same frequency/tone) and optionally collapse or annotate.
- Add talkgroup/contact generation for DMR (Contacts.csv, TG_Lists.csv) from structured metadata.
- Frequency sorting & deterministic channel numbering by category.

## Running the Generator

Requirements: Python 3.8+

```bash
python3 generate_channels.py
# Outputs: Wrote <N> channels to opengd77_cps_import_generated/Channels.csv
```

If you want a clean rebuild:

```bash
git checkout -- opengd77_cps_import_generated/Channels.csv
python3 generate_channels.py
```

Then re-apply any manual edits (e.g., GMRS) or enhance the script to include them automatically.

## Adding GMRS Support Programmatically

Currently GMRS was added manually. To automate:

1. Append `gmrs_repeaters_chicago.yml` to `YAML_FILES` list in the script.
2. Add a parsing block similar to others (simplex + repeater pairs + local repeaters).
3. Consider a `gmrs_channel_plan` root key for future expandability.

## Safety / Compliance Disclaimer

- Public safety & business frequencies: Monitor only unless explicitly authorized.
- Amateur (ham) & GMRS: Transmit only with appropriate FCC license and within permitted power/band limits.
- Verify tones, offsets, and activity — data may become outdated.

## Contributing / Workflow

1. Fork / branch
2. Edit or add YAML source
3. Run generator & spot-check channel count diffs
4. Update README / zones if structure changes
5. Submit PR with concise description

## Potential Enhancements

- Unit tests to assert row counts & header integrity
- Lint YAML (schema validation) before generation
- GitHub Action to regenerate on push and fail if diff not committed
- Optional geospatial metadata (lat/lon per repeater) carried into comments or an auxiliary file

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Missing channel in output | YAML key mismatch | Match existing field names (`alpha_tag`, `freq_mhz`) |
| Wrong bandwidth | Mode heuristic too simple | Extend logic in `add_analogue` calls |
| Duplicate names | Multiple YAML entries share alpha tag | Rename or add suffix in YAML |

## License

(Choose and add a license file, e.g., MIT, if you intend public sharing.)

## Attribution

Frequency data compiled from personal monitoring, public directories, and common U.S. band plans. This is an informal, best-effort dataset.

---

Questions or ideas for improvement? Open an issue or start a discussion.
# Chicago_OpenGD77_Generator
