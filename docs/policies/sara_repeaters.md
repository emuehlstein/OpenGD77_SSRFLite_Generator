# sara_repeaters

**File:** `sara_repeaters.yml`  
**Path:** `policies/sara_repeaters.yml`  

## Overview

- **Assignment Overrides:** 3
- **Zone Definitions:** 3
- **Custom Names:** 3
- **RX-Only Assignments:** 0
- **TX-Enabled Assignments:** 3
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions

## Zone Organization

| Zone | Assignments |
|------|-------------|
| DMR Repeater | 1 |
| Emergency / Calling | 1 |
| Ham Repeaters | 2 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asgn_ka9hhh_2m_fm` | SARA VHF |
| `asgn_ka9hhh_440_fm` | SARA UHF |
| `asgn_na9pl_440_c4fm` | SARA UHF C4FM |

## TX/RX Configuration

### TX-Enabled Assignments

- `asgn_ka9hhh_2m_fm`
- `asgn_ka9hhh_440_fm`
- `asgn_na9pl_440_c4fm`

## Assignment Details

### `asgn_ka9hhh_2m_fm`

**Codeplug:**
- `name`: SARA VHF
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters

### `asgn_ka9hhh_440_fm`

**Codeplug:**
- `name`: SARA UHF
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters, Emergency / Calling

### `asgn_na9pl_440_c4fm`

**Codeplug:**
- `name`: SARA UHF C4FM
- `rx_only`: False

**Zones:**
- Include: DMR Repeater

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/sara_repeaters.yml
```
