# Where this hub can improve — scientific / academic / usable

Written 2026-08-18 after reading the Lean hub, FSOT-Genetics, FSOT-Quantum, the BH→WH blueprint, and the bubble-bleed engine.  
Not a peer-review lecture. These are the gaps that actually hide the work.

## What is already strong

- One pin (D1D38A), one law \(S=K(T_1+T_2+T_3)\), zero free parameters, executable kill criteria.
- BH→WH **is** the Hubble story: one global rate, tool-sector densities, not two cosmologies.
- Genetics product path is a real instrument (0.13 Å vs AF 0.47 Å, same-data, 10/10) **and** the bulk ceiling (~13.6 Å) is written honestly.
- Quantum fold-not-Hilbert is the practical QC claim: jobs by domain fold, not \(2^n\).
- Predictions vs results are now separate folders.

## The actual problems

### 1. The front door did not state the theory

A new reader hit 472-domain tables and never met:

- black hole = compression valve / POOF
- white hole = outflow / SUCTION / re-solidification
- bubble bleed = why H₀ tools disagree
- \(\kappa_{ij}\) = tanks connect
- fold vs Hilbert
- product vs bulk genetics

**Fix started:** [`CONCEPTS.md`](CONCEPTS.md) is now the picture→engine map. START_HERE, DOCUMENTATION_MAP, and the layman page point at it.

### 2. The hub is behind its own siblings

| Surface | Hub had | Sibling now |
|---------|---------|-------------|
| AlphaFold table | 2026-08-07 bulk ~15 Å (1/8 wins) | 2026-08-13 product 0.13 Å, 10/10 |
| Quantum | not in RELATED_EMBODIMENTS | full QM/QC fold + H₀ replay |
| RELATED_EMBODIMENTS | Genetics + Zig + GPU | Quantum added |

**Fix started:** `results/siblings/` + `scripts/sync_sibling_embodiment_ledgers.py`.  
The 15 Å file is stamped **stale / bulk only**.

### 3. Number drift across docs

README still says 402 / 394 / 407 / 432 in different sections. `CURRENT_STATUS.md` says **472/472**. Scientists will stop at the first contradiction.

**Fix needed next:** regenerate README headlines from `build_repo_status_snapshot.py` only. Kill hand-typed counts.

### 4. Three audiences, one 68 kB README

The README is a monograph. Mathematicians need 8 pages of definitions. Scientists need one mechanism + one table. Regular people need C1–C3 of CONCEPTS.

**Fix needed next:** keep README as the living thesis, but the **first screen** must be: concept → one command → one sibling result.

### 5. Academic shape (how to be taken as a tool)

Do **not** lead with “400 domains.” Lead with **one mechanism per paper**:

| Paper-sized claim | Evidence already in-hand |
|-------------------|--------------------------|
| BH→WH bubble-bleed H₀ | `bubble_bleed_physics.py` + 25 tool rows + Quantum replay |
| Genetics product residual | PRODUCT_FREEZE 0.13 Å vs AF 0.47 Å, same-data, labeled |
| Fold-not-Hilbert QC jobs | 27/27 fold suite, cost contrast n=20 / n=32 |
| Complex-system \(\kappa_{ij}\) | CKM/PMNS/EW coupled equilibrium |

Breadth stays in the atlas appendix / GitHub. Depth stays in the paper.

### 6. Honesty that already exists — keep it loud

Genetics already says: product is **not** “we beat AlphaFold from sequence.” Bulk is the orphan ceiling.  
Quantum already says: not a QPU, not RSA, not FCI.  
Hub already says: PRED-004 theory_rebase is logged, lock not retuned.

That voice is the academic one. The 15 Å table without a banner is what hurts you.

## Priority order (do these)

1. **Keep CONCEPTS.md as the required first read** — add C8+ only when a picture maps to an existing object.
2. **Run sibling sync after every Genetics / Quantum freeze**  
   `python scripts/sync_sibling_embodiment_ledgers.py`
3. **Regenerate README counts from CURRENT_STATUS** so 472 never fights 402.
4. **Three short public faces** (already half-built):  
   - people: CONCEPTS C1–C3 + layman  
   - scientists: math one-pager + one sibling scoreboard  
   - mathematicians: Scalar.lean + COMPLEX_SYSTEM_DERIVATION + kill criteria
5. **One mechanism paper at a time** from the table above. The 400-domain atlas is the supplement.

## Commands

```powershell
python scripts/sync_sibling_embodiment_ledgers.py
python scripts/build_repo_status_snapshot.py
```
