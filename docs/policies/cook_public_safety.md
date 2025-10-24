# cook_public_safety

**File:** `cook_public_safety.yml`  
**Path:** `policies/cook_public_safety.yml`  

## Overview

- **Assignment Overrides:** 9
- **Zone Definitions:** 1
- **Custom Names:** 9
- **RX-Only Assignments:** 9
- **TX-Enabled Assignments:** 0
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions
- **Scan:** Skip settings and scan behavior

## Zone Organization

| Zone | Assignments |
|------|-------------|
| Public Safety | 9 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asg_interop_u1` | Interop UHF 1 |
| `asg_interop_u2` | Interop UHF 2 |
| `asg_interop_v1` | Interop VHF 1 |
| `asg_interop_v2` | Interop VHF 2 |
| `asg_interop_v3` | Interop VHF 3 |
| `asg_interop_v4` | Interop VHF 4 |
| `asg_interop_vmetro3` | Interop VMet3 |
| `asg_interop_vmetro4` | Interop VMet4 |
| `asg_interop_vmetro5` | Interop VMet5 |

## TX/RX Configuration

### RX-Only Assignments

- `asg_interop_u1`
- `asg_interop_u2`
- `asg_interop_v1`
- `asg_interop_v2`
- `asg_interop_v3`
- `asg_interop_v4`
- `asg_interop_vmetro3`
- `asg_interop_vmetro4`
- `asg_interop_vmetro5`

## Scan Configuration

### Scan-Disabled Assignments

- `asg_interop_u1`
- `asg_interop_u2`
- `asg_interop_v1`
- `asg_interop_v2`
- `asg_interop_v3`
- `asg_interop_v4`
- `asg_interop_vmetro3`
- `asg_interop_vmetro4`
- `asg_interop_vmetro5`

## Assignment Details

### `asg_interop_u1`

**Codeplug:**
- `name`: Interop UHF 1
- `rx_only`: True

**Zones:**
- Include: Public Safety

**Scan:**
- `all_skip`: True

### `asg_interop_u2`

**Codeplug:**
- `name`: Interop UHF 2
- `rx_only`: True

**Zones:**
- Include: Public Safety

**Scan:**
- `all_skip`: True

### `asg_interop_v1`

**Codeplug:**
- `name`: Interop VHF 1
- `rx_only`: True

**Zones:**
- Include: Public Safety

**Scan:**
- `all_skip`: True

### `asg_interop_v2`

**Codeplug:**
- `name`: Interop VHF 2
- `rx_only`: True

**Zones:**
- Include: Public Safety

**Scan:**
- `all_skip`: True

### `asg_interop_v3`

**Codeplug:**
- `name`: Interop VHF 3
- `rx_only`: True

**Zones:**
- Include: Public Safety

**Scan:**
- `all_skip`: True

### `asg_interop_v4`

**Codeplug:**
- `name`: Interop VHF 4
- `rx_only`: True

**Zones:**
- Include: Public Safety

**Scan:**
- `all_skip`: True

### `asg_interop_vmetro3`

**Codeplug:**
- `name`: Interop VMet3
- `rx_only`: True

**Zones:**
- Include: Public Safety

**Scan:**
- `all_skip`: True

### `asg_interop_vmetro4`

**Codeplug:**
- `name`: Interop VMet4
- `rx_only`: True

**Zones:**
- Include: Public Safety

**Scan:**
- `all_skip`: True

### `asg_interop_vmetro5`

**Codeplug:**
- `name`: Interop VMet5
- `rx_only`: True

**Zones:**
- Include: Public Safety

**Scan:**
- `all_skip`: True

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/cook_public_safety.yml
```
