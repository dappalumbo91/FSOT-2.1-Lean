# Object scoring — do not kill the wrong row

**As-of:** 2026-09-07 · freeze `TOE-PREREG-20260806` · pin **D1D38A**

Do **not** retune `fsot_predicted`. Do **not** rewrite Family B `vendor/fsot_compute.py`.
A literature number is a **named object**. Scoring the wrong object is a false kill.

## 1. H₀ — five objects, not one sky

JWST Perfect Host **73.49 ± 0.93** (doi:10.3847/2041-8213/ae0ad6 · arXiv:2509.01667)
is a **local Cepheid ladder** readout. It is **not** PRED-001.

| Object | Lock | Fair compare | Not |
|--------|------|--------------|-----|
| **Bridge** PRED-001 | **70.75** | CCHP TRGB ~70.39 · dual-anchor PRED-024 **72.1** · sits *between* Planck 67.4 and SH0ES ~73 | JWST Perfect Host 73.49 as “the” H₀ |
| **Dual-anchor** PRED-024 | **72.1** | local-ladder *sector*, not the bridge | Planck-only or SH0ES-only as the bridge kill |
| **Global** | **68.440** | Cosmology wave-1 background | any local-ladder paper |
| **Planck-class** | **67.4** | CMB tool row (`planck_cmb_local` 67.384, 0.024%) | SH0ES 73.04 |
| **Local ladder / SH0ES-class** | class bin **73.773** (2.5% band) · chain **72.856 vs 73.04 (0.252%)** | Perfect Host 73.49 · SH0ES 73.04 · sightline hosts (M101 73.497 is a *host*, not the sky) | PRED-001 70.75 |

**One line:** Perfect Host 73.49 is PRED-001 tension **only if mis-scored as the bridge**; the correct compares are CCHP TRGB / dual-anchor rows (and the local-ladder class row, 2.5% band).

Monitor: `WATCH-Local-H0-JWST` scores local-ladder papers against PRED-024 / PRED-051, **not** PRED-001.

## 2. S₈ — DES-alone vs joint

PRED-002 / PRED-042 lock **0.805** (`between_planck_and_des`). Euclid DR1 (~12 Nov 2026) is still the independent drop.

| Object | Number | Role |
|--------|-------:|------|
| DES Y6 **alone** | 0.789 ± 0.012 | **Tension row** (~2.6σ vs CMB). Not the PRED-002 kill. |
| Joint DES+CMB+low-z | **0.806** | **Fair compare** to 0.805 (arXiv:2601.14559 primary; review arXiv:2602.12238) |
| Euclid CLOE.3 FoM(w₀,wₐ)>400 | synthetic | **Not measured.** Do not cite as support. |

Quoting DES-alone as the kill is the wrong object.

## 3. wₐ — direction, not a 3σ lock

PRED-043 frozen central **−1.018**. Kill remains `desi_or_euclid_3sigma_exclusion` of that *frozen* central — not “we already won 3σ.”

DESI DR2 prefers wₐ<0 / evolving DE (~3.1σ DESI+CMB over ΛCDM in some combinations); SN sample **moves** the significance (doi:10.1103/PhysRevD.112.083515 · arXiv:2503.14738).

**Status: adjacent / hold-not-kill.** Direction supports. Central stays **−1.018** until Euclid/DESI **joint** names the same object. Do not claim 3σ on −1.018.

## 4. Euclid — forecast only

PRED-002 / PRED-042 / PRED-043 stay **awaiting** Euclid DR1-Foundation **~12 Nov 2026**.
CLOE.3 is a synthetic figure of merit (doi:10.1051/0004-6361/202556861). Zero survey-level S₈ / H₀ / wₐ for Tier A.

## Genetics Å objects

See [`GENETICS_CLAIM_EVIDENCE.md`](GENETICS_CLAIM_EVIDENCE.md) — product **0.13 Å** ≠ AF **~0.47 Å** ≠ cryo-EM FSC **~1.2 Å** ≠ bulk **~13 Å**. Do not cross-cite.

## 5. Standing compare (living)

The table above is the rule. The living scoreboard is

[`OBJECT_COMPARE.md`](OBJECT_COMPARE.md) · [`../results/object_compare.json`](../results/object_compare.json)

Refresh: `python scripts/build_object_compare.py`

Append a paper without touching `predictions/`:

```powershell
python scripts/record_prediction_outcome.py --pred-id PRED-001 --survey "Paper-label" --result hold --measured 70.39 --unit km/s/Mpc --source https://arxiv.org/abs/... --notes "one sentence"
```

Related: [`SH0ES_LADDER_DIAGNOSIS.md`](SH0ES_LADDER_DIAGNOSIS.md) · [`../predictions/reports/H0_MULTI_TOOL_PREDICTIONS.md`](../predictions/reports/H0_MULTI_TOOL_PREDICTIONS.md) · [`PREDATA_RISK.md`](PREDATA_RISK.md) · [`ISOLATED_RESIDUALS.md`](ISOLATED_RESIDUALS.md)
