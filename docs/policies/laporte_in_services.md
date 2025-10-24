# laporte_in_services

**File:** `laporte_in_services.yml`  
**Path:** `policies/laporte_in_services.yml`  

## Overview

- **Assignment Overrides:** 25
- **Zone Definitions:** 10
- **Custom Names:** 25
- **RX-Only Assignments:** 15
- **TX-Enabled Assignments:** 10
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions
- **Scan:** Skip settings and scan behavior

## Zone Organization

| Zone | Assignments |
|------|-------------|
| DMR Repeater | 1 |
| Emergency / Calling | 2 |
| Fusion Digital | 1 |
| Ham Repeaters | 6 |
| Ham-DMR | 3 |
| LaPorte EMA | 1 |
| LaPorte EMS | 1 |
| LaPorte Fire | 8 |
| LaPorte Sheriff | 4 |
| Westville PD | 1 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asg_laporte_ema_ops` | EMA Ops / Siren |
| `asg_laporte_ems_dispatch` | EMS Dispatch |
| `asg_laporte_fire_dispatch` | Fire Dispatch |
| `asg_laporte_fire_secondary` | Fire Secondary |
| `asg_laporte_fire_tertiary` | Fire Tertiary |
| `asg_laporte_fireground14` | Fireground 1-4 |
| `asg_laporte_fireground5` | Fireground 5 |
| `asg_laporte_fireground6` | Fireground 6 |
| `asg_laporte_fireground7` | Fireground 7 |
| `asg_laporte_jail` | County Jail |
| `asg_laporte_mutual_aid` | Fire Mutual Aid |
| `asg_laporte_sheriff_car` | Sheriff Car-Car |
| `asg_laporte_sheriff_dispatch` | Sheriff Dispatch |
| `asg_laporte_sheriff_swat` | Sheriff SWAT |
| `asg_westville_pd` | Westville B2C |
| `asgn_k9jsi_vhf_fm` | K9JSI VHF |
| `asgn_n9iaa_146_fm` | N9IAA VHF |
| `asgn_n9iaa_crownpoint_dmr` | N9IAA CP DMR |
| `asgn_n9iaa_laporte_dmr` | N9IAA LP DMR |
| `asgn_n9iaa_valpo_dmr` | N9IAA Val DMR |
| `asgn_w9ly_uhf_c4fm` | W9LY UHF C4FM |
| `asgn_w9ly_uhf_fm` | W9LY UHF FM |
| `asgn_w9ly_vhf_c4fm` | W9LY VHF C4FM |
| `asgn_w9ly_vhf_fm` | W9LY VHF FM |
| `asgn_w9sal_uhf_fm` | W9SAL UHF |

## TX/RX Configuration

### RX-Only Assignments

- `asg_laporte_ema_ops`
- `asg_laporte_ems_dispatch`
- `asg_laporte_fire_dispatch`
- `asg_laporte_fire_secondary`
- `asg_laporte_fire_tertiary`
- `asg_laporte_fireground14`
- `asg_laporte_fireground5`
- `asg_laporte_fireground6`
- `asg_laporte_fireground7`
- `asg_laporte_jail`
- `asg_laporte_mutual_aid`
- `asg_laporte_sheriff_car`
- `asg_laporte_sheriff_dispatch`
- `asg_laporte_sheriff_swat`
- `asg_westville_pd`

### TX-Enabled Assignments

- `asgn_k9jsi_vhf_fm`
- `asgn_n9iaa_146_fm`
- `asgn_n9iaa_crownpoint_dmr`
- `asgn_n9iaa_laporte_dmr`
- `asgn_n9iaa_valpo_dmr`
- `asgn_w9ly_uhf_c4fm`
- `asgn_w9ly_uhf_fm`
- `asgn_w9ly_vhf_c4fm`
- `asgn_w9ly_vhf_fm`
- `asgn_w9sal_uhf_fm`

## Scan Configuration

### Scan-Disabled Assignments

- `asg_laporte_ema_ops`
- `asg_laporte_ems_dispatch`
- `asg_laporte_fire_dispatch`
- `asg_laporte_fire_secondary`
- `asg_laporte_fire_tertiary`
- `asg_laporte_fireground14`
- `asg_laporte_fireground5`
- `asg_laporte_fireground6`
- `asg_laporte_fireground7`
- `asg_laporte_jail`
- `asg_laporte_mutual_aid`
- `asg_laporte_sheriff_car`
- `asg_laporte_sheriff_dispatch`
- `asg_laporte_sheriff_swat`
- `asg_westville_pd`

## Assignment Details

### `asg_laporte_ema_ops`

**Codeplug:**
- `name`: EMA Ops / Siren
- `rx_only`: True

**Zones:**
- Include: LaPorte EMA

**Scan:**
- `all_skip`: True

### `asg_laporte_ems_dispatch`

**Codeplug:**
- `name`: EMS Dispatch
- `rx_only`: True

**Zones:**
- Include: LaPorte EMS

**Scan:**
- `all_skip`: True

### `asg_laporte_fire_dispatch`

**Codeplug:**
- `name`: Fire Dispatch
- `rx_only`: True

**Zones:**
- Include: LaPorte Fire

**Scan:**
- `all_skip`: True

### `asg_laporte_fire_secondary`

**Codeplug:**
- `name`: Fire Secondary
- `rx_only`: True

**Zones:**
- Include: LaPorte Fire

**Scan:**
- `all_skip`: True

### `asg_laporte_fire_tertiary`

**Codeplug:**
- `name`: Fire Tertiary
- `rx_only`: True

**Zones:**
- Include: LaPorte Fire

**Scan:**
- `all_skip`: True

### `asg_laporte_fireground14`

**Codeplug:**
- `name`: Fireground 1-4
- `rx_only`: True

**Zones:**
- Include: LaPorte Fire

**Scan:**
- `all_skip`: True

### `asg_laporte_fireground5`

**Codeplug:**
- `name`: Fireground 5
- `rx_only`: True

**Zones:**
- Include: LaPorte Fire

**Scan:**
- `all_skip`: True

### `asg_laporte_fireground6`

**Codeplug:**
- `name`: Fireground 6
- `rx_only`: True

**Zones:**
- Include: LaPorte Fire

**Scan:**
- `all_skip`: True

### `asg_laporte_fireground7`

**Codeplug:**
- `name`: Fireground 7
- `rx_only`: True

**Zones:**
- Include: LaPorte Fire

**Scan:**
- `all_skip`: True

### `asg_laporte_jail`

**Codeplug:**
- `name`: County Jail
- `rx_only`: True

**Zones:**
- Include: LaPorte Sheriff

**Scan:**
- `all_skip`: True

### `asg_laporte_mutual_aid`

**Codeplug:**
- `name`: Fire Mutual Aid
- `rx_only`: True

**Zones:**
- Include: LaPorte Fire

**Scan:**
- `all_skip`: True

### `asg_laporte_sheriff_car`

**Codeplug:**
- `name`: Sheriff Car-Car
- `rx_only`: True

**Zones:**
- Include: LaPorte Sheriff

**Scan:**
- `all_skip`: True

### `asg_laporte_sheriff_dispatch`

**Codeplug:**
- `name`: Sheriff Dispatch
- `rx_only`: True

**Zones:**
- Include: LaPorte Sheriff

**Scan:**
- `all_skip`: True

### `asg_laporte_sheriff_swat`

**Codeplug:**
- `name`: Sheriff SWAT
- `rx_only`: True

**Zones:**
- Include: LaPorte Sheriff

**Scan:**
- `all_skip`: True

### `asg_westville_pd`

**Codeplug:**
- `name`: Westville B2C
- `rx_only`: True

**Zones:**
- Include: Westville PD

**Scan:**
- `all_skip`: True

### `asgn_k9jsi_vhf_fm`

**Codeplug:**
- `name`: K9JSI VHF
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters, Emergency / Calling

### `asgn_n9iaa_146_fm`

**Codeplug:**
- `name`: N9IAA VHF
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters, Emergency / Calling

### `asgn_n9iaa_crownpoint_dmr`

**Codeplug:**
- `name`: N9IAA CP DMR
- `preferred_contacts`: ['tg_8', 'tg_3118', 'tg_1', 'tg_3', 'tg_9', 'tg_5000', 'tg_4000']
- `rx_only`: False

**Zones:**
- Include: Ham-DMR

### `asgn_n9iaa_laporte_dmr`

**Codeplug:**
- `name`: N9IAA LP DMR
- `preferred_contacts`: ['tg_8', 'tg_3118', 'tg_1', 'tg_3', 'tg_9', 'tg_5000', 'tg_4000']
- `rx_only`: False

**Zones:**
- Include: Ham-DMR

### `asgn_n9iaa_valpo_dmr`

**Codeplug:**
- `name`: N9IAA Val DMR
- `preferred_contacts`: ['tg_8', 'tg_3118', 'tg_1', 'tg_3', 'tg_9', 'tg_5000', 'tg_4000']
- `rx_only`: False

**Zones:**
- Include: Ham-DMR

### `asgn_w9ly_uhf_c4fm`

**Codeplug:**
- `name`: W9LY UHF C4FM
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters, Fusion Digital

### `asgn_w9ly_uhf_fm`

**Codeplug:**
- `name`: W9LY UHF FM
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters

### `asgn_w9ly_vhf_c4fm`

**Codeplug:**
- `name`: W9LY VHF C4FM
- `rx_only`: False

**Zones:**
- Include: DMR Repeater

### `asgn_w9ly_vhf_fm`

**Codeplug:**
- `name`: W9LY VHF FM
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters

### `asgn_w9sal_uhf_fm`

**Codeplug:**
- `name`: W9SAL UHF
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/laporte_in_services.yml
```
