# noaa_weather

**File:** `noaa_weather.yml`  
**Path:** `policies/noaa_weather.yml`  

## Overview

- **Assignment Overrides:** 7
- **Zone Definitions:** 1
- **Custom Names:** 7
- **RX-Only Assignments:** 7
- **TX-Enabled Assignments:** 0
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions

## Zone Organization

| Zone | Assignments |
|------|-------------|
| NOAA Weather | 7 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asg_wx1` | WX1 |
| `asg_wx2` | WX2 |
| `asg_wx3` | WX3 |
| `asg_wx4` | WX4 |
| `asg_wx5` | WX5 |
| `asg_wx6` | WX6 |
| `asg_wx7` | WX7 |

## TX/RX Configuration

### RX-Only Assignments

- `asg_wx1`
- `asg_wx2`
- `asg_wx3`
- `asg_wx4`
- `asg_wx5`
- `asg_wx6`
- `asg_wx7`

## Assignment Details

### `asg_wx1`

**Codeplug:**
- `all_skip`: True
- `name`: WX1
- `rx_only`: True

**Zones:**
- Include: NOAA Weather

### `asg_wx2`

**Codeplug:**
- `all_skip`: True
- `name`: WX2
- `rx_only`: True

**Zones:**
- Include: NOAA Weather

### `asg_wx3`

**Codeplug:**
- `all_skip`: True
- `name`: WX3
- `rx_only`: True

**Zones:**
- Include: NOAA Weather

### `asg_wx4`

**Codeplug:**
- `all_skip`: True
- `name`: WX4
- `rx_only`: True

**Zones:**
- Include: NOAA Weather

### `asg_wx5`

**Codeplug:**
- `all_skip`: True
- `name`: WX5
- `rx_only`: True

**Zones:**
- Include: NOAA Weather

### `asg_wx6`

**Codeplug:**
- `all_skip`: True
- `name`: WX6
- `rx_only`: True

**Zones:**
- Include: NOAA Weather

### `asg_wx7`

**Codeplug:**
- `all_skip`: True
- `name`: WX7
- `rx_only`: True

**Zones:**
- Include: NOAA Weather

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/noaa_weather.yml
```
