# Policy Documentation

This directory contains automatically generated documentation for all policy files in the project.

## Quick Statistics

- **Total Policies:** 32
- **Total Assignment Overrides:** 563
- **Unique Zones:** 39
- **Custom Names:** 533

## Policy Overview

| Policy | Assignment Overrides | Zones | Custom Names | Configuration Types |
|--------|---------------------|-------|--------------|-------------------|
| [berrien_county_amateur](berrien_county_amateur.md) | 5 | 3 | 5 | Codeplug, Zones |
| [berrien_county_public_safety](berrien_county_public_safety.md) | 13 | 4 | 13 | Codeplug, Zones, Scan |
| [business_itinerant](business_itinerant.md) | 27 | 1 | 27 | Codeplug, Zones |
| [cfmc_repeaters](cfmc_repeaters.md) | 7 | 3 | 7 | Codeplug, Zones |
| [chicago_businesses_northside](chicago_businesses_northside.md) | 50 | 1 | 50 | Codeplug, Zones, Scan |
| [chicago_gmrs_repeaters](chicago_gmrs_repeaters.md) | 9 | 1 | 9 | Codeplug, Zones |
| [chicago_public_services](chicago_public_services.md) | 98 | 2 | 98 | Codeplug, Zones, Scan |
| [chicago_transit](chicago_transit.md) | 7 | 1 | 7 | Codeplug, Zones, Scan |
| [chicagoland_dmr](chicagoland_dmr.md) | 2 | 1 | 2 | Codeplug, Zones, Scan |
| [cook_public_safety](cook_public_safety.md) | 9 | 1 | 9 | Codeplug, Zones, Scan |
| [default](default.md) | 0 | 0 | 0 | *None* |
| [family_channels](family_channels.md) | 17 | 4 | 17 | Codeplug, Zones |
| [florida_simulcast_group](florida_simulcast_group.md) | 15 | 1 | 15 | Codeplug, Zones, Scan |
| [gmrs_channels](gmrs_channels.md) | 30 | 2 | 30 | Codeplug, Zones |
| [gmrs_only](gmrs_only.md) | 30 | 4 | 0 | Codeplug, Zones, Scan |
| [ham_dmr_simplex](ham_dmr_simplex.md) | 14 | 1 | 14 | Codeplug, Zones |
| [ham_fm_simplex](ham_fm_simplex.md) | 40 | 3 | 40 | Codeplug, Zones, Scan |
| [laporte_in_services](laporte_in_services.md) | 25 | 10 | 25 | Codeplug, Zones, Scan |
| [marine_vhf](marine_vhf.md) | 52 | 2 | 52 | Codeplug, Zones |
| [mmdvm_duplex_hotspot](mmdvm_duplex_hotspot.md) | 2 | 1 | 2 | Codeplug, Zones, Scan |
| [murs](murs.md) | 5 | 1 | 5 | Codeplug, Zones |
| [niles_kc8brs](niles_kc8brs.md) | 1 | 1 | 1 | Codeplug, Zones |
| [noaa_weather](noaa_weather.md) | 7 | 1 | 7 | Codeplug, Zones |
| [ns9rc](ns9rc.md) | 13 | 8 | 13 | Codeplug, Zones |
| [pmr446](pmr446.md) | 16 | 1 | 16 | Codeplug, Zones |
| [rail_aar_scan](rail_aar_scan.md) | 24 | 1 | 24 | Codeplug, Zones |
| [sara_repeaters](sara_repeaters.md) | 3 | 3 | 3 | Codeplug, Zones |
| [st_pete_gmrs_repeaters](st_pete_gmrs_repeaters.md) | 7 | 1 | 7 | Codeplug, Zones, Scan |
| [tampa_amateur_radio_club](tampa_amateur_radio_club.md) | 3 | 1 | 3 | Codeplug, Zones |
| [tri_state_dmr](tri_state_dmr.md) | 16 | 1 | 16 | Codeplug, Zones |
| [venues_chicago](venues_chicago.md) | 15 | 1 | 15 | Codeplug, Zones, Scan |
| [wcars](wcars.md) | 1 | 1 | 1 | Codeplug, Zones |

## Zone Usage Analysis

| Zone | Usage Count | Policies |
|------|-------------|----------|
| Business | 92 | business_itinerant, chicago_businesses_northside, venues_chicago |
| Public Safety | 90 | chicago_public_services, cook_public_safety |
| Ham Repeaters | 60 | berrien_county_amateur, cfmc_repeaters, chicagoland_dmr (+8 more) |
| Marine | 52 | marine_vhf |
| GMRS | 46 | chicago_gmrs_repeaters, gmrs_channels, st_pete_gmrs_repeaters |
| Rail | 24 | rail_aar_scan |
| Ham UHF | 22 | family_channels, ham_fm_simplex, ns9rc |
| Ham VHF | 22 | ham_fm_simplex, ns9rc |
| Public Works & Parks | 17 | chicago_public_services |
| PMR446 | 16 | pmr446 |
| GMRS Simplex | 15 | gmrs_only |
| Ham DMR Simplex | 14 | ham_dmr_simplex |
| Family Ops | 13 | family_channels |
| Emergency / Calling | 12 | cfmc_repeaters, gmrs_channels, gmrs_only (+5 more) |
| Berrien Fire | 9 | berrien_county_public_safety |
| GMRS Repeaters | 8 | gmrs_only |
| LaPorte Fire | 8 | laporte_in_services |
| Transit & Transport | 7 | chicago_transit |
| GMRS Listen | 7 | gmrs_only |
| NOAA Weather | 7 | noaa_weather |
| DMR Repeater | 6 | cfmc_repeaters, laporte_in_services, ns9rc (+1 more) |
| Berrien Amateur | 5 | berrien_county_amateur |
| MURS | 5 | murs |
| Family Ops Digital | 4 | family_channels |
| LaPorte Sheriff | 4 | laporte_in_services |
| Ham-DMR | 3 | laporte_in_services |
| Public Service | 2 | berrien_county_public_safety |
| Ham-Hotspot | 2 | mmdvm_duplex_hotspot |
| Beacons | 2 | ns9rc |
| Digital Voice | 1 | berrien_county_amateur |
| Berrien Sheriff | 1 | berrien_county_public_safety |
| Berrien Parks | 1 | berrien_county_public_safety |
| Fusion Digital | 1 | laporte_in_services |
| LaPorte EMA | 1 | laporte_in_services |
| Westville PD | 1 | laporte_in_services |
| LaPorte EMS | 1 | laporte_in_services |
| APRS | 1 | ns9rc |
| Packet/Winlink | 1 | ns9rc |
| Amateur Nets | 1 | wcars |

## Configuration Patterns

### Codeplug Configuration (31 policies)
Policies that modify channel names, RX/TX settings:

- [berrien_county_amateur](berrien_county_amateur.md) (5 assignments)
- [berrien_county_public_safety](berrien_county_public_safety.md) (13 assignments)
- [business_itinerant](business_itinerant.md) (27 assignments)
- [cfmc_repeaters](cfmc_repeaters.md) (7 assignments)
- [chicago_businesses_northside](chicago_businesses_northside.md) (50 assignments)
- [chicago_gmrs_repeaters](chicago_gmrs_repeaters.md) (9 assignments)
- [chicago_public_services](chicago_public_services.md) (98 assignments)
- [chicago_transit](chicago_transit.md) (7 assignments)
- [chicagoland_dmr](chicagoland_dmr.md) (2 assignments)
- [cook_public_safety](cook_public_safety.md) (9 assignments)
- *...and 21 more*

### Zone Configuration (31 policies)
Policies that organize assignments into zones:

- [berrien_county_amateur](berrien_county_amateur.md) (3 zones)
- [berrien_county_public_safety](berrien_county_public_safety.md) (4 zones)
- [business_itinerant](business_itinerant.md) (1 zones)
- [cfmc_repeaters](cfmc_repeaters.md) (3 zones)
- [chicago_businesses_northside](chicago_businesses_northside.md) (1 zones)
- [chicago_gmrs_repeaters](chicago_gmrs_repeaters.md) (1 zones)
- [chicago_public_services](chicago_public_services.md) (2 zones)
- [chicago_transit](chicago_transit.md) (1 zones)
- [chicagoland_dmr](chicagoland_dmr.md) (1 zones)
- [cook_public_safety](cook_public_safety.md) (1 zones)
- *...and 21 more*

### Scan Configuration (13 policies)
Policies that modify scan behavior:

- [berrien_county_public_safety](berrien_county_public_safety.md) (13 assignments)
- [chicago_businesses_northside](chicago_businesses_northside.md) (50 assignments)
- [chicago_public_services](chicago_public_services.md) (98 assignments)
- [chicago_transit](chicago_transit.md) (7 assignments)
- [chicagoland_dmr](chicagoland_dmr.md) (2 assignments)
- [cook_public_safety](cook_public_safety.md) (9 assignments)
- [florida_simulcast_group](florida_simulcast_group.md) (5 assignments)
- [gmrs_only](gmrs_only.md) (30 assignments)
- [ham_fm_simplex](ham_fm_simplex.md) (1 assignments)
- [laporte_in_services](laporte_in_services.md) (15 assignments)
- *...and 3 more*

## Using Policies

Policies provide assignment-level overrides for codeplug generation. They can be used in profiles:

### Single Policy File
```yaml
profile:
  policy:
    files:
      - policies/gmrs_only.yml
```

### Multiple Policy Files
```yaml
profile:
  policy:
    files:
      - policies/default.yml
      - policies/chicago_gmrs_repeaters.yml
    paths:
      - policies/chicago/**/*.yml
```

### Legacy Policy Support
```yaml
# If profile omits policy block, generator looks for:
# policies/<profile_name>.yml
```

## Policy Configuration Reference

### Assignment Overrides
```yaml
policy:
  assignments:
    assignment_id:
      codeplug:
        name: "Custom Name"
        rx_only: true/false
        preferred_contacts: [contact_id, ...]
      zones:
        include: ["Zone 1", "Zone 2"]
        exclude: ["Zone 3"]
      scan:
        all_skip: true/false
        zone_skip: true/false
        tot: 30
        power: "High"
        vox: true/false
      tx:
        enabled: true/false
```
