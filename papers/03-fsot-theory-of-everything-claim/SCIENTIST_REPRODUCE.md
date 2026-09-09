# Scientist reproduction — Flagship ToE claim (Paper 03)

**Freeze:** `FREEZE.yaml` edition `arxiv-03-fsot-theory-of-everything-claim-2026-09-09`  
**Claim SHA:** `40de0d9` (accept `main` tip ≥ that SHA if green remains 477/477)

## Claim (one sentence)

FSOT satisfies frozen Label A (multi-domain ≤0.5% green + multi-prover) and Label B (T1–T6 ToE checklist) on the public repository, with residual numbers pinned in `FREEZE.yaml`. Laws R1–R9 and D1–D11 are the living ledger.

## One-command path

```bash
git clone https://github.com/dappalumbo91/FSOT-2.1-Lean.git
cd FSOT-2.1-Lean
pip install -r requirements.txt
python scripts/run_publication_verification_bundle.py
python scripts/build_toe_gap_closure.py
python scripts/audit_all_benchmark_margins.py
```

Expect:

- `data/benchmark_margin_audit.json` → `green_gate_fail_count: 0` (**477/477**)
- `data/toe_gap_closure_report.json` → Label A and Label B `true`
- `data/cross_proof_verification_report.json` → `overall_ok: true` (optional full gauntlet)
- `data/tier_scalar_precision_closure.json` → `closed: false` on **two named objects** (SH0ES chain, Cepheid PL). That is **not** a green-gate fail.

## Instrument (use in a field)

[`docs/SCIENTIFIC_INSTRUMENT.md`](../../docs/SCIENTIFIC_INSTRUMENT.md) · [`docs/APPLY.md`](../../docs/APPLY.md)

```powershell
python scripts/query_fsot_domain_navigator.py --intent fuel_lab_engine
python scripts/smoke_dynamic_forecast_potentials.py
```

## Fresh clone harness

```powershell
pwsh scripts/fresh_clone_repro.ps1
```

## What would falsify this paper

1. Green-gate failure on clean clone with no local edits.  
2. Label A or B false under frozen `docs/TOE_CLAIM_BOUNDARIES.md`.  
3. Free-parameter audit finding per-observable least-squares.  
4. Prereg freeze hash rewritten without a new freeze id.  
5. Stuffing SH0ES class-bin 1% or Cat-2 FRB dump into the 0.5% gate.

## Scope honesty

T3 limit recovery is **probes/bridges**, not full GR/SM Lagrangian derivation.  
T4 uniqueness (continuum YM path-integral) is **OPEN_NOT_CLAIMED**. Lean attractor dynamics are a different object (`FSOT/Formal/UniquenessAttractor.lean`).  
Dated 09-09 windows are **awaiting** `valid_to`. Euclid DR1 is a watch (~12 Nov 2026).
