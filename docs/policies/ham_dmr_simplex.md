# ham_dmr_simplex

**File:** `ham_dmr_simplex.yml`  
**Path:** `policies/ham_dmr_simplex.yml`  

## Overview

- **Assignment Overrides:** 14
- **Zone Definitions:** 1
- **Custom Names:** 14
- **RX-Only Assignments:** 0
- **TX-Enabled Assignments:** 0
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions

## Zone Organization

| Zone | Assignments |
|------|-------------|
| Ham DMR Simplex | 14 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asg_dmr_hs_4304125` | HS 4304125 |
| `asg_dmr_hs_4304250` | HS 4304250 |
| `asg_dmr_hs_4394125` | HS 4394125 |
| `asg_dmr_hs_4394250` | HS 4394250 |
| `asg_dmr_hs_duplex_4304375` | HS 4304375 |
| `asg_dmr_hs_duplex_4304500` | HS 4304500 |
| `asg_dmr_hs_duplex_4304625` | HS 4304625 |
| `asg_dmr_hs_duplex_4304750` | HS 4304750 |
| `asg_dmr_hs_duplex_4394375` | HS 4394375 |
| `asg_dmr_hs_duplex_4394500` | HS 4394500 |
| `asg_dmr_hs_duplex_4394625` | HS 4394625 |
| `asg_dmr_hs_duplex_4394750` | HS 4394750 |
| `asg_dmr_smpx_446075` | DMR Smpx B |
| `asg_dmr_smpx_446500` | DMR Smpx A |

## Assignment Details

### `asg_dmr_hs_4304125`

**Codeplug:**
- `all_skip`: True
- `name`: HS 4304125
- `preferred_contacts`: ['ct_dmr_simplex']

**Zones:**
- Include: Ham DMR Simplex

### `asg_dmr_hs_4304250`

**Codeplug:**
- `all_skip`: True
- `name`: HS 4304250
- `preferred_contacts`: ['ct_dmr_simplex']

**Zones:**
- Include: Ham DMR Simplex

### `asg_dmr_hs_4394125`

**Codeplug:**
- `all_skip`: True
- `name`: HS 4394125
- `preferred_contacts`: ['ct_dmr_simplex']

**Zones:**
- Include: Ham DMR Simplex

### `asg_dmr_hs_4394250`

**Codeplug:**
- `all_skip`: True
- `name`: HS 4394250
- `preferred_contacts`: ['ct_dmr_simplex']

**Zones:**
- Include: Ham DMR Simplex

### `asg_dmr_hs_duplex_4304375`

**Codeplug:**
- `all_skip`: True
- `name`: HS 4304375
- `preferred_contacts`: ['ct_dmr_simplex']

**Zones:**
- Include: Ham DMR Simplex

### `asg_dmr_hs_duplex_4304500`

**Codeplug:**
- `all_skip`: True
- `name`: HS 4304500
- `preferred_contacts`: ['ct_dmr_simplex']

**Zones:**
- Include: Ham DMR Simplex

### `asg_dmr_hs_duplex_4304625`

**Codeplug:**
- `all_skip`: True
- `name`: HS 4304625
- `preferred_contacts`: ['ct_dmr_simplex']

**Zones:**
- Include: Ham DMR Simplex

### `asg_dmr_hs_duplex_4304750`

**Codeplug:**
- `all_skip`: True
- `name`: HS 4304750
- `preferred_contacts`: ['ct_dmr_simplex']

**Zones:**
- Include: Ham DMR Simplex

### `asg_dmr_hs_duplex_4394375`

**Codeplug:**
- `all_skip`: True
- `name`: HS 4394375
- `preferred_contacts`: ['ct_dmr_simplex']

**Zones:**
- Include: Ham DMR Simplex

### `asg_dmr_hs_duplex_4394500`

**Codeplug:**
- `all_skip`: True
- `name`: HS 4394500
- `preferred_contacts`: ['ct_dmr_simplex']

**Zones:**
- Include: Ham DMR Simplex

### `asg_dmr_hs_duplex_4394625`

**Codeplug:**
- `all_skip`: True
- `name`: HS 4394625
- `preferred_contacts`: ['ct_dmr_simplex']

**Zones:**
- Include: Ham DMR Simplex

### `asg_dmr_hs_duplex_4394750`

**Codeplug:**
- `all_skip`: True
- `name`: HS 4394750
- `preferred_contacts`: ['ct_dmr_simplex']

**Zones:**
- Include: Ham DMR Simplex

### `asg_dmr_smpx_446075`

**Codeplug:**
- `all_skip`: True
- `name`: DMR Smpx B
- `preferred_contacts`: ['ct_dmr_simplex']

**Zones:**
- Include: Ham DMR Simplex

### `asg_dmr_smpx_446500`

**Codeplug:**
- `all_skip`: True
- `name`: DMR Smpx A
- `preferred_contacts`: ['ct_dmr_simplex']

**Zones:**
- Include: Ham DMR Simplex

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/ham_dmr_simplex.yml
```
