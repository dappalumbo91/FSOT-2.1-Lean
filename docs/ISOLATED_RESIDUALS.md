# Isolated residuals — do not stuff

*Generated 2026-09-09T16:04:03.910423+00:00 · pin D1D38A*

If a residual is huge and everything else is sub-percent, the mathematics
is usually **applied to the wrong object** (wrong \(D_{\mathrm{eff}}\), wrong
split, class vs chain). Isolate it. Name the interface. Do **not** add a
coefficient so the 0.5% gate looks pretty.

Once the right object is named and gated, the ugly number is **remedied** —
retired formula, do-not-use note — **not** an open isolate.

**Refresh:** `python scripts/diagnose_frb_dm_interface.py` then
`python scripts/build_frb_orifice_benchmark.py` then this script.

## Open isolates

| ID | Error | Verdict | Why | Next apply |
|----|------:|---------|-----|------------|
| `ISO-SHOES-CLASS-BIN` | **1.00%** | WRONG_OBJECT_ISOLATED | 73.04 is a three-rung mixture, not the class bin. Chain 72.856 vs 73.04 is 0.252%. | Kill the class row on the 2.5% band; score the chain; do not retune ρ |

## Remedied — retired formulas (do not reuse, do not keep open)

| ID | Retired error | Verdict | Why | What replaced it |
|----|--------------:|---------|-----|------------------|
| `ISO-FRB-200x1pdens` | **66.44%** | REMEDIED_WRONG_APPLY | IGM path (Cosmology D=25) vs H0 angular kernel (±0.2). Formula trapped in ~160–240 pc; measured excess 15–580. Sign wrong. Orifice replaced it — not an open isolate. | PRED-084 orifice (width×fluence vs e·POOF). PRED-052 200 class. PRED-076 kernel is angular grammar only. |
| `ISO-FRB-PHI6-DAYS` | **9.75%** | REMEDIED_WRONG_OBJECT | 16.35 d is the saloon-door activity season, not a compactification tick. φ⁶ is the wrong object. Live handle is T=5π+1/φ days (0.147%). | T_activity = D_particle·π + 1/φ days (Particle orifice cycle + Omori c rest) |
| `ISO-MAT-OPT-S-RATIO` | **17.84%** | REMEDIED_WRONG_APPLY | vs 1 is the same-C same-δψ test. Materials δψ=1/2 is the body/mass look; Optics δψ=3/5 is the light look. C does not enter S. The 18% is that observer-phase fold (T1 perception, D9), not a failed n/ρ tissue. Closed form |1+T1_mat|/|1+T1_opt| matches live |S| (T3 leftover 0%). Live handle vs PhysChem/Chem is 0.329%. | T1 view (D9): |S_i|/|S_j|=|1+T1_i|/|1+T1_j|. Fold the look-split onto Physical_Chemistry/Chemistry (same 0.5/0.6 at D=8). CRC n/ρ dual-route. Ice n vs φ²/2. |

## Rules

1. Report the ugly number in `results/`.
2. Name the object that was applied vs the object science measured.
3. If they differ, the residual is not a failed 0.5% central.
4. When the right object is gated, move the ugly number to **remedied**.
5. Forbidden: β-fit, ρ-retune, identity pads, moving the green gate,
   keeping a remedied wrong-apply on the open isolate list.

Related: [`APPLY.md`](APPLY.md) · [`OBJECT_SCORING.md`](OBJECT_SCORING.md) ·
[`FRB_INTERFACE_DIAGNOSIS.md`](FRB_INTERFACE_DIAGNOSIS.md) ·
[`FRB_ORIFICE.md`](FRB_ORIFICE.md) ·
[`SH0ES_LADDER_DIAGNOSIS.md`](SH0ES_LADDER_DIAGNOSIS.md)
