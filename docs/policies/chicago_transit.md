# chicago_transit

**File:** `chicago_transit.yml`  
**Path:** `policies/chicago_transit.yml`  

## Overview

- **Assignment Overrides:** 7
- **Zone Definitions:** 1
- **Custom Names:** 7
- **RX-Only Assignments:** 7
- **TX-Enabled Assignments:** 0
- **Scan-Enabled Assignments:** 0

### Configuration Types

- **Codeplug:** Channel names, RX/TX settings
- **Zones:** Zone membership and exclusions
- **Scan:** Skip settings and scan behavior

## Zone Organization

| Zone | Assignments |
|------|-------------|
| Transit & Transport | 7 |

## Custom Channel Names

| Assignment ID | Custom Name |
|---------------|-------------|
| `asg_cta1` | CTA Ops A |
| `asg_cta2` | CTA Ops B |
| `asg_cta_yard` | CTA Yard |
| `asg_deliv_fm1` | Delivery FM |
| `asg_deliv_u1` | Delivery DMR |
| `asg_midway_ops` | MDW Ops |
| `asg_ord_ops` | ORD Ops |

## TX/RX Configuration

### RX-Only Assignments

- `asg_cta1`
- `asg_cta2`
- `asg_cta_yard`
- `asg_deliv_fm1`
- `asg_deliv_u1`
- `asg_midway_ops`
- `asg_ord_ops`

## Scan Configuration

### Scan-Disabled Assignments

- `asg_cta1`
- `asg_cta2`
- `asg_cta_yard`
- `asg_deliv_fm1`
- `asg_deliv_u1`
- `asg_midway_ops`
- `asg_ord_ops`

## Assignment Details

### `asg_cta1`

**Codeplug:**
- `name`: CTA Ops A
- `rx_only`: True

**Zones:**
- Include: Transit & Transport

**Scan:**
- `all_skip`: True

### `asg_cta2`

**Codeplug:**
- `name`: CTA Ops B
- `rx_only`: True

**Zones:**
- Include: Transit & Transport

**Scan:**
- `all_skip`: True

### `asg_cta_yard`

**Codeplug:**
- `name`: CTA Yard
- `rx_only`: True

**Zones:**
- Include: Transit & Transport

**Scan:**
- `all_skip`: True

### `asg_deliv_fm1`

**Codeplug:**
- `name`: Delivery FM
- `rx_only`: True

**Zones:**
- Include: Transit & Transport

**Scan:**
- `all_skip`: True

### `asg_deliv_u1`

**Codeplug:**
- `name`: Delivery DMR
- `rx_only`: True

**Zones:**
- Include: Transit & Transport

**Scan:**
- `all_skip`: True

### `asg_midway_ops`

**Codeplug:**
- `name`: MDW Ops
- `rx_only`: True

**Zones:**
- Include: Transit & Transport

**Scan:**
- `all_skip`: True

### `asg_ord_ops`

**Codeplug:**
- `name`: ORD Ops
- `rx_only`: True

**Zones:**
- Include: Transit & Transport

**Scan:**
- `all_skip`: True

## Usage

This policy can be used in profiles to override assignment behavior:

```yaml
profile:
  policy:
    files:
      - policies/chicago_transit.yml
```
