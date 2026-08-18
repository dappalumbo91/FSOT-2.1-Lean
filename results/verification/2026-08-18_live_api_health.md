# Live API health — 2026-08-18

Source: `data/live_api_health_report.json`  
Checked: `2026-08-18T01:30:28Z` · MAST re-verified after install  
**38 / 42 ok** (credential-free probes)

## MAST — installed and live

| Item | Value |
|------|-------|
| Packages | `astroquery 0.4.11`, `astropy 8.0.1` (required in `requirements.txt`) |
| Query | public HST images of M1 (Crab), no login |
| Result | **1588** rows · 5 metadata records ingested |
| Artifacts | `data/mast_astroquery_ingest_report.json` · `vendor/open_science/mast_astroquery/live.json` |

Health channel `open_mast_astroquery` is **ok**. Missing package is a fail, not a skip.

## Remaining failures (source-side, not missing software)

| Channel | Status | Note |
|---------|--------|------|
| `tier82_soilgrids` | 503 | ISRIC temporarily unavailable. Bundled SoilGrids cache remains. |
| `tier84_arxiv_grqc` | timeout | arXiv export flaky. Retry later. |
| `tier87_arxiv_quantph` | 429 | Rate limit. Retry later. |
| `open_chembl` | timeout | ChEMBL slow/unresponsive this run. |

None of these four are prediction kills. Green-gate panels use bundled/cached measured values when a live hop is down.

## GBIF scale check

`count=3,755,207,765` occurrences reachable (was 3,742,920,496 on 2026-08-03). Channel alive.

Re-run: `python scripts/live_api_health_check.py`
