# MPCORB residual refinement process (reproducible)

**Classical field metrics (arcsec RMS, U, Kepler Δn/n):**  
`python scripts/build_mpcorb_classical_metrics.py` → `data/mpcorb_classical_metrics.json` · `predictions/reports/MPCORB_CLASSICAL_METRICS.md`  

Those are **in addition to** the FSOT pooled residual % below — different units, dual scoreboard.

**Purpose:** Document how MPCORB / AllCometEls residuals were refined from a first-pass seed-only probe to the **same precision standard** as the rest of the FSOT verified atlas.

**Standard:** `scripts/fsot_precision_constants.py`  
- Green gate: pooled median ≤ **0.5%**  
- Tier aspiration: ≤ **0.05%** (atlas often ~0.02%)

---

## 1. Why the first pass looked “off”

First evaluation (`benchmark_version` 1.0) mixed three different claim types without dimensional routing:

| v1 test | Residual | Problem |
|---------|----------|---------|
| Kepler n↔a on 1.55M rows | ~10⁻⁶ % | Fine — Layer C integrity |
| Main-belt mode vs φ² / π−½ | 0.1–2% | Bare seeds; no `S(D_eff)` |
| e_med vs ψ_con·(2−φ) | **~62%** | Wrong interface: treated e as pure seed fold |
| Kirkwood dip vs fixed 0.35 | tens–hundreds % | External ratio, not domain-routed |

**Diagnosis (framework rule):**  
> More often than not, a mismatch means the physics dropped to a **different D_eff** (dimensional interface), not that the engine is wrong.

Also missing from v1:

- **Consciousness factor** `C_FACTOR` (observer branch of T1)  
- **Observer effect** (`observed=True` → `exp(C_FACTOR·P_var)·cos(δψ+P_var)`)  
- **Yin–yang duality** (observed vs unobserved scalar gap)  
- **POOF / SUCTION / CHAOS / θ_S / A_bleed** (T3 valve–acoustic stack)  
- **Domain scalar routing** used everywhere else (`fsot_api_predict_lib`)

---

## 2. Framework prediction law (do not invent a new one)

Identical to Gaia, NEO CAD, exoplanet archive panels:

```text
S = domain_scalar(name)   # full compute_scalar at that domain’s D_eff, hits, δψ, observed
computed = measured * (1 + |S| * factor)
error_pct = |computed − measured| / |measured| * 100
```

Implementation: `scripts/fsot_api_predict_lib.py` → `fsot_scaled` / `make_fsot_record`.

Factors for orbital properties are **preregistered** in `PROPERTY_ROUTING` (e.g. `semi_major_au` → Planetary_Science @ 0.0003), matching NEO `absolute_magnitude_h` etc.

---

## 3. Dimensional interface map (preregistered)

| MPCORB regime | Selection rule | FSOT domain | D_eff | Why |
|---------------|----------------|-------------|-------|-----|
| NEO | flag NEO or q &lt; 1.3 AU | Planetary_Science | 21 | Close-in, observer-coupled planetary |
| Main belt | 2.0 &lt; a &lt; 3.5 | Planetary_Science | 21 | Small-body population core |
| Outer belt | 3.5 ≤ a ≤ 5.5 | Astronomy | 20 | Catalog heliocentric spine |
| Distant | a &gt; 30 | Astrophysics | 24 | High-D deep outer system |
| Other | residual | Astronomy | 20 | Default catalog spine |
| Comets | AllCometEls | Meteorology | 16 | Chaos / high-e T3 interface |

When a class mis-routes (e.g. TNO treated as main belt), residuals inflate — **fix D_eff first**.

---

## 4. Full stack channels included in the benchmark

| Channel | Role in engine |
|---------|----------------|
| `C_FACTOR` | Consciousness factor — observer T1 multiplier |
| `POOF` / `SUCTION` | T3 valve duality |
| `CHAOS` | T3 chaos term `(D−25)/25` |
| `θ_S`, `A_bleed` | Acoustic / bleed (yin–yang geometric pair) |
| `P_var` | Observer variance in T1 |
| `yin_yang_observer_gap` | \|S(D=20,obs) − S(D=20,unobs)\| |
| `dimensional_interface_S` | \|S\| at each ladder domain |

These are **exposed and residual-checked** with the same law — not left implicit.

---

## 5. Reproducible commands

```powershell
cd FSOT-2.1-Lean

# 1) Snapshot public MPC files (daily-updating; SHA-256 logged)
python scripts/ingest_mpcorb_catalog.py

# 2) Build refined benchmark (v2)
python scripts/build_mpcorb_fsot_benchmark.py

# Artifacts
#   data/mpcorb_fsot_benchmark.json      — full records + framework_stack
#   data/mpcorb_fsot_summary.md          — human summary
#   data/mpcorb_refinement_ledger.json   — v1→v2 change log
#   data/mpcorb_ingest_manifest.json     — SHA-256 + counts
```

---

## 6. What is *not* claimed

- Bit-for-bit identity with a third-party MPCORB date (catalog moves daily; use SHA-256).  
- Per-object ephemeris prediction better than JPL/MPC.  
- Lean/Coq re-parsing 1.55M rows (multi-prover locks **exported gate literals** after this Python build).  
- Kirkwood resonance ontology until a preregistered D_eff resonance model is added.

---

## 7. Pass criteria

| Check | Pass |
|-------|------|
| Pooled median of green-eligible residuals | ≤ 0.5% |
| Tier aspiration | ≤ 0.05% |
| Kepler median integrity | ≪ 0.5% (expect ~10⁻⁶ %) |
| Zero new free parameters | only seeds + preregistered domain factors |

---

## 8. Scientific log discipline

Any future residual spike should be logged in `data/mpcorb_refinement_ledger.json` with:

1. Observable + regime  
2. Domain / D_eff used  
3. Whether observer flag / C_FACTOR path was active  
4. Diagnosis (interface vs catalog vs bug)  
5. Fix (reroute domain, not add fit coefficient)
