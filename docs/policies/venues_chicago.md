# venues_chicago

**File:** `venues_chicago.yml`  
**Path:** `policies/venues_chicago.yml`  

## Overview

- **Assignment Overrides:** 15
- **Zone Definitions:** 1
- **Custom Names:** 15
- **RX-Only Assignments:** 15
- **TX-Enabled Assignments:** 0
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions
- **Scan:** Skip settings and scan behavior

## Zone Organization

| Zone | Assignments |
|------|-------------|
| Business | 15 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asg_333wab` | 333 S Wabash |
| `asg_allegro` | Allegro FM |
| `asg_ama` | AMA Plaza |
| `asg_aon` | Aon Tower |
| `asg_bcbs` | BCBS HQ |
| `asg_mccormick` | McCormick Pl |
| `asg_merch` | Merch Mart |
| `asg_navy_pier` | Navy Pier |
| `asg_oldpo` | Old Post Office |
| `asg_soldier` | Soldier Field |
| `asg_two77` | Two Prud FM |
| `asg_two_pru` | Two Prudential |
| `asg_united` | United Center |
| `asg_wrigley_dmr` | Wrigley DMR |
| `asg_wrigley_fm` | Wrigley FM |

## TX/RX Configuration

### RX-Only Assignments

- `asg_333wab`
- `asg_allegro`
- `asg_ama`
- `asg_aon`
- `asg_bcbs`
- `asg_mccormick`
- `asg_merch`
- `asg_navy_pier`
- `asg_oldpo`
- `asg_soldier`
- `asg_two77`
- `asg_two_pru`
- `asg_united`
- `asg_wrigley_dmr`
- `asg_wrigley_fm`

## Scan Configuration

### Scan-Disabled Assignments

- `asg_333wab`
- `asg_allegro`
- `asg_ama`
- `asg_aon`
- `asg_bcbs`
- `asg_mccormick`
- `asg_merch`
- `asg_navy_pier`
- `asg_oldpo`
- `asg_soldier`
- `asg_two77`
- `asg_two_pru`
- `asg_united`
- `asg_wrigley_dmr`
- `asg_wrigley_fm`

## Assignment Details

### `asg_333wab`

**Codeplug:**
- `name`: 333 S Wabash
- `rx_only`: True

**Zones:**
- Include: Business

**Scan:**
- `all_skip`: True

### `asg_allegro`

**Codeplug:**
- `name`: Allegro FM
- `rx_only`: True

**Zones:**
- Include: Business

**Scan:**
- `all_skip`: True

### `asg_ama`

**Codeplug:**
- `name`: AMA Plaza
- `rx_only`: True

**Zones:**
- Include: Business

**Scan:**
- `all_skip`: True

### `asg_aon`

**Codeplug:**
- `name`: Aon Tower
- `rx_only`: True

**Zones:**
- Include: Business

**Scan:**
- `all_skip`: True

### `asg_bcbs`

**Codeplug:**
- `name`: BCBS HQ
- `rx_only`: True

**Zones:**
- Include: Business

**Scan:**
- `all_skip`: True

### `asg_mccormick`

**Codeplug:**
- `name`: McCormick Pl
- `rx_only`: True

**Zones:**
- Include: Business

**Scan:**
- `all_skip`: True

### `asg_merch`

**Codeplug:**
- `name`: Merch Mart
- `rx_only`: True

**Zones:**
- Include: Business

**Scan:**
- `all_skip`: True

### `asg_navy_pier`

**Codeplug:**
- `name`: Navy Pier
- `rx_only`: True

**Zones:**
- Include: Business

**Scan:**
- `all_skip`: True

### `asg_oldpo`

**Codeplug:**
- `name`: Old Post Office
- `rx_only`: True

**Zones:**
- Include: Business

**Scan:**
- `all_skip`: True

### `asg_soldier`

**Codeplug:**
- `name`: Soldier Field
- `rx_only`: True

**Zones:**
- Include: Business

**Scan:**
- `all_skip`: True

### `asg_two77`

**Codeplug:**
- `name`: Two Prud FM
- `rx_only`: True

**Zones:**
- Include: Business

**Scan:**
- `all_skip`: True

### `asg_two_pru`

**Codeplug:**
- `name`: Two Prudential
- `rx_only`: True

**Zones:**
- Include: Business

**Scan:**
- `all_skip`: True

### `asg_united`

**Codeplug:**
- `name`: United Center
- `rx_only`: True

**Zones:**
- Include: Business

**Scan:**
- `all_skip`: True

### `asg_wrigley_dmr`

**Codeplug:**
- `name`: Wrigley DMR
- `rx_only`: True

**Zones:**
- Include: Business

**Scan:**
- `all_skip`: True

### `asg_wrigley_fm`

**Codeplug:**
- `name`: Wrigley FM
- `rx_only`: True

**Zones:**
- Include: Business

**Scan:**
- `all_skip`: True

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/venues_chicago.yml
```
