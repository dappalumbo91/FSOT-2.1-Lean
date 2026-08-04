# Recent breakthrough expansion

**Date:** 2026-08-04  
**Honesty:** Documents post-hoc residual binds of public breakthroughs. QCE was **not** in the 2026-07 prereg freeze — this is expansion after the Max Planck / PRL result, not a backdated prediction claim.

## Panels

| Domain | File |
|--------|------|
| QCE / ELM fusion edge | `data/qce_elm_fusion_edge_panel_benchmark.json` |
| Recent breakthroughs rollup | `data/recent_breakthroughs_expansion_panel_benchmark.json` |
| Spine | `data/breakthrough_fusion_spine_benchmark.json` |

## Anchors

`vendor/fusion/qce_elm_public_anchors.json` — Zhang et al. PRL 2026 QCE summary anchors.

## Commands

```powershell
python scripts/build_recent_breakthrough_expansion.py
python scripts/gen_recent_breakthrough_lean.py
python scripts/audit_all_benchmark_margins.py
```

## Covered breakthroughs (initial set)

1. **QCE Goldilocks / ELM exhaust** (2026 IPP) — continuous vs burst, 1/5 ELM dump bound, blob classes, ballooning access gate  
2. **NIF ignition 2022** — Q>1 / yield  
3. **EAST long-pulse H-mode 2023** — τ class  
4. **ITER / SPARC design Q** — design targets  
5. **Room-temp quantum comm literature class** — θ measurement law invariant (not device fidelity fold)  

## Densify status (2026-08-04)

Granular depth added: multi-blob classes, SOL 1–10 mm, power ladder, L-mode/ELMy/QCE regimes, KBM/RXM flags, 8+ validation obs class, machine candidates (ITER/DEMO/SPARC), NIF/EAST/facility Q ladder on breakthroughs panel.

## Gap for later densify

- Numeric α_m ballooning threshold residual (needs equilibrium numbers)  
- Gyrokinetic follow-on parameters from paper limitations section  
- Thin science domains outside fusion (separate campaign)  
- Full multiprover re-run after this densify batch  

