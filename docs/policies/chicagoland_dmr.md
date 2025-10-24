# chicagoland_dmr

**File:** `chicagoland_dmr.yml`  
**Path:** `policies/chicagoland_dmr.yml`  

## Overview

- **Assignment Overrides:** 2
- **Zone Definitions:** 1
- **Custom Names:** 2
- **RX-Only Assignments:** 0
- **TX-Enabled Assignments:** 0
- **Scan-Enabled Assignments:** 2

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions
- **Scan:** Skip settings and scan behavior

## Zone Organization

| Zone | Assignments |
|------|-------------|
| Ham Repeaters | 2 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asgn_cl_loop` | CL Loop |
| `asgn_cl_schaumburg` | CL Schaumburg |

## Scan Configuration

### Scan-Enabled Assignments

- `asgn_cl_loop`
- `asgn_cl_schaumburg`

## Assignment Details

### `asgn_cl_loop`

**Codeplug:**
- `name`: CL Loop
- `preferred_contacts`: ['tg_9', 'tg_3181', 'tg_3166', 'tg_3117', 'tg_3169', 'tg_310', 'tg_9998']

**Zones:**
- Include: Ham Repeaters

**Scan:**
- `all_skip`: False

### `asgn_cl_schaumburg`

**Codeplug:**
- `name`: CL Schaumburg
- `preferred_contacts`: ['tg_9', 'tg_3181', 'tg_3166', 'tg_3117', 'tg_3169', 'tg_310', 'tg_9998']

**Zones:**
- Include: Ham Repeaters

**Scan:**
- `all_skip`: False

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/chicagoland_dmr.yml
```
