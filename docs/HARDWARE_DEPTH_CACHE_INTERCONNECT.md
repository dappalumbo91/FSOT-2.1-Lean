# Hardware depth — cache hierarchy, interconnect, C parity

**Date:** 2026-08-04  
**Status:** residual-gated + multiprover path (with processor/RAM/GPU)

## Scope

Same-class silicon layers (not GPU-vs-CPU confusion):

| Layer | Same-class industry bar | FSOT residual |
|-------|-------------------------|---------------|
| **Cache** | 64 B line, \(2^k\) L1/L2/L3, L1&lt;L2&lt;L3 | trit/line packing, locality \(A_\mathrm{frac}\le\phi^{-4}\) |
| **Interconnect** | Always-on bus / broadcast | coherence gate, active speakers ≤ \(\phi^{-4}\) |
| **C host** | ad-hoc floats | thin pack/θ golden parity only |

## Commands

```powershell
python scripts/run_hardware_competitive_refine.py
python scripts/build_hardware_depth_bridge.py
python scripts/gen_hardware_depth_lean.py
python scripts/run_fsot_hardware_bare_metal.py
lake build FSOT.Formal.FsotCacheHierarchyPanelPriors FSOT.Formal.FsotInterconnectCoherencePanelPriors FSOT.Formal.FsotCPackParityPanelPriors
python scripts/run_cross_proof_verification.py
```

## C parity (optional evidence, not authority)

`verification/c/fsot_pack_parity/fsot_pack_parity.c` — compile with clang/gcc; markers must match archive θ and pack word `5270498306774157604`.

## Panels

- `data/fsot_cache_hierarchy_panel_benchmark.json`
- `data/fsot_interconnect_coherence_panel_benchmark.json`
- `data/fsot_c_pack_parity_panel_benchmark.json`
- `data/fsot_hardware_depth_spine_benchmark.json`
