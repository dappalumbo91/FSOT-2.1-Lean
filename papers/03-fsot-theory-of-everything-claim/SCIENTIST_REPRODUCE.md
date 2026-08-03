# Scientist reproduction — Flagship ToE claim (Paper 03)

## Claim (one sentence)

FSOT satisfies frozen Label A (multi-domain ≤0.5% green + multi-prover) and Label B (T1–T6 ToE checklist) on the public repository, with residual numbers pinned in `FREEZE.yaml`.

## One-command path

```bash
git clone https://github.com/dappalumbo91/FSOT-2.1-Lean.git
cd FSOT-2.1-Lean
pip install -r requirements.txt
python scripts/run_publication_verification_bundle.py
python scripts/build_toe_gap_closure.py
```

Expect:

- `data/benchmark_margin_audit.json` → `green_gate_fail_count: 0`
- `data/toe_gap_closure_report.json` → both labels `true`
- `data/tier_scalar_precision_closure.json` → `closed: true`
- optional: `data/cross_proof_verification_report.json` → `overall_ok: true`

## Fresh clone harness

```powershell
pwsh scripts/fresh_clone_repro.ps1
```

## What would falsify this paper

1. Green-gate failure on clean clone with no local edits.  
2. Label A or B false under frozen `docs/TOE_CLAIM_BOUNDARIES.md`.  
3. Free-parameter audit finding per-observable least-squares.  
4. Prereg freeze hash rewritten without a new freeze id.

## Scope honesty

T3 limit recovery is **probes/bridges**, not full GR/SM Lagrangian derivation.  
T4 includes an explicit scope statement until a full force package exists.
