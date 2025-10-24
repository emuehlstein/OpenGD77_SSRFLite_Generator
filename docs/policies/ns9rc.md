# ns9rc

**File:** `ns9rc.yml`  
**Path:** `policies/ns9rc.yml`  

## Overview

- **Assignment Overrides:** 13
- **Zone Definitions:** 8
- **Custom Names:** 13
- **RX-Only Assignments:** 2
- **TX-Enabled Assignments:** 11
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions

## Zone Organization

| Zone | Assignments |
|------|-------------|
| APRS | 1 |
| Beacons | 2 |
| DMR Repeater | 2 |
| Emergency / Calling | 2 |
| Ham Repeaters | 4 |
| Ham UHF | 1 |
| Ham VHF | 2 |
| Packet/Winlink | 1 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asgn_ns9rc_220` | NS9RC 220 |
| `asgn_ns9rc_2m_c4fm` | NS9RC 2m C4FM |
| `asgn_ns9rc_2m_fm` | NS9RC 2m FM |
| `asgn_ns9rc_440` | NS9RC 440 |
| `asgn_ns9rc_aprs` | NS9RC APRS |
| `asgn_ns9rc_beacon_10m` | NS9RC 10m BCN |
| `asgn_ns9rc_beacon_6m` | NS9RC 6m BCN |
| `asgn_ns9rc_dstar_23cm` | NS9RC DSTAR23 |
| `asgn_ns9rc_dstar_440` | NS9RC DSTAR4 |
| `asgn_ns9rc_simplex_146_460` | NS9RC VHF460 |
| `asgn_ns9rc_simplex_147_405` | NS9RC VHF405 |
| `asgn_ns9rc_simplex_446_025` | NS9RC UHF025 |
| `asgn_ns9rc_winlink` | NS9RC Winlink |

## TX/RX Configuration

### RX-Only Assignments

- `asgn_ns9rc_beacon_10m`
- `asgn_ns9rc_beacon_6m`

### TX-Enabled Assignments

- `asgn_ns9rc_220`
- `asgn_ns9rc_2m_c4fm`
- `asgn_ns9rc_2m_fm`
- `asgn_ns9rc_440`
- `asgn_ns9rc_aprs`
- `asgn_ns9rc_dstar_23cm`
- `asgn_ns9rc_dstar_440`
- `asgn_ns9rc_simplex_146_460`
- `asgn_ns9rc_simplex_147_405`
- `asgn_ns9rc_simplex_446_025`
- `asgn_ns9rc_winlink`

## Assignment Details

### `asgn_ns9rc_220`

**Codeplug:**
- `name`: NS9RC 220
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters

### `asgn_ns9rc_2m_c4fm`

**Codeplug:**
- `name`: NS9RC 2m C4FM
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters

### `asgn_ns9rc_2m_fm`

**Codeplug:**
- `name`: NS9RC 2m FM
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters, Emergency / Calling

### `asgn_ns9rc_440`

**Codeplug:**
- `name`: NS9RC 440
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters, Emergency / Calling

### `asgn_ns9rc_aprs`

**Codeplug:**
- `name`: NS9RC APRS
- `rx_only`: False

**Zones:**
- Include: APRS

### `asgn_ns9rc_beacon_10m`

**Codeplug:**
- `name`: NS9RC 10m BCN
- `rx_only`: True

**Zones:**
- Include: Beacons

### `asgn_ns9rc_beacon_6m`

**Codeplug:**
- `name`: NS9RC 6m BCN
- `rx_only`: True

**Zones:**
- Include: Beacons

### `asgn_ns9rc_dstar_23cm`

**Codeplug:**
- `name`: NS9RC DSTAR23
- `rx_only`: False

**Zones:**
- Include: DMR Repeater

### `asgn_ns9rc_dstar_440`

**Codeplug:**
- `name`: NS9RC DSTAR4
- `rx_only`: False

**Zones:**
- Include: DMR Repeater

### `asgn_ns9rc_simplex_146_460`

**Codeplug:**
- `name`: NS9RC VHF460
- `rx_only`: False

**Zones:**
- Include: Ham VHF

### `asgn_ns9rc_simplex_147_405`

**Codeplug:**
- `name`: NS9RC VHF405
- `rx_only`: False

**Zones:**
- Include: Ham VHF

### `asgn_ns9rc_simplex_446_025`

**Codeplug:**
- `name`: NS9RC UHF025
- `rx_only`: False

**Zones:**
- Include: Ham UHF

### `asgn_ns9rc_winlink`

**Codeplug:**
- `name`: NS9RC Winlink
- `rx_only`: False

**Zones:**
- Include: Packet/Winlink

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/ns9rc.yml
```
