# niles_kc8brs

**File:** `niles_kc8brs.yml`  
**Path:** `policies/niles_kc8brs.yml`  

## Overview

- **Assignment Overrides:** 1
- **Zone Definitions:** 1
- **Custom Names:** 1
- **RX-Only Assignments:** 0
- **TX-Enabled Assignments:** 1
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions

## Zone Organization

| Zone | Assignments |
|------|-------------|
| Ham Repeaters | 1 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asgn_kc8brs_vhf_fm` | KC8BRS 147.180 |

## TX/RX Configuration

### TX-Enabled Assignments

- `asgn_kc8brs_vhf_fm`

## Assignment Details

### `asgn_kc8brs_vhf_fm`

**Codeplug:**
- `name`: KC8BRS 147.180
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/niles_kc8brs.yml
```
