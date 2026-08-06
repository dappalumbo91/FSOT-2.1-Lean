# Nearest data drops (monitor priority)

*As of 2026-08-06 · generated 2026-08-06T13:22:56.628181+00:00*

## Closest hard calendar event

**Euclid DR1-Foundation (raw/calibrated ~1900 deg²)**  
ID: `EUCLID-DR1-FOUNDATION` · window start **2026-11-12** · **98 days** from as-of date  
Linked PREDs: `PRED-042`, `PRED-043`, `PRED-002`, `PRED-wa`  

Hard date on ESA timeline (12 Nov 2026). Foundation is imaging/catalogs; full weak-lensing cosmology products follow mid-2027. Still the cleanest named calendar event for FSOT cosmology locks.

## Policy (WIP model — do not freeze development)

True

Git commit timestamps on GitHub are the preregistration clock for any prediction already pushed. New work can continue on main; when a survey drops, log outcome against the commit SHA that contained the prediction — do not retune that SHA's predicted values.

Recommended: keep predictions *in* the monorepo for pin/engine integrity; optionally add a thin public mirror repo that only tracks prediction JSON + outcomes. Full multiprover stays here.

## Full ranking

| Rank | Drop | Window start | Days | Certainty | Status |
|-----:|------|--------------|-----:|-----------|--------|
| 1 | Euclid DR1-Foundation (raw/calibrated ~1900 deg²) | 2026-11-12 | 98 | announced_date | upcoming |
| 2 | Rubin LSST Early DP2 complete (visit/diff images) | 2026-10-01 | 56 | target_window | upcoming |
| 3 | LVK remaining O4 open data / catalog updates | 2026-12-01 | 117 | expected_window | upcoming |
| 4 | LVK O5 observing run start | 2026-08-15 | 9 | envisioned | upcoming |
| 5 | Euclid DR1 complete (WL / clustering science products) | 2027-06-01 | 299 | mid_year_target | upcoming |
| 6 | CHIME/FRB catalog updates | 2026-08-06 | 0 | continuous | open_now |
| 7 | DESI public BAO / cosmology catalog refreshes | 2026-08-06 | 0 | continuous | open_now |
| 8 | JWST / CCHP / SH0ES local ladder papers | 2026-08-06 | 0 | continuous | open_now |
| 9 | Open bio/earth/materials panel refreshes (GBIF, NCEI, PubChem…) | 2026-08-06 | 0 | continuous | open_now |

Refresh: `python scripts/rank_nearest_data_drops.py`
