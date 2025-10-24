# st_pete_gmrs_repeaters

**File:** `st_pete_gmrs_repeaters.yml`  
**Path:** `policies/st_pete_gmrs_repeaters.yml`  

## Overview

- **Assignment Overrides:** 7
- **Zone Definitions:** 1
- **Custom Names:** 7
- **RX-Only Assignments:** 0
- **TX-Enabled Assignments:** 7
- **Scan-Enabled Assignments:** 7

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions
- **Scan:** Skip settings and scan behavior

## Zone Organization

| Zone | Assignments |
|------|-------------|
| GMRS | 7 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asg_gmrs_clearwater_675` | Clearwater 675 |
| `asg_gmrs_ruskin_700` | Ruskin 700 |
| `asg_gmrs_seminole_725` | Seminole 725 |
| `asg_gmrs_tampa_600` | Tampa Bay 600 |
| `asg_gmrs_tampa_shores_650` | Tampa Shores 650 |
| `asg_gmrs_tampa_shores_700` | Tampa Shores 700 |
| `asg_gmrs_west_bradenton_625` | Cortez 625 |

## TX/RX Configuration

### TX-Enabled Assignments

- `asg_gmrs_clearwater_675`
- `asg_gmrs_ruskin_700`
- `asg_gmrs_seminole_725`
- `asg_gmrs_tampa_600`
- `asg_gmrs_tampa_shores_650`
- `asg_gmrs_tampa_shores_700`
- `asg_gmrs_west_bradenton_625`

## Scan Configuration

### Scan-Enabled Assignments

- `asg_gmrs_clearwater_675`
- `asg_gmrs_ruskin_700`
- `asg_gmrs_seminole_725`
- `asg_gmrs_tampa_600`
- `asg_gmrs_tampa_shores_650`
- `asg_gmrs_tampa_shores_700`
- `asg_gmrs_west_bradenton_625`

## Assignment Details

### `asg_gmrs_clearwater_675`

**Codeplug:**
- `name`: Clearwater 675
- `rx_only`: False

**Zones:**
- Include: GMRS

**Scan:**
- `all_skip`: False

### `asg_gmrs_ruskin_700`

**Codeplug:**
- `name`: Ruskin 700
- `rx_only`: False

**Zones:**
- Include: GMRS

**Scan:**
- `all_skip`: False

### `asg_gmrs_seminole_725`

**Codeplug:**
- `name`: Seminole 725
- `rx_only`: False

**Zones:**
- Include: GMRS

**Scan:**
- `all_skip`: False

### `asg_gmrs_tampa_600`

**Codeplug:**
- `name`: Tampa Bay 600
- `rx_only`: False

**Zones:**
- Include: GMRS

**Scan:**
- `all_skip`: False

### `asg_gmrs_tampa_shores_650`

**Codeplug:**
- `name`: Tampa Shores 650
- `rx_only`: False

**Zones:**
- Include: GMRS

**Scan:**
- `all_skip`: False

### `asg_gmrs_tampa_shores_700`

**Codeplug:**
- `name`: Tampa Shores 700
- `rx_only`: False

**Zones:**
- Include: GMRS

**Scan:**
- `all_skip`: False

### `asg_gmrs_west_bradenton_625`

**Codeplug:**
- `name`: Cortez 625
- `rx_only`: False

**Zones:**
- Include: GMRS

**Scan:**
- `all_skip`: False

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/st_pete_gmrs_repeaters.yml
```
