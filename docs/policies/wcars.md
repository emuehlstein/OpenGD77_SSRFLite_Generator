# wcars

**File:** `wcars.yml`  
**Path:** `policies/wcars.yml`  

## Overview

- **Assignment Overrides:** 1
- **Zone Definitions:** 1
- **Custom Names:** 1
- **RX-Only Assignments:** 0
- **TX-Enabled Assignments:** 0
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions

## Zone Organization

| Zone | Assignments |
|------|-------------|
| Amateur Nets | 1 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asg_wcars_thursday_net` | WCARS Thu Net |

## Assignment Details

### `asg_wcars_thursday_net`

**Codeplug:**
- `name`: WCARS Thu Net

**Zones:**
- Include: Amateur Nets

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/wcars.yml
```
