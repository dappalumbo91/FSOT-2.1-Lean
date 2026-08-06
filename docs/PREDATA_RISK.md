# Pre-data risk discipline (Label B · T5)

**Purpose:** Make FSOT’s contested-sector predictions **risky before the data land**, not curve-fits after.

**Authority:** pin **D1D38A** · zero free parameters · `docs/TOE_CLAIM_BOUNDARIES.md` T5  
**Frozen artifact:** `data/toe_prereg_freeze.json` (SHA-256 bundle)  
**Prereg manifest:** `data/preregistered_predictions_manifest.yaml` (PRED-001–041+)  
**Future ledger:** `data/contested_future_observation_ledger.json`

---

## What “pre-data risk” means here

1. **Freeze first.** Sector centrals and kill criteria are written to `toe_prereg_freeze.json` with a dated `freeze_id` and `bundle_sha256` **before** decisive survey releases are used as gates.
2. **No silent retune.** Changing an `fsot_predicted` value requires a **new** `freeze_id`. The old hash remains in git history as the risk record.
3. **Kill criteria are executable.** A failed kill is a ledger event (falsification registry), not a narrative rescue.
4. **Contested ≠ pipeline failure.** H₀ tension, S₈, wₐ, N_eff, cusp-core, BBN lithium, FRB DM excess remain **open science problems** with FSOT seed readouts; see contested closure.

---

## T5 checklist

| Check | Artifact |
|-------|----------|
| Freeze file exists with `bundle_sha256` | `data/toe_prereg_freeze.json` |
| ≥2 supporting files hashed | prereg manifest, holdouts, falsification, contested |
| Sector PREDs include future-survey tags | `sector_predictions[].future_survey` |
| Review horizon set | `review_horizon` (currently through mid-2027 class) |
| Global kill registered | `global_kill` string + T6 registry |

Regenerate freeze (does not retune engine):

```powershell
python -c "import sys; sys.path.insert(0,'scripts'); from build_toe_gap_closure import freeze_prereg; r=freeze_prereg(); print(r['freeze_id'], r['bundle_sha256'][:16])"
# or full Label A/B recompute:
python scripts/build_toe_gap_closure.py
```

---

## Risk classes

| Class | Meaning | Example PREDs |
|-------|---------|----------------|
| **Bridge** | Must sit between rival anchors | PRED-H0-bridge, PRED-S8 |
| **Central** | Frozen central within 0.5% of next release | PRED-mH, PRED-sigma8-central, PRED-Omega-Lambda |
| **Sign / evolution** | Discriminates LCDM default | PRED-wa, PRED-DarkEnergy-CPL-wa-sign |
| **Anomaly map** | Maps known hard problems without free ε | PRED-lithium-factor, PRED-cusp-core-rc, PRED-FRB-DM-excess |
| **Panel hold** | Worst-green empirical watch ≤0.5% | PRED-Zebrafish-panel-hold |

---

## What does **not** count as pre-data risk

- Adding more green domains after the fact without freeze rows  
- Tightening residuals by introducing free color / free ε  
- Citing “someone agreed” without a clean-clone command path  
- Renaming a failed kill as “effective theory” without a new freeze_id  

---

## Independent reader path

1. Open `data/toe_prereg_freeze.json` — note `freeze_id` and `bundle_sha256`.  
2. Confirm pin D1D38A via `python scripts/build_repo_status_snapshot.py`.  
3. Re-hash listed `files[]` and verify they match.  
4. After a survey release: evaluate each `kill` string; register outcome in falsification registry — **do not** edit the frozen predicted centrals.

See also: [`TOE_GAP_CLOSURE.md`](TOE_GAP_CLOSURE.md) · [`SKEPTIC_REPLICATION_KIT.md`](SKEPTIC_REPLICATION_KIT.md) · [`INDEPENDENT_REPRODUCTION.md`](INDEPENDENT_REPRODUCTION.md)
