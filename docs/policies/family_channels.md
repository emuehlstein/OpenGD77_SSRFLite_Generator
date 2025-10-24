# family_channels

**File:** `family_channels.yml`  
**Path:** `policies/family_channels.yml`  

## Overview

- **Assignment Overrides:** 17
- **Zone Definitions:** 4
- **Custom Names:** 17
- **RX-Only Assignments:** 0
- **TX-Enabled Assignments:** 17
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions

## Zone Organization

| Zone | Assignments |
|------|-------------|
| Family Ops | 13 |
| Family Ops Digital | 4 |
| Ham Repeaters | 2 |
| Ham UHF | 1 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asgn_family_f10_evnst` | F10 Evnst 700 |
| `asgn_family_f11_nrthbrk` | F11 Nrthbrk |
| `asgn_family_f13_uhf_call` | F13 UHF Call |
| `asgn_family_f14_ns9rc` | F14 NS9RC UHF |
| `asgn_family_f15_cmfc` | F15 CMFC UHF |
| `asgn_family_f1_all` | F1 All |
| `asgn_family_f2_team_a` | F2 Team A |
| `asgn_family_f3_team_b` | F3 Team B |
| `asgn_family_f4_team_c` | F4 Team C |
| `asgn_family_f5_road` | F5 Road |
| `asgn_family_f6_rptr` | F6 RPTR |
| `asgn_family_f8_evnstn` | F8 Evnstn 725 |
| `asgn_family_f9_prkrdg` | F9 PrkRdg 675 |
| `asgn_family_fd1_all` | FD1 All |
| `asgn_family_fd2_team_a` | FD2 Team A |
| `asgn_family_fd3_team_b` | FD3 Team B |
| `asgn_family_fd4_team_c` | FD4 Team C |

## TX/RX Configuration

### TX-Enabled Assignments

- `asgn_family_f10_evnst`
- `asgn_family_f11_nrthbrk`
- `asgn_family_f13_uhf_call`
- `asgn_family_f14_ns9rc`
- `asgn_family_f15_cmfc`
- `asgn_family_f1_all`
- `asgn_family_f2_team_a`
- `asgn_family_f3_team_b`
- `asgn_family_f4_team_c`
- `asgn_family_f5_road`
- `asgn_family_f6_rptr`
- `asgn_family_f8_evnstn`
- `asgn_family_f9_prkrdg`
- `asgn_family_fd1_all`
- `asgn_family_fd2_team_a`
- `asgn_family_fd3_team_b`
- `asgn_family_fd4_team_c`

## Assignment Details

### `asgn_family_f10_evnst`

**Codeplug:**
- `name`: F10 Evnst 700
- `rx_only`: False
- `scan_list`: Family SL

**Zones:**
- Include: Family Ops

### `asgn_family_f11_nrthbrk`

**Codeplug:**
- `duplex`: -
- `name`: F11 Nrthbrk
- `rx_only`: False
- `scan_list`: Family SL
- `tx_offset_mhz`: -2.0

**Zones:**
- Include: Family Ops

### `asgn_family_f13_uhf_call`

**Codeplug:**
- `name`: F13 UHF Call
- `rx_only`: False
- `scan_list`: Family SL

**Zones:**
- Include: Family Ops, Ham UHF

### `asgn_family_f14_ns9rc`

**Codeplug:**
- `duplex`: +
- `name`: F14 NS9RC UHF
- `rx_only`: False
- `tx_offset_mhz`: 5.0

**Zones:**
- Include: Family Ops, Ham Repeaters

### `asgn_family_f15_cmfc`

**Codeplug:**
- `duplex`: +
- `name`: F15 CMFC UHF
- `rx_only`: False
- `scan_list`: HamRptrs SL
- `tx_offset_mhz`: 5.0

**Zones:**
- Include: Family Ops, Ham Repeaters

### `asgn_family_f1_all`

**Codeplug:**
- `name`: F1 All
- `rx_only`: False
- `scan_list`: Family SL

**Zones:**
- Include: Family Ops

### `asgn_family_f2_team_a`

**Codeplug:**
- `name`: F2 Team A
- `rx_only`: False

**Zones:**
- Include: Family Ops

### `asgn_family_f3_team_b`

**Codeplug:**
- `name`: F3 Team B
- `rx_only`: False
- `scan_list`: Family SL

**Zones:**
- Include: Family Ops

### `asgn_family_f4_team_c`

**Codeplug:**
- `name`: F4 Team C
- `rx_only`: False

**Zones:**
- Include: Family Ops

### `asgn_family_f5_road`

**Codeplug:**
- `name`: F5 Road
- `rx_only`: False
- `scan_list`: Family SL

**Zones:**
- Include: Family Ops

### `asgn_family_f6_rptr`

**Codeplug:**
- `duplex`: +
- `name`: F6 RPTR
- `rx_only`: False
- `scan_list`: Family SL
- `tx_offset_mhz`: 5.0

**Zones:**
- Include: Family Ops

### `asgn_family_f8_evnstn`

**Codeplug:**
- `duplex`: +
- `name`: F8 Evnstn 725
- `rx_only`: False
- `scan_list`: Family SL
- `tx_offset_mhz`: 5.025

**Zones:**
- Include: Family Ops

### `asgn_family_f9_prkrdg`

**Codeplug:**
- `duplex`: +
- `name`: F9 PrkRdg 675
- `rx_only`: False
- `scan_list`: Family SL
- `tx_offset_mhz`: 5.0

**Zones:**
- Include: Family Ops

### `asgn_family_fd1_all`

**Codeplug:**
- `name`: FD1 All
- `preferred_contacts`: ['contact_local99', 'contact_eric']
- `rx_only`: False
- `scan_list`: Family SL

**Zones:**
- Include: Family Ops Digital

### `asgn_family_fd2_team_a`

**Codeplug:**
- `name`: FD2 Team A
- `preferred_contacts`: ['contact_local99', 'contact_eric']
- `rx_only`: False
- `scan_list`: Family SL

**Zones:**
- Include: Family Ops Digital

### `asgn_family_fd3_team_b`

**Codeplug:**
- `name`: FD3 Team B
- `preferred_contacts`: ['contact_local99', 'contact_eric']
- `rx_only`: False
- `scan_list`: Family SL

**Zones:**
- Include: Family Ops Digital

### `asgn_family_fd4_team_c`

**Codeplug:**
- `name`: FD4 Team C
- `preferred_contacts`: ['contact_local99', 'contact_eric']
- `rx_only`: False
- `scan_list`: Family SL

**Zones:**
- Include: Family Ops Digital

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/family_channels.yml
```
