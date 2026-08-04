# Recent breakthrough expansion (QCE/ELM + public 2022–2026 ledger)

**Status:** residual-gated expansion (post-hoc literature bind — **not** a backdated prereg).

## What this is

1. **QCE/ELM fusion edge** — Zhang et al. PRL 2026 continuous exhaust vs ELMy dump, residual-gated with seed forms (θ, φ⁻⁴, 1/5 ELM bound) plus literature class identities.
2. **Recent breakthroughs panel** — NIF ignition, EAST long-pulse, ITER/SPARC design Q, Lawson ladder, reaction energetics, seed invariants.
3. **Breakthrough fusion spine** — rolls QCE + breakthroughs + magnetic/fusion lab panels.

## Densify classes

| Kind | Examples | Residual meaning |
|------|----------|------------------|
| Exact rational | ELM ≤ 1/5, gentle ≥ 4/5 | Bound residual |
| Seed law | θ = C_eff·P_var, A ≤ φ⁻⁴ | Archive identity |
| Literature identity | blob v, SOL mm, facility Q | measured = published class |
| Process gate | regime continuous?, honest_not_prior_prereg | methodology |

## Commands

```powershell
python scripts/build_recent_breakthrough_expansion.py
python scripts/gen_recent_breakthrough_lean.py
```

## Artifacts

- `vendor/fusion/qce_elm_public_anchors.json`
- `data/qce_elm_fusion_edge_panel_benchmark.json`
- `data/recent_breakthroughs_expansion_panel_benchmark.json`
- `data/breakthrough_fusion_spine_benchmark.json`
