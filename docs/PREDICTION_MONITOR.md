# Prediction monitor system

**Human / X explainers (start here):** [`predictions/EXPLAINED.md`](../predictions/EXPLAINED.md) · [`predictions/public/X_READY.md`](../predictions/public/X_READY.md) · [`predictions/public/ONE_PAGER.md`](../predictions/public/ONE_PAGER.md)

**Goal:** FSOT covers hundreds of domains; only a subset had **falsifiable near-term predictions**. This system expands locks for **public data drops that are imminent or rolling**, and re-checks them on a schedule without retuning the engine.

| Artifact | Role |
|----------|------|
| `predictions/preregistered_predictions_manifest.yaml` | Hand PRED-001… curated locks |
| `predictions/domain_prediction_atlas.json` | **Atlas-scale** PREDs for every green domain |
| `predictions/h0_multi_tool_predictions.json` | **Per-tool H₀** under BH→WH bubble bleed |
| `predictions/h0_sightline_predictions.json` | **Per-host / sky-sector H₀** (SH0ES sightlines) |
| `predictions/sector_h0_seed.json` | H₀ tool seed + density proxies |
| `predictions/prediction_monitor_registry.yaml` | Watches ↔ facilities ↔ windows ↔ kill criteria |
| `predictions/toe_prereg_freeze.json` | T5 SHA-locked slate |
| `scripts/run_prediction_monitor.py` | Offline/online status runner |
| `predictions/prediction_monitor_report.json` | Machine report |
| `predictions/reports/PREDICTION_MONITOR.md` | Human table |
| `results/` | **Outcomes after data lands** (literature packs + jsonl). Predictions stay frozen. |
| `kaggle/fsot-prediction-monitor/` | Portable dataset + notebook |

### Multi-tool H₀ (not one number)

FSOT does **not** claim a single H₀ for every instrument. Under the BH→WH bubble-bleed
picture, Cepheid ladders, TRGB, CMB, BAO, masers, time-delay lenses, etc. couple to
**different information-flow sectors**. Each tool has its own preregistered prediction:

`H0_tool = H0_global_fsot × (1 + density_model × bleed_fraction)`

See `predictions/reports/H0_MULTI_TOOL_PREDICTIONS.md` and per-host
`predictions/reports/H0_SIGHTLINE_PREDICTIONS.md`.

### Not cosmology-only

The domain atlas tags every green panel into scientific sectors (bio_med,
materials_chem, particle_nuclear, earth_climate, social_econ, engineering_compute,
astro_gw, …) with residual holds, scalar locks, and **sector portfolio** predictions.
Cosmology is one sector among many — see `predictions/reports/DOMAIN_PREDICTION_ATLAS.md`.

Authority pin: **D1D38A** · zero free parameters · see [`PREDATA_RISK.md`](PREDATA_RISK.md).

---

## Near/future data drops (research snapshot · 2026-08)

| Facility | Drop | Window | FSOT lock class |
|----------|------|--------|-----------------|
| **Euclid** | DR1-Foundation; DR1 complete (WL / S8 / clustering) | Nov 2026; mid-2027 | S8 0.805 · wₐ −1.018 |
| **Rubin LSST** | Survey live; EDP2 phase-2; early science pathfinders | Oct–Dec 2026 onward | S8 / structure pathfinder |
| **DESI** | Public BAO / cosmology; extension | Ongoing 2026–27 | H₀ bridge 70.75 · wₐ |
| **JWST / SH0ES-class** | Local ladder H₀ papers | Rolling | H₀ bridge |
| **LVK / GWOSC** | GWTC-5.0 out; more O4 ~Dec 2026; O5 ~late 2026 | 2026 | Compact-binary panel ≤0.5% |
| **SO / ACT / SPT** | N_eff (CMB-S4 not continued) | 2026–28 | N_eff 3.046 |
| **PDG** | Higgs mass | Annual | m_H 125.25 GeV |
| **CHIME/FRB** | DM catalogs | Rolling | DM excess class 200 |
| **NCEI / open bio** | Continuous | Continuous | Panel residual ceilings |

Sources are public project timelines (ESA Euclid, Rubin Observatory, GWOSC, DESI data portal). Dates are **tentative** — the monitor records status; it does not invent release dates.

---

## Commands

```powershell
# Rebuild multi-tool H0 + per-host sightlines + full multi-sector atlas:
python scripts/build_h0_multi_tool_predictions.py
python scripts/build_h0_sightline_predictions.py
python scripts/build_domain_prediction_atlas.py
python scripts/run_prediction_monitor.py              # offline, uses repo panels
python scripts/run_prediction_monitor.py --online     # + GWOSC / URL probes

# Kaggle portable pack (no upload):
python scripts/build_kaggle_prediction_pack.py

# Upload (CLI already authenticated as damianpalumbo):
python scripts/build_kaggle_prediction_pack.py --push
```

### Schedule

| Cadence | Command |
|---------|---------|
| Weekly | `python scripts/run_prediction_monitor.py` |
| Fortnightly | `python scripts/run_prediction_monitor.py --online` |
| After freeze change | re-run monitor + Kaggle pack |

Windows Task Scheduler / cron example:

```text
# every Sunday 06:00 local
python C:\Users\damia\Desktop\FSOT-2.1-Lean\scripts\run_prediction_monitor.py
```

Or use the Grok/session scheduler to fire the same prompt weekly.

---

## Kaggle path

**Yes — this is supported.** Your CLI is authenticated (`damianpalumbo`) and you already host FSOT datasets/kernels.

1. **Dataset** `damianpalumbo/fsot-prediction-monitor`  
   - `fsot_compute.py` (full seed engine)  
   - prereg YAML, freeze JSON, monitor registry + report  
   - slim margin summary (not all 472 heavy benchmarks — full atlas stays on GitHub)

2. **Notebook** same slug  
   - Validates pin D1D38A  
   - Lists PREDs + high-urgency watches  
   - Optional live GWOSC count  

3. **What Kaggle is good for**  
   - Public reproduction of prediction locks  
   - Lightweight engine demos  
   - Attaching open datasets for domain notebooks  

4. **What stays on GitHub**  
   - Full multiprover (Lean/Coq/Isabelle/…)  
   - 472-domain green atlas  
   - Reality OS kernel  

Dumping *everything* to Kaggle is possible but heavy (GBs of benchmarks). Prefer: **engine + predictions + slim evidence** on Kaggle; link monorepo for the rest. Existing biohub competition bundles show the pattern (`vendor/kaggle_biohub_review/`).

---

## Adding a new prediction

1. Append PRED-NNN to `preregistered_predictions_manifest.yaml` with `future_survey` and kill discriminant.  
2. Add a `watches:` row in `prediction_monitor_registry.yaml`.  
3. Run `freeze_prereg` if it belongs on the T5 slate.  
4. `python scripts/run_prediction_monitor.py`  
5. Optional: rebuild/push Kaggle pack.  

**Never** edit `fsot_predicted` in place after registration — new freeze_id only.
