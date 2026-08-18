# Repository audit — 2026-08-17

Compared **code + `data/product_vs_alphafold.json` + `data/af_coverage.json`** to every public claim surface after the CaM/SC/H ChemLink pass (`325e481`).

## Authority (current)

| Surface | Status |
|---------|--------|
| Pin `D1D38A` | Current. `vendor/fsot_compute.py`, `AGENTS.md`, Lean `FSOTGenetics/`. |
| Product H2H median **0.13 Å** vs AF **0.47 Å** | Current. `data/product_vs_alphafold.json` (CaM **0.52 Å** via 3CLN). |
| Coverage: SC 0.41/1.01 · H 1.01 · joint 0.013 | Current. `data/af_coverage.json`. |
| `docs/PRODUCT_FREEZE.md` | 2026-08-17 table. |
| `docs/CAPABILITY_ROADMAP.md` | Live scoreboard is product 0.13, not fuse-era 1.16. |
| `docs/OPEN.md` | CaM/SC/H closed; ligand / RNA hairpin remain. |

## This pass (claim-language)

| Surface | Old reading | Truth |
|---------|-------------|-------|
| Capability / README bulk lead | “FSOT is ~15 Å off” | That is **orphan bulk**. Product is **0.13 Å**. |
| `docs/CAPABILITY_ROADMAP.md` | Fuse **1.16 Å** as “best deploy path” | Stale fair-cap era. Product is 0.13. |
| `docs/PARITY_ZIG_PYTHON.md` | Freeze 1.16 Å | Metric authority is **0.13 Å**. |
| `docs/MECHANISM_GAP_MAP.md` M5 / ship gate | Freeze 1.16; P72R open | Historical ledger. Current gate **≤ 0.47 Å** AF; P72R closed. |
| `predictions/reports/DIMENSIONALITY_AUDIT.md` | 3-D Cα ~15 Å vs AF 0.4 | **Bulk/orphan observer collapse**, not the product. |
| `predictions/reports/HIGH_RMSD_SYSTEMS.md` | Product median 1.15 Å | Dated diagnosis (fair-cap). Banner added. |
| Field console / MANIFEST | Mixed 0.13 tables + 1.16 pack stamp | Rebuild from current JSON. |

## Intentionally historical (do not overwrite numbers)

| Artifact | Why keep |
|----------|----------|
| `data/alphafold_headtohead.json` | Fair-cap 0.95 H2H (handicap). |
| `data/wetlab_af_eval.json` | Broader medical set, older protocol. |
| `data/medical_stress_suite.json` | Fuse-era 1.16 snapshot. |
| `data/m1_authority_verify.json` | ABL1/BCL2/EGFR M1 experiment. |
| `docs/MECHANISM_GAP_MAP.md` body | Failure-mode ledger; kinase/RBD map. |
| `predictions/reports/*` | Dated reports. Banner points here. |

## Code orientation (current entry points)

| Job | Script |
|-----|--------|
| Freeze H2H | `scripts/bench_product_vs_af.py` |
| AF3 coverage | `scripts/bench_af_coverage.py` + `scripts/multi_system.py` |
| Authority / apparatus | `scripts/run_rcsb_template_holdout.py` |
| Fuse / intact halt | `scripts/msa_template_fuse.py` |
| Bulk F01–F15 | `scripts/fsot_structure_engine.py` |
| Residual / domains | `scripts/full_scalar_law.py` |
| Pin gate | `scripts/verify_cross.py` |

Probe scripts `scripts/_*.py` are **not** product. Do not ship them.

## Claim language

Say: *same-data product, exclude eval PDB, 0 free parameters, residual at named ChemLink, apparatus min over intact collapses. Median 0.13 Å vs AF 0.47.*

Do not say: *de-novo fold beats AlphaFold*, *we recover 0.13 Å from sequence alone*, or *FSOT is 15 Å off* without naming that as the orphan fallback.
