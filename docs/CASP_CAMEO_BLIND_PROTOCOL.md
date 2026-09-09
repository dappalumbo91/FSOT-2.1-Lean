# CASP / CAMEO-style blind plan (OPEN)

**Owner:** Grok Build run on the Genetics freeze, not a post-hoc RMSD pick.  
**Pin:** D1D38A · product freeze 2026-08-17 · **0 free parameters**.  
**This hub does not invent a CASP score.** Docs state the protocol; the run is future work.

## Why this exists

CASP16 / AF3 / cryo-EM papers talk **AF ceiling** (experimental uncertainty) or **FSC ~1.24 Å maps**. None of those is the Genetics **product** 0.13 Å. A reviewer who equates AF Å, cryo-EM Å, and product Å is scoring the wrong object ([`GENETICS_CLAIM_EVIDENCE.md`](GENETICS_CLAIM_EVIDENCE.md)).

A **blind** plan is the only honest next product claim beyond the same-data 10-protein freeze.

## Protocol (do not skip)

1. **Freeze the engine** at the 2026-08-17 product path (F01–F15 + measured-homolog transfer; 3-D MDS **not** emitted).
2. **Register targets before coordinates are used as eval.** CASP/CAMEO target IDs, sequences, and a SHA of the formula pack (`formulas/fsot_protein_formulas.json` + pin D1D38A).
3. **Same information universe as the freeze:** homologs allowed except the evaluation PDB. Sequence-only (no-map) is a **separate** track and must not emit a 3-D fold.
4. **Metrics:** Cα RMSD vs experimental (or CASP GDT). Report product vs AF vs cryo-EM FSC **in three columns**. Never one Å number.
5. **Kill:** product median on the blind set **> AF median on that same set**, or any freeze-winner protein **> 3 Å**, or a fitted spring / MDS grind.
6. **Anti-goals:** bond-idealizing intact crystals; residual picking DFG-in vs DFG-out; quoting 0.13 Å as “from sequence alone.”

Sources to cite as *context*, not as the product: CASP16 prot.70076 / prot.70031; Nat Biotech AF3 ensembles doi:10.1038/s41587-026-03166-5; IUCrJ 1.24 Å doi:10.1107/S2052252526004100.

Sibling OPEN list: Genetics `docs/OPEN.md` (copied at [`../results/siblings/genetics/OPEN.md`](../results/siblings/genetics/OPEN.md)).
