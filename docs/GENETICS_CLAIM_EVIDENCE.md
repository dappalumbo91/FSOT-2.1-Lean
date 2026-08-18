# Genetics (C6) — claim → sibling freeze → kill command

**Purpose:** A skeptic who thinks “FSOT is 15 Å off” or “they replaced AlphaFold from sequence” should be able to **read the live sibling freeze**, not an old Lean snapshot.

**Pin:** **D1D38A** (byte-identical in [FSOT-Genetics](https://github.com/dappalumbo91/FSOT-Genetics))  
**Picture:** [`CONCEPTS.md`](CONCEPTS.md) **C6**  
**Authority freeze:** 2026-08-17 · `docs/PRODUCT_FREEZE.md` in the Genetics repo · pulled copy [`../results/siblings/genetics/PRODUCT_FREEZE.md`](../results/siblings/genetics/PRODUCT_FREEZE.md)

This hub does **not** re-run the protein engine. It quotes the sibling freeze. Refresh:

```powershell
python scripts/sync_sibling_embodiment_ledgers.py
```

---

## What the live Genetics repo actually says (2026-08-17)

I re-read `C:\Users\damia\Desktop\FSOT-Genetics` (README, `docs/AUDIT.md`, `docs/OPEN.md`, `docs/PRODUCT_FREEZE.md`, `data/product_vs_alphafold.json`). The product path is **closed** at 0.13 Å. The thing that was “fixed” after the 2026-08-13 Lean pull is **claim language + CaM/SC/H observer law**, not a new median invented here.

| Claim | Live number | Where | Kill |
|-------|-------------|-------|------|
| Same-data product median Cα | **0.13 Å** vs AlphaFold **0.47 Å** | `data/product_vs_alphafold.json` (n=10) | product median **> 0.47 Å** (AF) or any freeze winner **> 3 Å** |
| All ten beat AF / sub-2 Å | **10/10** | same | any protein loses the freeze set |
| Calmodulin | **0.52 Å** via 3CLN (P0DP29) | PRODUCT_FREEZE + OPEN | residual must not drop 3CLN for 1UP5 |
| Side-chain / hydrogens | SC centroids **0.41** · SC heavy **1.01** · H **1.01** | OPEN — closed as *observer-policy*, leftover is crystal scatter | do not “fix” rotamer scatter with a spring |
| Joint `predict_system` | protein **0.013 Å** · DNA C1′ **0.016 Å** | OPEN coverage | apparatus min must still match the DNA job |
| Experimental PGx | **10/10** public mechanism classes | `scripts/bench_experimental_pgx.py` | disclosure required; not a marketing panel |
| **No measured map** | F01–F15 only (Rg, secondary). **3-D MDS is not emitted** | README + OPEN anti-goals | do **not** grind MDS toward AF |

The old **~11–14 Å / ~15 Å** figure is the **retired** `--force-bulk` MDS path. It is **not** the product and it is **not** a live fold the hub should score.

---

## Two regimes (never mix)

| Regime | What it is | What you may say |
|--------|------------|------------------|
| **Product** | Every measured homolog except the eval PDB + residual only when bonds are broken | 0.13 Å vs AF 0.47 Å, same information universe, 0 free parameters |
| **No measured map** | Sequence-only F01–F15. No 3-D fold emitted | “We do not invent a fold.” |

Do **not** say: *de-novo fold beats AlphaFold*, *0.13 Å from sequence alone*, or *FSOT is 15 Å off* without naming the retired MDS fallback.

---

## What stays open (Genetics `docs/OPEN.md`, not this hub)

| Item | Status |
|------|--------|
| Protein–RNA full hairpin register | Superposed; seed C1′ 0.28 Å (9 nt) |
| Ligand site (trypsin–BEN) | 0.60 Å first-shell — not a Cα freeze item |
| CASP / CAMEO blind | still open on the historical wet-lab ledger |
| 3-D MDS bulk → AF | **anti-goal** — retired |

Those are sibling work. The Lean hub quotes the freeze and refuses the 15 Å product headline.

---

## Stale numbers on *this* hub — ignore

| Phrase | Why it is stale |
|--------|-----------------|
| Genetics freeze **2026-08-13** / CaM **0.90 Å** | Superseded 2026-08-17: CaM **0.52 Å** (3CLN) |
| Bulk / orphan median **~13.6 Å** as a live product-adjacent fold | Retired MDS. Genetics no longer emits that fold. |
| `predictions/reports/FSOT_VS_ALPHAFOLD_STRUCTURE.md` ~15 Å | 2026-08-07 sequence-only snapshot. Banner already says bulk-only. |

---

## Related

- Sibling INDEX: [`../results/siblings/INDEX.md`](../results/siblings/INDEX.md)  
- Consciousness map (same skeptic shape): [`CONSCIOUSNESS_CLAIM_EVIDENCE.md`](CONSCIOUSNESS_CLAIM_EVIDENCE.md)  
- Genetics repo: https://github.com/dappalumbo91/FSOT-Genetics
