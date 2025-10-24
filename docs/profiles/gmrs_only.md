# Profile: gmrs_only

**Description:** GMRS-only build with national simplex plans for quick programming.

## Overview

- **Total Assignments:** 30
- **Services:** gmrs
- **SSRF Files:** 1
- **Policy Files:** 2
- **Organizations:** 0
- **Locations:** 0
- **Contacts:** 0

## Statistics

### By Mode
- **FM:** 30

### By Usage Type
- **Simplex:** 15
- **Repeater:** 8
- **Receive-Only:** 7

### By Frequency Band
- **UHF (400-480 MHz):** 30

## Zones

### Emergency / Calling
*1 channels*

- GMRS 20

### GMRS
*30 channels*

- GMRS 01
- GMRS 02
- GMRS 03
- GMRS 04
- GMRS 05
- GMRS 06
- GMRS 07
- GMRS 08 (RX)
- GMRS 09 (RX)
- GMRS 10 (RX)
- GMRS 11 (RX)
- GMRS 12 (RX)
- GMRS 13 (RX)
- GMRS 14 (RX)
- GMRS 15
- GMRS 16
- GMRS 17
- GMRS 18
- GMRS 19
- GMRS 20
- GMRS 21
- GMRS 22
- GMRS 15 RPT
- GMRS 16 RPT
- GMRS 17 RPT
- GMRS 18 RPT
- GMRS 19 RPT
- GMRS 20 RPT
- GMRS 21 RPT
- GMRS 22 RPT

## Channel Details

### Gmrs Service
*30 channels*

| Channel | RX Freq | TX Freq | Mode | Tone | Usage | TX | Zones | Location |
|---------|---------|---------|------|------|-------|----| ------|----------|
| GMRS 15 | 462.5500 MHz | 462.5500 MHz | FM | None | Simplex | ✓ | GMRS |  |
| GMRS 15 RPT | 462.5500 MHz | 462.5500 MHz | FM | None | Repeater | ✓ | GMRS |  |
| GMRS 01 | 462.5625 MHz | 462.5625 MHz | FM | None | Simplex | ✓ | GMRS |  |
| GMRS 16 | 462.5750 MHz | 462.5750 MHz | FM | None | Simplex | ✓ | GMRS |  |
| GMRS 16 RPT | 462.5750 MHz | 462.5750 MHz | FM | None | Repeater | ✓ | GMRS |  |
| GMRS 02 | 462.5875 MHz | 462.5875 MHz | FM | None | Simplex | ✓ | GMRS |  |
| GMRS 17 | 462.6000 MHz | 462.6000 MHz | FM | None | Simplex | ✓ | GMRS |  |
| GMRS 17 RPT | 462.6000 MHz | 462.6000 MHz | FM | None | Repeater | ✓ | GMRS |  |
| GMRS 03 | 462.6125 MHz | 462.6125 MHz | FM | None | Simplex | ✓ | GMRS |  |
| GMRS 18 | 462.6250 MHz | 462.6250 MHz | FM | None | Simplex | ✓ | GMRS |  |
| GMRS 18 RPT | 462.6250 MHz | 462.6250 MHz | FM | None | Repeater | ✓ | GMRS |  |
| GMRS 04 | 462.6375 MHz | 462.6375 MHz | FM | None | Simplex | ✓ | GMRS |  |
| GMRS 19 | 462.6500 MHz | 462.6500 MHz | FM | None | Simplex | ✓ | GMRS |  |
| GMRS 19 RPT | 462.6500 MHz | 462.6500 MHz | FM | None | Repeater | ✓ | GMRS |  |
| GMRS 05 | 462.6625 MHz | 462.6625 MHz | FM | None | Simplex | ✓ | GMRS |  |
| GMRS 20 | 462.6750 MHz | 462.6750 MHz | FM | None | Simplex | ✓ | GMRS, Emergency / Calling |  |
| GMRS 20 RPT | 462.6750 MHz | 462.6750 MHz | FM | None | Repeater | ✓ | GMRS |  |
| GMRS 06 | 462.6875 MHz | 462.6875 MHz | FM | None | Simplex | ✓ | GMRS |  |
| GMRS 21 | 462.7000 MHz | 462.7000 MHz | FM | None | Simplex | ✓ | GMRS |  |
| GMRS 21 RPT | 462.7000 MHz | 462.7000 MHz | FM | None | Repeater | ✓ | GMRS |  |
| GMRS 07 | 462.7125 MHz | 462.7125 MHz | FM | None | Simplex | ✓ | GMRS |  |
| GMRS 22 | 462.7250 MHz | 462.7250 MHz | FM | None | Simplex | ✓ | GMRS |  |
| GMRS 22 RPT | 462.7250 MHz | 462.7250 MHz | FM | None | Repeater | ✓ | GMRS |  |
| GMRS 08 (RX) | 467.5625 MHz | 467.5625 MHz | FM | None | Receive-Only | RX Only | GMRS |  |
| GMRS 09 (RX) | 467.5875 MHz | 467.5875 MHz | FM | None | Receive-Only | RX Only | GMRS |  |
| GMRS 10 (RX) | 467.6125 MHz | 467.6125 MHz | FM | None | Receive-Only | RX Only | GMRS |  |
| GMRS 11 (RX) | 467.6375 MHz | 467.6375 MHz | FM | None | Receive-Only | RX Only | GMRS |  |
| GMRS 12 (RX) | 467.6625 MHz | 467.6625 MHz | FM | None | Receive-Only | RX Only | GMRS |  |
| GMRS 13 (RX) | 467.6875 MHz | 467.6875 MHz | FM | None | Receive-Only | RX Only | GMRS |  |
| GMRS 14 (RX) | 467.7125 MHz | 467.7125 MHz | FM | None | Receive-Only | RX Only | GMRS |  |

## Authorization Requirements

### gmrs
- **Authority:** FCC
- **Class:** License required
- **Notes:** GMRS simplex permitted on 462 MHz interstitial (Ch 1-7) and main 462 MHz (Ch 15-22). 
467 MHz interstitial (Ch 8-14) are FRS-only simplex; GMRS licensees should not transmit on these frequencies 
except as repeater inputs where authorized. Marked as Rx-only here for GMRS use.


## Source Files

### SSRF Files
- `ssrf/plans/US/gmrs/gmrs_channels.yml`

### Policy Files
- `policies/gmrs_channels.yml`
- `policies/noaa_weather.yml`

## Notes

- This documentation is automatically generated from SSRF-Lite data and policy files
- **OpenGD77 Filtering Applied**: Only FM and DMR modes within 136-174 MHz and 400-480 MHz bands are included
- Unsupported modes (D-STAR, C4FM, APRS, etc.) and out-of-band frequencies are excluded
- TX enablement depends on profile settings and `--tx-service` flags used during generation
- Frequencies, tones, and other technical details should be verified before use
- Geographic coordinates are approximate and for reference only
