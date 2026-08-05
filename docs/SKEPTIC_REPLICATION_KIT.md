# FSOT Skeptic Replication Kit

*15-minute verification path · 2026-08-05 · commit `7f75df97ec38`*

Run this if you want to **break FSOT fast** — not read 12,000 lines of narrative first.

**Live authority:** pin **D1D38A** (match=True) · green **432/432** · multiprover overall_ok=True  
Full human guide: [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) · audience map: [`DOCUMENTATION_MAP.md`](DOCUMENTATION_MAP.md) · math: [`FSOT_MATH_KEY.md`](FSOT_MATH_KEY.md)

Plain-language ladder: [`CLEAR_PATH_FOR_INDEPENDENTS.md`](CLEAR_PATH_FOR_INDEPENDENTS.md) ·  
Claim tiers: [`RESIDUAL_HONESTY_AND_CLAIM_TIERS.md`](RESIDUAL_HONESTY_AND_CLAIM_TIERS.md) ·  
Status snapshot: [`CURRENT_STATUS.md`](CURRENT_STATUS.md)

## Step 1 — Clone and install (~2 min)

```bash
git clone https://github.com/dappalumbo91/FSOT-2.1-Lean.git
cd FSOT-2.1-Lean
pip install -r requirements.txt
```

## Step 2 — Status + green gate (~3–10 min)

```bash
python scripts/build_repo_status_snapshot.py
python scripts/audit_all_benchmark_margins.py
python scripts/audit_parameter_count.py
```

**Expect (at generation of this kit):**

| Check | Expected |
|-------|----------|
| Pin | **D1D38A** with `pin_match: true` in `docs/CURRENT_STATUS.md` |
| Benchmark green | **432/432** fail 0 (`data/benchmark_margin_audit.json`) |
| Gate | pooled median ≤ **0.5%** |
| Parameter audit | **ZERO_FREE** |
| Label A / B (if toe report present) | A=True, B=True |

Optional one-command publication bundle:

```bash
python scripts/run_publication_verification_bundle.py
```

## Step 3 — Spot-check three domains (~3 min)

```bash
python scripts/reproduce_domain_panel.py --panel Fuel_Lab_Live_Panel --deep
python scripts/query_fsot_domain_navigator.py --intent cosmology_cmb
python scripts/query_fsot_domain_navigator.py --query hubble
```

**Expect:** Fuel Lab pooled ≤0.5%; cosmology/Hubble panels present.

## Step 4 — Near-miss transparency (~1 min)

```bash
python scripts/build_benchmark_near_miss_ledger.py
```

Open `data/publication/BENCHMARK_NEAR_MISS_LEDGER.md` — worst green domains published openly.

## Step 5 — Formal spine (optional, longer)

```bash
python scripts/run_cross_proof_verification.py
```

**Expect when toolchains installed:** `overall_ok: true` in `data/cross_proof_verification_report.json`  
(at kit generation: multiprover overall_ok=True).

## What would falsify FSOT?

1. Any active benchmark fails green gate after fresh clone (no local edits).
2. `overall_ok: false` in cross-proof report with provers installed.
3. Authority pin leaves D1D38A without a documented migration.
4. Preregistered prediction PRED rows violated after manifest-locked registration.
5. Parameter audit finds per-observable least-squares tuning.

## Artifacts to cite

- `docs/CURRENT_STATUS.md` / `data/repo_status_snapshot.json`
- `data/benchmark_margin_audit.json`
- `data/publication_claims_manifest.json`
- `data/cross_proof_verification_report.json`
- `data/publication/domain_atlas.csv`
- Math key: [`FSOT_MATH_KEY.md`](FSOT_MATH_KEY.md)
- Main thesis: [`README.md`](../README.md)

Regenerate this kit: `python scripts/build_skeptic_replication_kit.py`  
(after `python scripts/build_repo_status_snapshot.py` and margin audit).
