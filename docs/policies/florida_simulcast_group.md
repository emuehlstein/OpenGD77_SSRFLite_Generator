# florida_simulcast_group

**File:** `florida_simulcast_group.yml`  
**Path:** `policies/florida_simulcast_group.yml`  

## Overview

- **Assignment Overrides:** 15
- **Zone Definitions:** 1
- **Custom Names:** 15
- **RX-Only Assignments:** 1
- **TX-Enabled Assignments:** 1
- **Scan-Enabled Assignments:** 2

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions
- **Scan:** Skip settings and scan behavior

## Zone Organization

| Zone | Assignments |
|------|-------------|
| Ham Repeaters | 15 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asgn_fsg_stpete_444_fm` | FSG St Pete 444 FM |
| `asgn_fsg_stpete_444_p25` | FSG St Pete 444 P25 |
| `asgn_ka9rix_tampa_dstar` | FSG Tampa KA9RIX D-Star |
| `asgn_ka9rix_tampa_fm` | FSG Tampa KA9RIX |
| `asgn_kj4shl_stpete_dmr` | FSG St Pete DMR |
| `asgn_kj4shl_stpete_nxdn` | FSG St Pete NXDN |
| `asgn_kj4shl_tampa_dmr` | FSG Tampa DMR |
| `asgn_w9cr_tampa_224_fm` | FSG Tampa 224 |
| `asgn_w9cr_tampa_443_fm` | FSG Tampa 443 FM |
| `asgn_w9cr_tampa_443_p25` | FSG Tampa 443 P25 |
| `asgn_w9cr_tampa_927_fm` | FSG Tampa 927 FM |
| `asgn_w9cr_tampa_927_p25` | FSG Tampa 927 P25 |
| `asgn_wd4scd_remote_rx` | WD4SCD Remote RX |
| `asgn_wraf954_tampa_fm` | FSG Tampa GMRS |
| `asgn_wraf954_tampa_p25` | FSG Tampa GMRS P25 |

## TX/RX Configuration

### RX-Only Assignments

- `asgn_wd4scd_remote_rx`

### TX-Enabled Assignments

- `asgn_kj4shl_stpete_nxdn`

## Scan Configuration

### Scan-Enabled Assignments

- `asgn_kj4shl_stpete_dmr`
- `asgn_kj4shl_tampa_dmr`

### Scan-Disabled Assignments

- `asgn_wd4scd_remote_rx`
- `asgn_wraf954_tampa_fm`
- `asgn_wraf954_tampa_p25`

## Assignment Details

### `asgn_fsg_stpete_444_fm`

**Codeplug:**
- `name`: FSG St Pete 444 FM
- `power`: High

**Zones:**
- Include: Ham Repeaters

### `asgn_fsg_stpete_444_p25`

**Codeplug:**
- `name`: FSG St Pete 444 P25
- `power`: High

**Zones:**
- Include: Ham Repeaters

### `asgn_ka9rix_tampa_dstar`

**Codeplug:**
- `name`: FSG Tampa KA9RIX D-Star
- `power`: High

**Zones:**
- Include: Ham Repeaters

### `asgn_ka9rix_tampa_fm`

**Codeplug:**
- `name`: FSG Tampa KA9RIX
- `power`: High

**Zones:**
- Include: Ham Repeaters

### `asgn_kj4shl_stpete_dmr`

**Codeplug:**
- `name`: FSG St Pete DMR
- `power`: High
- `preferred_contacts`: ['tg_fsg_florida_simulcast', 'tg_fsg_worldwide', 'tg_fsg_north_america', 'tg_fsg_worldwide_english', 'tg_fsg_tac310', 'tg_fsg_tac311', 'tg_fsg_tac312', 'tg_fsg_bridge_3100', 'tg_fsg_southeast_regional', 'tg_fsg_parrot', 'tg_fsg_first_coast', 'tg_fsg_southeast_florida', 'tg_fsg_local_repeater', 'tg_fsg_local_2', 'tg_fsg_florida_statewide']
- `tg_list_name`: FSG SP

**Zones:**
- Include: Ham Repeaters

**Scan:**
- `all_skip`: False

### `asgn_kj4shl_stpete_nxdn`

**Codeplug:**
- `name`: FSG St Pete NXDN
- `power`: High
- `rx_only`: False

**Zones:**
- Include: Ham Repeaters

### `asgn_kj4shl_tampa_dmr`

**Codeplug:**
- `name`: FSG Tampa DMR
- `power`: High
- `preferred_contacts`: ['tg_fsg_florida_simulcast', 'tg_fsg_worldwide', 'tg_fsg_north_america', 'tg_fsg_worldwide_english', 'tg_fsg_tac310', 'tg_fsg_tac311', 'tg_fsg_tac312', 'tg_fsg_bridge_3100', 'tg_fsg_southeast_regional', 'tg_fsg_parrot', 'tg_fsg_first_coast', 'tg_fsg_southeast_florida', 'tg_fsg_local_repeater', 'tg_fsg_local_2', 'tg_fsg_florida_statewide']
- `tg_list_name`: FSG TP

**Zones:**
- Include: Ham Repeaters

**Scan:**
- `all_skip`: False

### `asgn_w9cr_tampa_224_fm`

**Codeplug:**
- `name`: FSG Tampa 224
- `power`: High

**Zones:**
- Include: Ham Repeaters

### `asgn_w9cr_tampa_443_fm`

**Codeplug:**
- `name`: FSG Tampa 443 FM
- `power`: High

**Zones:**
- Include: Ham Repeaters

### `asgn_w9cr_tampa_443_p25`

**Codeplug:**
- `name`: FSG Tampa 443 P25
- `power`: High

**Zones:**
- Include: Ham Repeaters

### `asgn_w9cr_tampa_927_fm`

**Codeplug:**
- `name`: FSG Tampa 927 FM
- `power`: High

**Zones:**
- Include: Ham Repeaters

### `asgn_w9cr_tampa_927_p25`

**Codeplug:**
- `name`: FSG Tampa 927 P25
- `power`: High

**Zones:**
- Include: Ham Repeaters

### `asgn_wd4scd_remote_rx`

**Codeplug:**
- `name`: WD4SCD Remote RX
- `power`: Low
- `rx_only`: True

**Zones:**
- Include: Ham Repeaters

**Scan:**
- `all_skip`: True

### `asgn_wraf954_tampa_fm`

**Codeplug:**
- `name`: FSG Tampa GMRS
- `power`: High

**Zones:**
- Include: Ham Repeaters

**Scan:**
- `all_skip`: True

### `asgn_wraf954_tampa_p25`

**Codeplug:**
- `name`: FSG Tampa GMRS P25
- `power`: High

**Zones:**
- Include: Ham Repeaters

**Scan:**
- `all_skip`: True

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/florida_simulcast_group.yml
```
