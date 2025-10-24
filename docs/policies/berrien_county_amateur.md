# berrien_county_amateur

**File:** `berrien_county_amateur.yml`  
**Path:** `policies/berrien_county_amateur.yml`  

## Overview

- **Assignment Overrides:** 5
- **Zone Definitions:** 3
- **Custom Names:** 5
- **RX-Only Assignments:** 1
- **TX-Enabled Assignments:** 4
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions

## Zone Organization

| Zone | Assignments |
|------|-------------|
| Berrien Amateur | 5 |
| Digital Voice | 1 |
| Ham Repeaters | 4 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asg_skywarn_intercounty` | IMO Skywarn 145.430 |
| `asg_skywarn_link` | Skywarn UHF Link 442.775 |
| `asg_skywarn_primary` | Skywarn Primary 146.820 |
| `asg_skywarn_secondary` | Skywarn Secondary 146.720 |
| `asg_w8mai_dstar_b` | W8MAI D-STAR B |

## TX/RX Configuration

### RX-Only Assignments

- `asg_skywarn_intercounty`

### TX-Enabled Assignments

- `asg_skywarn_link`
- `asg_skywarn_primary`
- `asg_skywarn_secondary`
- `asg_w8mai_dstar_b`

## Assignment Details

### `asg_skywarn_intercounty`

**Codeplug:**
- `name`: IMO Skywarn 145.430
- `rx_only`: True

**Zones:**
- Include: Berrien Amateur, Ham Repeaters

### `asg_skywarn_link`

**Codeplug:**
- `name`: Skywarn UHF Link 442.775
- `rx_only`: False

**Zones:**
- Include: Berrien Amateur, Ham Repeaters

### `asg_skywarn_primary`

**Codeplug:**
- `name`: Skywarn Primary 146.820
- `rx_only`: False

**Zones:**
- Include: Berrien Amateur, Ham Repeaters

### `asg_skywarn_secondary`

**Codeplug:**
- `name`: Skywarn Secondary 146.720
- `rx_only`: False

**Zones:**
- Include: Berrien Amateur, Ham Repeaters

### `asg_w8mai_dstar_b`

**Codeplug:**
- `name`: W8MAI D-STAR B
- `rx_only`: False

**Zones:**
- Include: Berrien Amateur, Digital Voice

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/berrien_county_amateur.yml
```
