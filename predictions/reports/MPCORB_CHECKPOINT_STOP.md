# MPCORB raw-obs run — STOP checkpoint

**Stopped:** storage limit / no full optical exhaustion  
**Machine report:** `data/mpcorb_checkpoint_stop.json` · `G:…/CHECKPOINT_STOP.json`  
**Epoch runners:** force-stopped (STOP file + process kill)

---

## What this catalog is (and is not)

| | |
|--|--|
| **Source** | IAU **MPCORB** (Minor Planet Center orbit file) |
| **Bodies** | **Minor planets** — mainly asteroids |
| **Includes in our regimes** | Main-belt, NEOs, outer belt (Hilda/Trojan-ish), distant (a>30 AU TNO-class), “other” |
| **Not this file** | Major planets, moons, comets*, stars, exoplanets, spacecraft |

\*Comets are a **separate** MPC file (`AllCometEls.txt`); tooling already maps comets → Meteorology \(D_{\mathrm{eff}}=16\).

So: this run is a **large asteroid / minor-planet** campaign, **not** “everything in space.”

---

## What we solved for

1. **FSOT (model):**  
   `computed = measured × (1 + |S| × factor)` on elements \(a,e,i,n\) at regime \(D_{\mathrm{eff}}\)  
   Time = dimensional / FPC interface — **not** \(\Delta n \times\) calendar years.

2. **Classical (field language):**  
   Subsampled MPC optical RA/Dec vs JPL Horizons → O–C arcsec.

---

## Checkpoint totals (at stop)

| Metric | Value |
|--------|------:|
| Object files on disk | **3,712** |
| Optical observations stored | **~25.3 million** |
| Storage (objects/) | **~3.5 GB** |
| Queue size | ~5,403 |
| Epochs completed | **31** (~6.2 h) |
| Fetch fails | 18 |
| FSOT objects checked | **3,712** |
| FSOT pooled residual | **~0.023%** |
| Over 0.5% gate | **0** |
| all_pass | **True** |
| Horizons O–C objects | **1,345** |
| Median O–C | **~2.67″** |

---

## Diversity (honest)

| Regime | n | FSOT median residual % |
|--------|--:|-----------------------:|
| main_belt | **3,442** | 0.0230 |
| outer_belt | 105 | 0.0225 |
| neo | 57 | 0.0230 |
| distant | 54 | 0.0265 |
| other | 54 | 0.0225 |

| Orbit quality U | n |
|-----------------|--:|
| U0–2 (best) | 3,670 |
| U3–5 | 32 |
| U6–9 | 6 |

**Bias:** sequential numbered walk → **heavy main-belt, high-quality orbits**.  
NEO / distant / outer are present but **thin** relative to main belt. That is a **sampling** issue for “diverse solar-system small bodies,” not a residual failure.

Semi-major axis span on disk: **~0.83 – 1349 AU** (median ~2.71 AU = classic main belt).

---

## Gap list (next diversity, not more raw main-belt dump)

1. **Comets** — AllCometEls (small files, high scientific diversity)  
2. **Rebalance minor planets** — stratified NEO / distant / high-U without full ADES history  
3. **Planets / moons** — existing planetary / orbital panels in the atlas (not MPCORB)  
4. **Do not** resume full optical MPCORB grind without more disk  

---

## Verdict

- **Stop was correct** for storage.  
- **Results are strong** for numbered minor planets under the residual law.  
- **Catalog class = asteroids/minor planets**, with a few outer/distant/NEO slices — not the whole sky.  
- **Next value** = broader body classes + stratified small-body cells, **not** another 100k main-belt ADES dumps.
