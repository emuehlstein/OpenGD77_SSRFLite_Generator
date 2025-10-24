# murs

**File:** `murs.yml`  
**Path:** `policies/murs.yml`  

## Overview

- **Assignment Overrides:** 5
- **Zone Definitions:** 1
- **Custom Names:** 5
- **RX-Only Assignments:** 0
- **TX-Enabled Assignments:** 5
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions

## Zone Organization

| Zone | Assignments |
|------|-------------|
| MURS | 5 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asgn_murs_1` | MURS 1 |
| `asgn_murs_2` | MURS 2 |
| `asgn_murs_3` | MURS 3 |
| `asgn_murs_4` | MURS 4 |
| `asgn_murs_5` | MURS 5 |

## TX/RX Configuration

### TX-Enabled Assignments

- `asgn_murs_1`
- `asgn_murs_2`
- `asgn_murs_3`
- `asgn_murs_4`
- `asgn_murs_5`

## Assignment Details

### `asgn_murs_1`

**Codeplug:**
- `all_skip`: True
- `name`: MURS 1
- `rx_only`: False

**Zones:**
- Include: MURS

### `asgn_murs_2`

**Codeplug:**
- `all_skip`: True
- `name`: MURS 2
- `rx_only`: False

**Zones:**
- Include: MURS

### `asgn_murs_3`

**Codeplug:**
- `all_skip`: True
- `name`: MURS 3
- `rx_only`: False

**Zones:**
- Include: MURS

### `asgn_murs_4`

**Codeplug:**
- `all_skip`: True
- `name`: MURS 4
- `rx_only`: False

**Zones:**
- Include: MURS

### `asgn_murs_5`

**Codeplug:**
- `all_skip`: True
- `name`: MURS 5
- `rx_only`: False

**Zones:**
- Include: MURS

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/murs.yml
```
