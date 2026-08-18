# Product freeze — structure path (2026-08-13)

**Marked results.** Do not silently overwrite this table. Remaining misses: `docs/OPEN.md`. Audit: `docs/AUDIT.md`.

**Status:** Same-data product (exclude eval PDB only).  
**Authority pin:** `D1D38A` · law \(S = K(T_1+T_2+T_3)\) · **0 free parameters**.

## Frozen product numbers (H2H, 10 proteins)

Source: `data/product_vs_alphafold.json` — every measured homolog except the
evaluation PDB. Same information universe as AlphaFold. Same-protein crystals
are clustered (`trit_consensus`); residual ranks inside a collapse; the
apparatus is scored across collapses. NMR ensembles are Superposed (trit 0)
and never residual-best. Intact measured transfers are not bond-idealized
(wrong interface). A near-self sequence search (id ≥ 1/φ) recovers crystals
the 0.25/80 search buried.

| metric | value |
|--------|------:|
| AlphaFold median Cα RMSD | **0.47 Å** |
| FSOT **product** median | **0.13 Å** |
| FSOT template median | **0.13 Å** |
| FSOT bulk (orphan) median | 13.57 Å |
| Product within 1.5 Å of AF | **10/10** |
| Product sub-2 Å | **10/10** |
| Fair-cap 0.95 median (handicap) | 1.14 Å |

Notable product Cα RMSDs:

| protein | product Å | AF Å |
|---------|----------:|-----:|
| p53 DNA-binding | 0.01 | 6.19 (product wins) |
| Ubiquitin | 0.09 | 0.88 (product wins) |
| RNase A | 0.09 | 0.33 (product wins) |
| SOD1 | 0.10 | 0.29 (product wins) |
| Lysozyme | 0.12 | 0.42 (product wins) |
| Insulin | 0.14 | 4.51 (product wins) |
| CAII | 0.14 | 0.36 (product wins) |
| Hb α | 0.21 | 0.27 (product wins) |
| Hb β | 0.22 | 0.52 (product wins) |
| Calmodulin | 0.90 | 6.45 (product wins) |

## What the product *is*

```
measured homolog Cα
  (id×cov authority; residual-fit filter if data-best transfer is unfit)
  → if transfer is bond-intact: keep the measured map
  → else residual-weighted physics
      bond   ← Physical_Chemistry · residual (1+|S|·P_NEW)
      clash  ← Chemistry
      anchor ← Biochemistry (template authority)
  → Cα model
```

- Templates = **measured authority** (RCSB/Pfam homologs; identity cap 0.95 fair H2H).
- MSA = **data**, not trained weights.
- Bulk de-novo ≈ 11–14 Å is the single-sequence information ceiling — not a bug.

## What we are *not* doing next

- Geometric shotgun (medoid-all, false contacts, residual springs that tank median).
- Bond-idealizing an already-intact crystal (that was 1EXR 0.80→1.16).
- Claiming AlphaFold-beating bulk fold without more measured coverage / hardware path.

## What we *are* doing next

**Polish + bare metal.** See `docs/BARE_METAL_GENETICS_ROADMAP.md`.

Python under `scripts/` remains the **research bench and oracle** for metrics.  
**Runtime product** moves to Zig (host + freestanding QEMU) / optional Rust `no_std`, same pin, same residual law, trinary codon front door.

Gate for any structure change: **do not ship if same-data product median > 0.47 Å** (AF median) on this freeze set, or if a previously winning protein jumps above 3 Å (poison state). Fair-cap 0.95 handicap remains a documented side number, not the product.
