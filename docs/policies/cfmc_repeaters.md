# cfmc_repeaters

**File:** `cfmc_repeaters.yml`  
**Path:** `policies/cfmc_repeaters.yml`  

## Overview

- **Assignment Overrides:** 7
- **Zone Definitions:** 3
- **Custom Names:** 7
- **RX-Only Assignments:** 0
- **TX-Enabled Assignments:** 7
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions

## Zone Organization

| Zone | Assignments |
|------|-------------|
| DMR Repeater | 2 |
| Emergency / Calling | 2 |
| Ham Repeaters | 5 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asgn_cfmc_220_north` | CFMC 220 North |
| `asgn_cfmc_220_south` | CFMC 220 S |
| `asgn_cfmc_2m` | CFMC 2m FM |
| `asgn_cfmc_440` | CFMC 440 FM |
| `asgn_cfmc_dstar_440` | CFMC D-STAR 440 |
| `asgn_cfmc_fusion_2m_c4fm` | CFMC 2m C4FM |
| `asgn_cfmc_fusion_2m_fm` | CFMC 2m FM |

## TX/RX Configuration

### TX-Enabled Assignments

- `asgn_cfmc_220_north`
- `asgn_cfmc_220_south`
- `asgn_cfmc_2m`
- `asgn_cfmc_440`
- `asgn_cfmc_dstar_440`
- `asgn_cfmc_fusion_2m_c4fm`
- `asgn_cfmc_fusion_2m_fm`

## Assignment Details

### `asgn_cfmc_220_north`

**Codeplug:**
- `name`: CFMC 220 North
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters

### `asgn_cfmc_220_south`

**Codeplug:**
- `name`: CFMC 220 S
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters

### `asgn_cfmc_2m`

**Codeplug:**
- `name`: CFMC 2m FM
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters, Emergency / Calling

### `asgn_cfmc_440`

**Codeplug:**
- `name`: CFMC 440 FM
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters, Emergency / Calling

### `asgn_cfmc_dstar_440`

**Codeplug:**
- `name`: CFMC D-STAR 440
- `rx_only`: False

**Zones:**
- Include: DMR Repeater

### `asgn_cfmc_fusion_2m_c4fm`

**Codeplug:**
- `name`: CFMC 2m C4FM
- `rx_only`: False

**Zones:**
- Include: DMR Repeater

### `asgn_cfmc_fusion_2m_fm`

**Codeplug:**
- `name`: CFMC 2m FM
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/cfmc_repeaters.yml
```
