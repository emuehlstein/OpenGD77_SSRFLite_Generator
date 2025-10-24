# tampa_amateur_radio_club

**File:** `tampa_amateur_radio_club.yml`  
**Path:** `policies/tampa_amateur_radio_club.yml`  

## Overview

- **Assignment Overrides:** 3
- **Zone Definitions:** 1
- **Custom Names:** 3
- **RX-Only Assignments:** 0
- **TX-Enabled Assignments:** 0
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions

## Zone Organization

| Zone | Assignments |
|------|-------------|
| Ham Repeaters | 3 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asgn_tarc_uhf1` | TARC 444.750 |
| `asgn_tarc_uhf2` | TARC 443.025 |
| `asgn_tarc_vhf` | TARC 147.105 |

## Assignment Details

### `asgn_tarc_uhf1`

**Codeplug:**
- `name`: TARC 444.750
- `power`: High

**Zones:**
- Include: Ham Repeaters

### `asgn_tarc_uhf2`

**Codeplug:**
- `name`: TARC 443.025
- `power`: High

**Zones:**
- Include: Ham Repeaters

### `asgn_tarc_vhf`

**Codeplug:**
- `name`: TARC 147.105
- `power`: High

**Zones:**
- Include: Ham Repeaters

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/tampa_amateur_radio_club.yml
```
