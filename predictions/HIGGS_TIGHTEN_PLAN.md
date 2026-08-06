# Higgs tighten plan (next phase — after prediction layers)

## Goal

**Beat** standard Higgs reporting precision (PDG / ATLAS / CMS class tolerances)
on FSOT seed readouts — **without** changing the global framework residual gate
(≤ **0.5%**).

The Grok app critique is valid as a *capability challenge*: literature often quotes
tighter absolute uncertainties on m_H than a 0.5% framework envelope. We answer by:

1. Keeping **0.5% as the framework kill** (whole atlas discipline).
2. Adding a **literature-tight secondary band** per Higgs observable.
3. Driving engine/panel refinement until FSOT error **beats** that band.

## Current snapshot

- FSOT m_H central ≈ **125.2637798817715** GeV  
- Higgs predictions registered: **17**  
- Already inside literature-tight band today: **17**  
- Outside tight band today (improve these first): **[]**

## Dual criteria (do not collapse them)

| Level | Gate | Role |
|-------|------|------|
| **Framework** | ≤ 0.5% | Immutable atlas / ToE residual law |
| **Literature-tight** | ~0.05–0.15% mass · ~0.15–0.40% BR | Competitive score vs PDG/exp |

A channel can be **framework-green** and still **tight-red**. That is the improvement queue.

## Work program (after catalog layer is live)

1. **Baseline freeze** — this layer + Git SHA (done when `higgs_prediction_layer.json` is committed).  
2. **Error budget** — split seed formula vs densify vs experiment-central mismatch for each fail.  
3. **Branching priority** — BR channels with largest gap to tight band.  
4. **Mass multi-experiment** — ATLAS/CMS/LHCb centrals already separate PREDs; refine so all beat tight % while formula stays seed-locked.  
5. **No free parameters** — no per-channel ε. Only seed-consistent structure or honest residual report.  
6. **Public scoreboard** — report *both* “framework hold” and “beats PDG-class tight %” on X.

## Explicit non-goals

- Do **not** lower the global 0.5% gate for all domains.  
- Do **not** retune m_H after PDG updates without a new freeze id.  
- Do **not** market Tier D scaffolds as Higgs proof.

## Commands

```powershell
python scripts/build_higgs_prediction_layer.py
# later: refine vendor/fsot path / higgs panel builders, then re-run
```

## Related

- Layer: `predictions/higgs_prediction_layer.json`  
- Table: `predictions/reports/HIGGS_PREDICTION_LAYER.md`  
- Framework boundaries: `docs/TOE_CLAIM_BOUNDARIES.md`
