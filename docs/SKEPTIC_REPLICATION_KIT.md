# FSOT Skeptic Replication Kit

*15-minute verification path · 2026-07-16 · commit `7e972dd16e21`*

Run this if you want to **break FSOT fast** — not read 12,000 lines of appendix first.

## Step 1 — Clone and install (~2 min)

```bash
git clone https://github.com/dappalumbo91/FSOT-2.1-Lean.git
cd FSOT-2.1-Lean
pip install -r requirements.txt
```

## Step 2 — One-command verification bundle (~8 min)

```bash
python scripts/run_publication_verification_bundle.py
```

**Expect:** `=== Publication verification bundle complete ===` with no hard failures.

| Check | Expected |
|-------|----------|
| Benchmark green | 394/394 |
| Cross-proof | `overall_ok: true` in `data/cross_proof_verification_report.json` |
| Contested pooled | ~0.030% in `data/contested_observables_closure.json` |

## Step 3 — Spot-check three domains (~3 min)

```bash
python scripts/reproduce_domain_panel.py --panel Fuel_Lab_Live_Panel --deep
python scripts/query_fsot_domain_navigator.py --intent hubble_tension
python scripts/audit_parameter_count.py
```

**Expect:** Fuel Lab pooled ≤0.5%; H₀ tension row present; parameter audit **ZERO_FREE**.

## Step 4 — Near-miss transparency (~1 min)

```bash
python scripts/build_benchmark_near_miss_ledger.py
```

Open `data/publication/BENCHMARK_NEAR_MISS_LEDGER.md` — worst green domains published openly.

## Step 5 — Formal spine (optional, ~5 min)

```bash
python scripts/run_cross_proof_verification.py
```

## What would falsify FSOT?

1. Any benchmark domain fails green gate after fresh clone (no local edits).
2. `overall_ok: false` in cross-proof report.
3. Preregistered prediction PRED-001–041 violated after manifest-locked registration.
4. Parameter audit finds per-observable least-squares tuning.

## Artifacts to cite

- `data/publication_claims_manifest.json`
- `data/cross_proof_verification_report.json`
- `data/publication/domain_atlas.csv`
- Main thesis: [`README.md`](../README.md)

Regenerate this kit: `python scripts/build_skeptic_replication_kit.py`
