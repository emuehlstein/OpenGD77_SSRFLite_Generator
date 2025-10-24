# chicago_gmrs_repeaters

**File:** `chicago_gmrs_repeaters.yml`  
**Path:** `policies/chicago_gmrs_repeaters.yml`  

## Overview

- **Assignment Overrides:** 9
- **Zone Definitions:** 1
- **Custom Names:** 9
- **RX-Only Assignments:** 0
- **TX-Enabled Assignments:** 9
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions

## Zone Organization

| Zone | Assignments |
|------|-------------|
| GMRS | 9 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asgn_gmrs_chicago_575` | OHare 575 |
| `asgn_gmrs_chicago_600` | PL-600 |
| `asgn_gmrs_evanston_700` | NSEA Evan700 |
| `asgn_gmrs_evanston_725` | Evanston 725 |
| `asgn_gmrs_forest_view_650` | PRJ 650 |
| `asgn_gmrs_lincolnwood_575` | Lincolnwood 575 |
| `asgn_gmrs_northbrook_650` | NSEA NBrk650 |
| `asgn_gmrs_oak_lawn_625` | Oak Lawn |
| `asgn_gmrs_parkridge_675` | NSEA Her675 |

## TX/RX Configuration

### TX-Enabled Assignments

- `asgn_gmrs_chicago_575`
- `asgn_gmrs_chicago_600`
- `asgn_gmrs_evanston_700`
- `asgn_gmrs_evanston_725`
- `asgn_gmrs_forest_view_650`
- `asgn_gmrs_lincolnwood_575`
- `asgn_gmrs_northbrook_650`
- `asgn_gmrs_oak_lawn_625`
- `asgn_gmrs_parkridge_675`

## Assignment Details

### `asgn_gmrs_chicago_575`

**Codeplug:**
- `all_skip`: True
- `name`: OHare 575
- `rx_only`: False

**Zones:**
- Include: GMRS

### `asgn_gmrs_chicago_600`

**Codeplug:**
- `all_skip`: True
- `name`: PL-600
- `rx_only`: False

**Zones:**
- Include: GMRS

### `asgn_gmrs_evanston_700`

**Codeplug:**
- `all_skip`: True
- `name`: NSEA Evan700
- `rx_only`: False

**Zones:**
- Include: GMRS

### `asgn_gmrs_evanston_725`

**Codeplug:**
- `all_skip`: True
- `name`: Evanston 725
- `rx_only`: False

**Zones:**
- Include: GMRS

### `asgn_gmrs_forest_view_650`

**Codeplug:**
- `all_skip`: True
- `name`: PRJ 650
- `rx_only`: False

**Zones:**
- Include: GMRS

### `asgn_gmrs_lincolnwood_575`

**Codeplug:**
- `all_skip`: True
- `name`: Lincolnwood 575
- `rx_only`: False

**Zones:**
- Include: GMRS

### `asgn_gmrs_northbrook_650`

**Codeplug:**
- `all_skip`: True
- `name`: NSEA NBrk650
- `rx_only`: False

**Zones:**
- Include: GMRS

### `asgn_gmrs_oak_lawn_625`

**Codeplug:**
- `all_skip`: True
- `name`: Oak Lawn
- `rx_only`: False

**Zones:**
- Include: GMRS

### `asgn_gmrs_parkridge_675`

**Codeplug:**
- `all_skip`: True
- `name`: NSEA Her675
- `rx_only`: False

**Zones:**
- Include: GMRS

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/chicago_gmrs_repeaters.yml
```
