# berrien_county_public_safety

**File:** `berrien_county_public_safety.yml`  
**Path:** `policies/berrien_county_public_safety.yml`  

## Overview

- **Assignment Overrides:** 13
- **Zone Definitions:** 4
- **Custom Names:** 13
- **RX-Only Assignments:** 13
- **TX-Enabled Assignments:** 0
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions
- **Scan:** Skip settings and scan behavior

## Zone Organization

| Zone | Assignments |
|------|-------------|
| Berrien Fire | 9 |
| Berrien Parks | 1 |
| Berrien Sheriff | 1 |
| Public Service | 2 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asg_berrien_eoc` | EOC |
| `asg_berrien_fg1` | Fireground 1 |
| `asg_berrien_fg2` | Fireground 2 |
| `asg_berrien_fg3` | Fireground 3 |
| `asg_berrien_fg4` | Fireground 4 |
| `asg_berrien_fg5` | Fireground 5 |
| `asg_berrien_fire1` | Fire Dispatch 1 |
| `asg_berrien_fire2` | Fire Dispatch 2 |
| `asg_berrien_fire3` | Fire Dispatch 3 |
| `asg_berrien_jail` | County Jail |
| `asg_berrien_media_page` | Media Alert Page |
| `asg_berrien_silver_beach` | Silver Beach Ops |
| `asg_berrien_sirens` | EMA Sirens |

## TX/RX Configuration

### RX-Only Assignments

- `asg_berrien_eoc`
- `asg_berrien_fg1`
- `asg_berrien_fg2`
- `asg_berrien_fg3`
- `asg_berrien_fg4`
- `asg_berrien_fg5`
- `asg_berrien_fire1`
- `asg_berrien_fire2`
- `asg_berrien_fire3`
- `asg_berrien_jail`
- `asg_berrien_media_page`
- `asg_berrien_silver_beach`
- `asg_berrien_sirens`

## Scan Configuration

### Scan-Disabled Assignments

- `asg_berrien_eoc`
- `asg_berrien_fg1`
- `asg_berrien_fg2`
- `asg_berrien_fg3`
- `asg_berrien_fg4`
- `asg_berrien_fg5`
- `asg_berrien_fire1`
- `asg_berrien_fire2`
- `asg_berrien_fire3`
- `asg_berrien_jail`
- `asg_berrien_media_page`
- `asg_berrien_silver_beach`
- `asg_berrien_sirens`

## Assignment Details

### `asg_berrien_eoc`

**Codeplug:**
- `name`: EOC
- `rx_only`: True

**Zones:**
- Include: Public Service

**Scan:**
- `all_skip`: True

### `asg_berrien_fg1`

**Codeplug:**
- `name`: Fireground 1
- `rx_only`: True

**Zones:**
- Include: Berrien Fire

**Scan:**
- `all_skip`: True

### `asg_berrien_fg2`

**Codeplug:**
- `name`: Fireground 2
- `rx_only`: True

**Zones:**
- Include: Berrien Fire

**Scan:**
- `all_skip`: True

### `asg_berrien_fg3`

**Codeplug:**
- `name`: Fireground 3
- `rx_only`: True

**Zones:**
- Include: Berrien Fire

**Scan:**
- `all_skip`: True

### `asg_berrien_fg4`

**Codeplug:**
- `name`: Fireground 4
- `rx_only`: True

**Zones:**
- Include: Berrien Fire

**Scan:**
- `all_skip`: True

### `asg_berrien_fg5`

**Codeplug:**
- `name`: Fireground 5
- `rx_only`: True

**Zones:**
- Include: Berrien Fire

**Scan:**
- `all_skip`: True

### `asg_berrien_fire1`

**Codeplug:**
- `name`: Fire Dispatch 1
- `rx_only`: True

**Zones:**
- Include: Berrien Fire

**Scan:**
- `all_skip`: True

### `asg_berrien_fire2`

**Codeplug:**
- `name`: Fire Dispatch 2
- `rx_only`: True

**Zones:**
- Include: Berrien Fire

**Scan:**
- `all_skip`: True

### `asg_berrien_fire3`

**Codeplug:**
- `name`: Fire Dispatch 3
- `rx_only`: True

**Zones:**
- Include: Berrien Fire

**Scan:**
- `all_skip`: True

### `asg_berrien_jail`

**Codeplug:**
- `name`: County Jail
- `rx_only`: True

**Zones:**
- Include: Berrien Sheriff

**Scan:**
- `all_skip`: True

### `asg_berrien_media_page`

**Codeplug:**
- `name`: Media Alert Page
- `rx_only`: True

**Zones:**
- Include: Berrien Fire

**Scan:**
- `all_skip`: True

### `asg_berrien_silver_beach`

**Codeplug:**
- `name`: Silver Beach Ops
- `rx_only`: True

**Zones:**
- Include: Berrien Parks

**Scan:**
- `all_skip`: True

### `asg_berrien_sirens`

**Codeplug:**
- `name`: EMA Sirens
- `rx_only`: True

**Zones:**
- Include: Public Service

**Scan:**
- `all_skip`: True

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/berrien_county_public_safety.yml
```
