# Open failures (marked 2026-08-17)

Results in `docs/PRODUCT_FREEZE.md` and `data/product_vs_alphafold.json` are **frozen**.  
This list is what to clear next. One mechanism at a time. Pin `D1D38A`. 0 free parameters.

## Product H2H

| Item | Now | Target / handle |
|------|-----|-----------------|
| Calmodulin 1CLL | **0.52 Å** (3CLN) | Closed. UniRef100 *other-accession* PDB xrefs admit P0DP29/3CLN; leftover collapse keeps every intact observation so residual cannot drop 3CLN for 1UP5. |
| Side-chain heavy atoms | **1.01 Å** · centroids **0.41** (CA 0.12) | Closed as a frame bug. Observed SC rides the Cα superposition (backbone unobserved). Remaining ~1 Å is crystal-to-crystal rotamer scatter. |
| Hydrogens | **1.01 Å** (961/962 on 1LZN, source 8RLH) | Closed as an observer-policy bug. EXPDTA-only neutron H; H/D name dedupe; pick the neutron map in the product collapse. Remaining ~1 Å is neutron-to-neutron H variance. |

## Coverage / AF3 depth

| Item | Note |
|------|------|
| Joint `predict_system` | **0.013 Å** protein · DNA C1′ **0.016 Å** · SC **0.016 Å** — apparatus min now matches the DNA job. |
| Protein–RNA | U1A prot **0.23 Å** · RNA seed C1′ **0.28 Å** (9 nt). Full hairpin register still Superposed. |
| Ligand site | trypsin–BEN **0.60 Å** (was 0.24 on 3PTB/1PPH). First-shell springs; not a Cα freeze item. |
| Organism 3-D / lineage | Proxy find **1.00**, follow **1.00 / 1.00**, Jaccard **1.00**. Dense find **0.96**, follow **0.84 / 0.94**, Jaccard **0.82 (adj. 0.83)** — TP 1538 / FP 6 / FN 333. Leftover-length dests yield when 2-opt cannot swap. Kaggle U-Net leftover public **0.821** (not Final; 0.848 holds). |

## Historical wet-lab (not the 10-protein freeze)

See `docs/MECHANISM_GAP_MAP.md` (historical wet-lab ledger — not the freeze scoreboard). Still open there: EGFR coverage, vaccine-antigen domain scope, CASP/CAMEO blind. P72R specificity is **closed** (`common_polymorphism`).

Medical expansion: `docs/MEDICAL_PLATFORM.md`. Experimental PGx: **10/10** (`scripts/bench_experimental_pgx.py`, disclosure required).

- **P72R** → `common_polymorphism` (pop AF ≥ 1/φ³).
- **HBB E122Q** (Hb D-Punjab) is not a failed driver: mid-conservation, α1β1 interface, compound-sickle apparatus. Catalog role is `context_dependent`. Solo call stays `uncertain`. PGx: `on_ppi_site` on 1A3N B121.

## CASP / CAMEO blind (OPEN — Grok Build owns the run)

There is **no** literature hit that is the 0.13 Å product. CASP16 (prot.70076 / prot.70031), AF3 ensembles, and ~1.24 Å FSC maps are **other objects**. Protocol (do not skip):

1. Freeze the 2026-08-17 product path (no MDS fold).
2. Register target IDs + sequences + formula-pack SHA **before** eval coordinates are used.
3. Two tracks: product (homologs except eval PDB) vs no-map (F01–F15 only, no 3-D).
4. Report product / AF / cryo-EM FSC in **three columns**.
5. Kill: blind product median > AF median on that set; freeze-winner > 3 Å; fitted spring.

Hub copy of the protocol: Lean `docs/CASP_CAMEO_BLIND_PROTOCOL.md`.

## Anti-goals (do not “fix” these)

- Grinding 3-D MDS bulk toward AlphaFold. Backbone is unobserved; pairwise contacts underdetermine a Cα fold. That path is **retired as a product** (`no_measured_map`). F01–F15 formulas (CA_CA, Rg target, secondary) stay — they still feed the measured product.
- Residual picking DFG-in vs DFG-out.
- Bond-idealizing intact crystals.
- Geometric shotgun (medoid-all, invented contacts).
