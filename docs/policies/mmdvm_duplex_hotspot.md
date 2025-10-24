# mmdvm_duplex_hotspot

**File:** `mmdvm_duplex_hotspot.yml`  
**Path:** `policies/mmdvm_duplex_hotspot.yml`  

## Overview

- **Assignment Overrides:** 2
- **Zone Definitions:** 1
- **Custom Names:** 2
- **RX-Only Assignments:** 0
- **TX-Enabled Assignments:** 2
- **Scan-Enabled Assignments:** 2

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions
- **Scan:** Skip settings and scan behavior

## Zone Organization

| Zone | Assignments |
|------|-------------|
| Ham-Hotspot | 2 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asgn_hotspot_brandmeister` | Hotspot BM |
| `asgn_hotspot_tgif` | Hotspot TGIF |

## TX/RX Configuration

### TX-Enabled Assignments

- `asgn_hotspot_brandmeister`
- `asgn_hotspot_tgif`

## Scan Configuration

### Scan-Enabled Assignments

- `asgn_hotspot_brandmeister`
- `asgn_hotspot_tgif`

## Assignment Details

### `asgn_hotspot_brandmeister`

**Codeplug:**
- `name`: Hotspot BM
- `power`: Low
- `preferred_contacts`: ['tg_hs_bm_91', 'tg_hs_bm_93', 'tg_hs_bm_3100', 'tg_hs_bm_3117', 'tg_hs_bm_310', 'tg_hs_bm_9990', 'tg_hs_bm_4000', 'tg_hs_bm_5000']
- `rx_only`: False
- `tot_seconds`: 180

**Zones:**
- Include: Ham-Hotspot

**Scan:**
- `all_skip`: False
- `zone_skip`: False

### `asgn_hotspot_tgif`

**Codeplug:**
- `name`: Hotspot TGIF
- `power`: Low
- `preferred_contacts`: ['tg_hs_tgif_31665', 'tg_hs_tgif_31672', 'tg_hs_tgif_556', 'tg_hs_tgif_9990', 'tg_hs_tgif_4000']
- `rx_only`: False
- `tot_seconds`: 180

**Zones:**
- Include: Ham-Hotspot

**Scan:**
- `all_skip`: False
- `zone_skip`: False

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/mmdvm_duplex_hotspot.yml
```
