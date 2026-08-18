# Live API health — 2026-08-18

Source: `data/live_api_health_report.json`  
Checked: `2026-08-18T01:30:28Z`  
**37 / 42 ok** (credential-free probes)

## Failures (source-side or optional)

| Channel | Status | Note |
|---------|--------|------|
| `tier82_soilgrids` | 503 | ISRIC temporarily unavailable. Bundled SoilGrids cache remains in `03_FSOT-PublicData` / vendor. |
| `tier84_arxiv_grqc` | timeout | arXiv export flaky. Retry later. |
| `tier87_arxiv_quantph` | 429 | Rate limit. Retry later. |
| `open_chembl` | timeout | ChEMBL slow/unresponsive this run. |
| `open_mast_astroquery` | optional dep | `astroquery` not installed. Health check now **skips** this (same pattern as Materials Project without a key). Public MAST cache stays valid. |

None of these five are prediction kills. Green-gate panels use bundled/cached measured values when a live hop is down.

## GBIF scale check

`count=3,755,207,765` occurrences reachable (was 3,742,920,496 on 2026-08-03). Channel alive.

Re-run: `python scripts/live_api_health_check.py`
