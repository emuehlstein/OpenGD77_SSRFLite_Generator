# SSRF-Lite YAML Specification  
*A pragmatic spectrum data model for codeplug generation*  

Version: **0.3.2**  
Last updated: 2025-09-17  

---

## 1. Purpose
SSRF-Lite is a trimmed-down profile of the [Standard Spectrum Resource Format (SSRF)](https://www.ntia.gov/publications/2023/standard-spectrum-resource-format-ssrf) designed for:  

- Representing radio channels, repeaters, and channel plans in **YAML**.  
- Driving automated codeplug generators ex. OpenGD77, qdmr, OpenRTX, & OEM imports.
- Remaining close enough to SSRF that future expansion or exchange is straightforward.  

---

## 2. Entities

### 2.1 Organization
Represents an owning or operating body.  
```yaml
organizations:
  - id: org_ns9rc
    name: "North Shore Radio Club"
```

Fields:  
- `id` (string, unique)  
- `name` (string)  

---

### 2.2 Location
Geographic site.  
```yaml
locations:
  - id: loc_chicago_lsd
    name: "Chicago – North Lake Shore Dr"
    lat: 41.9804506
    lon: -87.6546484
```
Fields:  
- `id`, `name`  
- `lat`, `lon` (decimal degrees)  

> **Note:** See Antenna for height fields (AGL/AMSL).

---

### 2.3 Station
Logical station at a location, often tied to an organization.  
```yaml
stations:
  - id: stn_ns9rc_440
    call_sign: "NS9RC"
    organization_id: org_ns9rc
    location_id: loc_chicago_lsd
    service: "amateur"
```

Fields:  
- `id`, `call_sign`  
- `organization_id` (ref → Organization)  
- `location_id` (ref → Location)  
- `service` (e.g. `"amateur"`, `"gmrs"`, `"marine"`)  

---

### 2.4 Antenna
Basic antenna info with explicit height references.  
```yaml
antennas:
  - id: ant_ns9rc_440
    station_id: stn_ns9rc_440
    name: "Offset Pattern Antenna"
    gain_dbi: null
    height_agl_m: 156.4       # 513 feet ≈ 156.4 m
    height_amsl_m: null
```
Fields:  
- `id`, `station_id`, `name`  
- `gain_dbi` (optional)  
- `height_agl_m` (optional, meters AGL)  
- `height_amsl_m` (optional, meters AMSL)  

> Populate whichever height(s) you know. If both are present, they need not be mathematically linked (site elevation is not modeled in SSRF-Lite).

---

### 2.5 RF Chain
Bundled **Transmitter + Receiver + Mode**.  
```yaml
rf_chains:
  - id: chain_ns9rc_440_fm
    station_id: stn_ns9rc_440
    antenna_id: ant_ns9rc_440
    tx:
      freq_mhz: 447.725       # uplink (ERP, repeater output +5 MHz)
      power_w: 80             # ERP approx
      emission: "16K0F3E"     # FM voice, wideband (25 kHz)
      bandwidth_khz: 25
    rx:
      freq_mhz: 442.725       # repeater input
    mode:
      type: "FM"
      ctcss_tx_hz: 114.8
      ctcss_rx_hz: 114.8
```
Fields:  
- `id`, `station_id`, `antenna_id`  
- `tx`: `freq_mhz`, `power_w?`, `emission`, `bandwidth_khz?`  
- `rx`: `freq_mhz`, `sensitivity_dbm?`  
- `mode`:  
  - `type` (`"FM"`, `"DMR"`, etc.)  
  - Mode-specific fields (`ctcss_*`, `color_code`, `timeslots`, `talkgroups`)  

---

### 2.6 Channel Plan
Reusable collections (NOAA, Marine, GMRS interstitials).  
```yaml
channel_plans:
  - id: chplan_noaa
    name: "NOAA WX"
    channels:
      - name: "WX1"
        freq_mhz: 162.550
      - name: "WX2"
        freq_mhz: 162.400
```

---

### 2.7 Authorization
License or permission required.  
```yaml
authorizations:
  - id: auth_fcc_amateur_t
    authority: "FCC"
    service: "Amateur Radio"
    class: "Technician or higher"
    identifier: null
    notes: "TX requires US amateur license."
  - id: auth_rx_only_public
    authority: "N/A"
    service: "Receive-only"
    class: null
    identifier: null
    notes: "Listening only (e.g., NOAA); no license required."
```

Fields:  
- `id`  
- `authority` (e.g. `"FCC"`)  
- `service` (Amateur, GMRS, Marine, etc.)  
- `class` (optional, license class)  
- `identifier` (e.g. license number)  
- `notes`  

---

### 2.8 Contacts
Directory for DMR talkgroups or similar.  
```yaml
contacts:
  - id: tg_310
    name: "TAC-310"
    kind: "Group"
```

---

### 2.9 Assignment
The “workhorse” — links RF chain or channel plan to an operational use (codeplug row).  
```yaml
assignments:
  - id: asgn_ns9rc_440
    rf_chain_id: chain_ns9rc_440_fm
    usage: "repeater"
    zones: ["Ham-Repeaters"]
    codeplug:
      name: "NS9RC 440"
      rx_only: false
    authorization_id: auth_fcc_amateur_t
    comment: |
      Motorola + S-Com 7330 controller, ~80 W ERP.
      Offset pattern antenna at 513 ft (156 m).
      Coverage: Cook & Lake Counties; one of the most active repeaters in Chicago.
      Mobile access: S to Merrillville IN, N to Kenosha WI, W to Crystal Lake.

  - id: asgn_noaa_wx1
    channel_plan_id: chplan_noaa
    channel_name: "WX1"
    usage: "receive-only"
    zones: ["NOAA"]
    codeplug:
      name: "WX1-Chicago"
      rx_only: true
    authorization_id: auth_rx_only_public
```

---

## 3. Mapping to SSRF

| SSRF Entity | SSRF-Lite Equivalent | Notes |
|---|---|---|
| Organization | `organizations[]` | same name, pared fields |
| Location | `locations[]` | same (no site elevation) |
| Station | `stations[]` | same |
| Antenna | `antennas[]` | same, + `height_agl_m` / `height_amsl_m` |
| Equipment / Tx / Rx / TxMode / RxMode | `rf_chains[]` | consolidated |
| ChannelPlan / ChannelFreq | `channel_plans[]` | same |
| Authorization | `authorizations[]` | same |
| Assignment | `assignments[]` | same, plus codeplug extras |
| Contacts (not in SSRF) | `contacts[]` | **added** for DMR convenience |
| Codeplug / Zones | `assignments[].codeplug`, `zones` | **added** for generator use |

---

## 4. Example Summary
This spec now demonstrates:  
- **Analog FM repeater**: NS9RC 440 MHz with ERP, offset, tones, and coverage notes.  
- **Receive-only channel plan**: NOAA WX frequencies.  
- **Authorization linkage**: Amateur TX license vs. public RX-only.  
- **Extensibility**: Ready to add DMR or other modes.  

---

## 5. Design Principles

- **Stay SSRF-shaped**: reuse names and relationships where possible.  
- **Trim fat**: omit coordination, workflows, and technical minutiae not needed for codeplugs.  
- **Add only what’s practical**: `zones`, `codeplug`, `contacts`.  
- **Interoperable**: keep ITU emission designators, MHz/kHz/Hz units consistent.  
- **Extensible**: can grow into full SSRF without breaking the schema.  
