# Profile Documentation

This directory contains automatically generated markdown documentation for each profile in the OpenGD77 SSRF-Lite Generator project.

## Quick Statistics

- **Total Profiles:** 8
- **Total Assignments:** 1,034
- **Services Covered:** 10
- **Modes Supported:** DMR, FM

## Profile Comparison

| Profile | Description | Channels | Services | Zones | Contacts |
|---------|-------------|----------|----------|-------|----------|
| [chicago_amateur](chicago_amateur.md) | Chicago-focused amateur repeaters, DMR talkgroups, and simpl... | 68 | amateur, unknown | 6 | 28 |
| [chicago_amateur_w_gmrs](chicago_amateur_w_gmrs.md) | Chicago-focused amateur repeaters, DMR talkgroups, and simpl... | 124 | amateur, gmrs, unknown | 9 | 30 |
| [chicago_gmrs](chicago_gmrs.md) | Chicago GMRS repeaters, family operations, and national simp... | 56 | amateur, gmrs | 6 | 2 |
| [chicago_light](chicago_light.md) | Slim scanning profile for Chicago (GMRS + public safety). | 56 | amateur, gmrs | 6 | 2 |
| [default](default.md) | Baseline build using common plans and local Chicago systems. | 450 | amateur, business_itinerant_part90, gmrs (+7 more) | 18 | 39 |
| [gmrs_only](gmrs_only.md) | GMRS-only build with national simplex plans for quick progra... | 30 | gmrs | 2 | 0 |
| [rolling_prairie_in](rolling_prairie_in.md) | Rolling Prairie IN area: La Porte & Berrien county public sa... | 78 | amateur, gmrs, murs (+2 more) | 14 | 0 |
| [st_pete_fl](st_pete_fl.md) | Florida Simulcast Group repeaters around St. Petersburg / Ta... | 172 | amateur, gmrs, marine (+1 more) | 10 | 31 |

## Available Profiles

### [chicago_amateur](chicago_amateur.md)

**Description:** Chicago-focused amateur repeaters, DMR talkgroups, and simplex plans.

**Key Statistics:**
- **Channels:** 68
- **Services:** amateur, unknown
- **Modes:** FM (50), DMR (18)
- **Zones:** 6
- **Contacts:** 28 (DMR talkgroups)

### [chicago_amateur_w_gmrs](chicago_amateur_w_gmrs.md)

**Description:** Chicago-focused amateur repeaters, DMR talkgroups, and simplex plans, plus GMRS

**Key Statistics:**
- **Channels:** 124
- **Services:** amateur, gmrs, unknown
- **Modes:** FM (102), DMR (22)
- **Zones:** 9
- **Contacts:** 30 (DMR talkgroups)

### [chicago_gmrs](chicago_gmrs.md)

**Description:** Chicago GMRS repeaters, family operations, and national simplex plans.

**Key Statistics:**
- **Channels:** 56
- **Services:** amateur, gmrs
- **Modes:** FM (52), DMR (4)
- **Zones:** 6
- **Contacts:** 2 (DMR talkgroups)

### [chicago_light](chicago_light.md)

**Description:** Slim scanning profile for Chicago (GMRS + public safety).

**Key Statistics:**
- **Channels:** 56
- **Services:** amateur, gmrs
- **Modes:** FM (52), DMR (4)
- **Zones:** 6
- **Contacts:** 2 (DMR talkgroups)

### [default](default.md)

**Description:** Baseline build using common plans and local Chicago systems.

**Key Statistics:**
- **Channels:** 450
- **Services:** amateur, business_itinerant_part90, gmrs, marine, murs, noaa_weather_radio, pmr446, public_safety_part90, railroad_aar, unknown
- **Modes:** FM (365), DMR (85)
- **Zones:** 18
- **Contacts:** 39 (DMR talkgroups)

### [gmrs_only](gmrs_only.md)

**Description:** GMRS-only build with national simplex plans for quick programming.

**Key Statistics:**
- **Channels:** 30
- **Services:** gmrs
- **Modes:** FM (30)
- **Zones:** 2

### [rolling_prairie_in](rolling_prairie_in.md)

**Description:** Rolling Prairie IN area: La Porte & Berrien county public safety, local amateur, GMRS/MURS/weather plans.

**Key Statistics:**
- **Channels:** 78
- **Services:** amateur, gmrs, murs, noaa_weather_radio, public_safety_part90
- **Modes:** FM (78)
- **Zones:** 14

### [st_pete_fl](st_pete_fl.md)

**Description:** Florida Simulcast Group repeaters around St. Petersburg / Tampa plus national simplex and GMRS

**Key Statistics:**
- **Channels:** 172
- **Services:** amateur, gmrs, marine, unknown
- **Modes:** FM (150), DMR (22)
- **Zones:** 10
- **Contacts:** 31 (DMR talkgroups)

## How to Use

### Generate Codeplug CSV Files
```bash
# Generate with default profile
uv run python generate_opengd_import.py

# Generate with specific profile
uv run python generate_opengd_import.py --profile chicago_amateur

# Enable TX on additional services (default is amateur only)
uv run python generate_opengd_import.py --profile chicago_gmrs --tx-service gmrs
```

### Regenerate This Documentation
```bash
# Generate documentation for all profiles
uv run python generate_profile_docs.py

# Generate documentation for a specific profile
uv run python generate_profile_docs.py --profile chicago_amateur
```

## Important Notes

- **OpenGD77 Compatibility:** Only FM and DMR modes within 136-174 MHz and 400-480 MHz bands are included
- **Licensing:** Ensure you have appropriate licenses (Amateur, GMRS, etc.) before transmitting
- **Verification:** Always verify frequencies, tones, and permissions before use
- **Updates:** Documentation reflects the current state of SSRF files and policies

## Profile Selection Guide

Choose a profile based on your needs:

- **New to radio programming?** Start with `gmrs_only` or `chicago_light`
- **Amateur radio operator in Chicago?** Use `chicago_amateur` or `chicago_amateur_w_gmrs`
- **GMRS license holder?** Try `chicago_gmrs` or `gmrs_only`
- **Want comprehensive coverage?** Use `default` (largest selection)
- **Specific geographic area?** Check `rolling_prairie_in` or `st_pete_fl` for examples
