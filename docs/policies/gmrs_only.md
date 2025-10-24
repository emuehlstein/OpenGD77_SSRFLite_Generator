# gmrs_only

**File:** `gmrs_only.yml`  
**Path:** `policies/gmrs_only.yml`  

## Overview

- **Assignment Overrides:** 30
- **Zone Definitions:** 4
- **Custom Names:** 0
- **RX-Only Assignments:** 7
- **TX-Enabled Assignments:** 0
- **Scan-Enabled Assignments:** 30

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions
- **Scan:** Skip settings and scan behavior

## Zone Organization

| Zone | Assignments |
|------|-------------|
| Emergency / Calling | 1 |
| GMRS Listen | 7 |
| GMRS Repeaters | 8 |
| GMRS Simplex | 15 |

## TX/RX Configuration

### RX-Only Assignments

- `asgn_gmrs_08`
- `asgn_gmrs_09`
- `asgn_gmrs_10`
- `asgn_gmrs_11`
- `asgn_gmrs_12`
- `asgn_gmrs_13`
- `asgn_gmrs_14`

## Scan Configuration

### Scan-Enabled Assignments

- `asgn_gmrs_01`
- `asgn_gmrs_02`
- `asgn_gmrs_03`
- `asgn_gmrs_04`
- `asgn_gmrs_05`
- `asgn_gmrs_06`
- `asgn_gmrs_07`
- `asgn_gmrs_08`
- `asgn_gmrs_09`
- `asgn_gmrs_10`
- `asgn_gmrs_11`
- `asgn_gmrs_12`
- `asgn_gmrs_13`
- `asgn_gmrs_14`
- `asgn_gmrs_15`
- `asgn_gmrs_16`
- `asgn_gmrs_17`
- `asgn_gmrs_18`
- `asgn_gmrs_19`
- `asgn_gmrs_20`
- `asgn_gmrs_21`
- `asgn_gmrs_22`
- `asgn_gmrs_rpt_15`
- `asgn_gmrs_rpt_16`
- `asgn_gmrs_rpt_17`
- `asgn_gmrs_rpt_18`
- `asgn_gmrs_rpt_19`
- `asgn_gmrs_rpt_20`
- `asgn_gmrs_rpt_21`
- `asgn_gmrs_rpt_22`

## Assignment Details

### `asgn_gmrs_01`

**Zones:**
- Include: GMRS Simplex

**Scan:**
- `all_skip`: False

### `asgn_gmrs_02`

**Zones:**
- Include: GMRS Simplex

**Scan:**
- `all_skip`: False

### `asgn_gmrs_03`

**Zones:**
- Include: GMRS Simplex

**Scan:**
- `all_skip`: False

### `asgn_gmrs_04`

**Zones:**
- Include: GMRS Simplex

**Scan:**
- `all_skip`: False

### `asgn_gmrs_05`

**Zones:**
- Include: GMRS Simplex

**Scan:**
- `all_skip`: False

### `asgn_gmrs_06`

**Zones:**
- Include: GMRS Simplex

**Scan:**
- `all_skip`: False

### `asgn_gmrs_07`

**Zones:**
- Include: GMRS Simplex

**Scan:**
- `all_skip`: False

### `asgn_gmrs_08`

**Codeplug:**
- `rx_only`: True

**Zones:**
- Include: GMRS Listen

**Scan:**
- `all_skip`: False

### `asgn_gmrs_09`

**Codeplug:**
- `rx_only`: True

**Zones:**
- Include: GMRS Listen

**Scan:**
- `all_skip`: False

### `asgn_gmrs_10`

**Codeplug:**
- `rx_only`: True

**Zones:**
- Include: GMRS Listen

**Scan:**
- `all_skip`: False

### `asgn_gmrs_11`

**Codeplug:**
- `rx_only`: True

**Zones:**
- Include: GMRS Listen

**Scan:**
- `all_skip`: False

### `asgn_gmrs_12`

**Codeplug:**
- `rx_only`: True

**Zones:**
- Include: GMRS Listen

**Scan:**
- `all_skip`: False

### `asgn_gmrs_13`

**Codeplug:**
- `rx_only`: True

**Zones:**
- Include: GMRS Listen

**Scan:**
- `all_skip`: False

### `asgn_gmrs_14`

**Codeplug:**
- `rx_only`: True

**Zones:**
- Include: GMRS Listen

**Scan:**
- `all_skip`: False

### `asgn_gmrs_15`

**Zones:**
- Include: GMRS Simplex

**Scan:**
- `all_skip`: False

### `asgn_gmrs_16`

**Zones:**
- Include: GMRS Simplex

**Scan:**
- `all_skip`: False

### `asgn_gmrs_17`

**Zones:**
- Include: GMRS Simplex

**Scan:**
- `all_skip`: False

### `asgn_gmrs_18`

**Zones:**
- Include: GMRS Simplex

**Scan:**
- `all_skip`: False

### `asgn_gmrs_19`

**Zones:**
- Include: GMRS Simplex

**Scan:**
- `all_skip`: False

### `asgn_gmrs_20`

**Zones:**
- Include: GMRS Simplex, Emergency / Calling

**Scan:**
- `all_skip`: False

### `asgn_gmrs_21`

**Zones:**
- Include: GMRS Simplex

**Scan:**
- `all_skip`: False

### `asgn_gmrs_22`

**Zones:**
- Include: GMRS Simplex

**Scan:**
- `all_skip`: False

### `asgn_gmrs_rpt_15`

**Zones:**
- Include: GMRS Repeaters

**Scan:**
- `all_skip`: False

### `asgn_gmrs_rpt_16`

**Zones:**
- Include: GMRS Repeaters

**Scan:**
- `all_skip`: False

### `asgn_gmrs_rpt_17`

**Zones:**
- Include: GMRS Repeaters

**Scan:**
- `all_skip`: False

### `asgn_gmrs_rpt_18`

**Zones:**
- Include: GMRS Repeaters

**Scan:**
- `all_skip`: False

### `asgn_gmrs_rpt_19`

**Zones:**
- Include: GMRS Repeaters

**Scan:**
- `all_skip`: False

### `asgn_gmrs_rpt_20`

**Zones:**
- Include: GMRS Repeaters

**Scan:**
- `all_skip`: False

### `asgn_gmrs_rpt_21`

**Zones:**
- Include: GMRS Repeaters

**Scan:**
- `all_skip`: False

### `asgn_gmrs_rpt_22`

**Zones:**
- Include: GMRS Repeaters

**Scan:**
- `all_skip`: False

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/gmrs_only.yml
```
