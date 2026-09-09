# Science vs FSOT — named-object compare

*Generated 2026-09-09T18:54:47.576030+00:00 · pin D1D38A*

A literature number is a **named object**. Score it against the named
lock, not a headline. Wrong object = false kill. Do **not** retune
`fsot_predicted`. Do **not** rewrite `predictions/`.

**Refresh:** `python scripts/build_object_compare.py`

How to add the next paper: `python scripts/record_prediction_outcome.py` (see [`OBJECT_SCORING.md`](OBJECT_SCORING.md) and the 2026-08-17 literature pack).

## Standing table

| Paper / survey | Measured | FSOT lock | Map | Verdict | Why | Not |
|----------------|----------|-----------|-----|---------|-----|-----|
| JWST Perfect Host 73.49±0.93 (arXiv:2509.01667) | 73.49 km/s/Mpc | PRED-024 / hosts-only local ladder (73.8019) | `local_ladder` | **hold** | Hosts-only 73.802 vs 73.49 (0.424%). Same Cepheid-ladder sector. | PRED-001 bridge 70.75 |
| SH0ES R22 published 73.04 | 73.04 km/s/Mpc | ladder chain (mixture) (72.8603) | `mixture_chain` | **hold** | Chain 72.860 vs 73.04 (0.246%). Three-rung mixture, not one class bin. | Class bin 73.773 as a 0.5% central; ρ retune 5.05→4.36 |
| SH0ES R22 scored as ρ=5.05 class bin | 73.04 km/s/Mpc | ISO-SHOES-CLASS-BIN (frozen) (73.7734) | `class_bin` | **frozen_isolate** | Class bin 73.773 vs 73.04 (1.00%). Isolated on purpose. Work the chain. | Retuning ρ; stuffing 1% into 0.5% |
| CCHP / Freedman JWST TRGB 70.39 | 70.39 km/s/Mpc | PRED-001 bridge · anchors-only (70.511) | `bridge_or_anchor` | **hold** | Anchors-only 70.511 vs 70.39 (0.172%). Fair bridge compare, not SH0ES 73.04. | Killing PRED-001 on Perfect Host 73.49 |
| A&A 2026 Local Distance Network 73.50±0.81 | 73.5 km/s/Mpc | PRED-024 / hosts-only local ladder (73.8019) | `local_ladder` | **hold** | Same local-high sector as Perfect Host. Hosts-only 73.802 vs 73.50. | PRED-001 70.75 |
| Planck 2018 TTTEEE+lowE+lensing 67.4 | 67.4 km/s/Mpc | Planck-class sector (planck_cmb_local) (67.384) | `cmb_sector` | **hold** | CMB tool row 67.384 vs 67.4 (0.024%). Early-universe depleted sector. | SH0ES 73.04 as the CMB kill |
| DES Y6 S8 = 0.789±0.012 (alone) | 0.789 S8 | PRED-002 / PRED-042 0.805 (0.805) | `tension_row` | **tension_row** | DES-alone is ~2.6σ vs CMB. Not the PRED-002 kill. Fair compare is the joint. | Killing 0.805 on DES-alone |
| Joint DES+CMB+low-z S8 = 0.806 (arXiv:2601.14559) | 0.806 S8 | PRED-002 / PRED-042 0.805 (0.805) | `fair_compare` | **hold** | Joint 0.806 vs lock 0.805 (0.124%). Discriminant is between Planck and DES. | Euclid CLOE FoM as measured S8 |
| Euclid CLOE.3 FoM(w0,wa)>400 (synthetic) | — FoM | PRED-002 / 042 / 043 | `no-map` | **awaiting** | Synthetic figure of merit. Zero survey-level S8/H0/wa. DR1 ~12 Nov 2026. | Citing CLOE as a measured hold |
| DES Y6 + DESI DR2 + CMB wa = −0.63^{+0.21}_{−0.18} | -0.63 w_a | PRED-043 −1.018 (-1.018) | `direction_hold` | **hold_not_kill** | Same sign (evolving DE). ~1.9σ from frozen central. Kill is 3σ Euclid/DESI exclusion. | Claiming 3σ on −1.018; retuning the central |
| CMS 2026 γγ m_H = 125.14±0.15 GeV | 125.14 GeV | PRED-049 125.25 (125.25) | `pdg_mass` | **hold** | |125.25−125.14|/125.25 = 0.088%. Inside 0.5% kill. | A per-channel ε at the LHC |
| Fermilab final Δa_μ ~2.6×10⁻⁹ (WP20 SM) | 2.600e-09 delta_a_mu | PRED-004 / 050 2.49e-9 (2.490e-09) | `same_sign` | **hold** | Same sign and scale vs WP20. Experiment locked. | Retuning after lattice WP25 moved the theory target |
| Muon g−2 Theory Initiative WP25 lattice excess ~0.38×10⁻⁹ | 3.750e-10 delta_a_mu | PRED-004 experimental lock (unchanged) (2.490e-09) | `theory_rebase` | **theory_rebase** | Lattice SM target moved. Logged as theory_rebase, not a retune of the experimental lock. | Rewriting PRED-004 central |
| Genetics product 0.13 Å (sibling freeze 2026-08-17) | 0.13 Å | ChemLink product (sibling-owned) (0.13) | `product` | **sibling_owned** | Product 0.13 Å vs AF 0.47 Å vs cryo-EM FSC ~1.2 Å vs bulk ~13 Å. Do not cross-cite. | Sequence-only 0.13 Å; CASP/FSC papers as the product |
| Riess+2022 Eq.7 R_H = 0.4 | 0.4 R_H | POOF·e·C_eff (0.399561) | `cepheid_wesenheit` | **hold** | NIR Wesenheit is acoustic+chemistry+light, not a fitted b. Residual ~0.110%. | A free Z_W or PL slope |
| FRB IGM 200·(1+sky_density) (~66%) | — pc cm^-3 | PRED-084 orifice (width×fluence vs e·POOF) | `wrong_object_remedied` | **remedied** | IGM path vs orifice puncture. Retired. Repeaters = saloon door; one-shots = paper-rip. | Stuffing DM into 0.5%; dark matter in puncture energy |
| JINR Z=119 run (started May 2026) | — Z | PRED-017 viability | `awaiting` | **awaiting** | No confirmed atom. IUPAC ceiling still 118. | A half-life as a 0.5% central |
| CASP/CAMEO blind protocol (Genetics freeze 2026-08-17) | — Å | product vs AF vs FSC, three columns | `awaiting_protocol` | **awaiting** | Protocol is registered. Blind run is future (Grok Build owns it). Not 0.13 Å from sequence. | Quoting 0.13 Å as sequence-only; cross-citing FSC Å as the product |
| Euclid DR1-Foundation (~12 Nov 2026) | — S8/H0/wa | PRED-002 / 042 / 043 | `awaiting` | **awaiting** | Independent drop. CLOE is synthetic. Do not cite FoM as measured S8/H0/wa. | Euclid CLOE as a hold |
| Path-integral confinement / T3–T4 uniqueness | — theorem | OPEN_NOT_CLAIMED | `open_research` | **awaiting** | Executable probes exist (γ_color, singlets). Continuum YM path-integral uniqueness is not proved. | Pretending Label B uniqueness is a theorem |
| GWTC-5.0 catalog (~390 p_astro≥0.5) | 390 catalog_count | PRED-048 / 067 residual class | `catalog` | **local_green_hold** | Catalog public. Compact-object / GWOSC panels already green. Siren H0 70.024 awaits O4/O5. | Retuning ρ onto SH0ES from one siren |

Counts: {'hold': 9, 'frozen_isolate': 1, 'tension_row': 1, 'awaiting': 5, 'hold_not_kill': 1, 'theory_rebase': 1, 'sibling_owned': 1, 'remedied': 1, 'local_green_hold': 1}. Outcome-log PRED rows (not FCAST): **14**.

## Verdict vocabulary

| Verdict | Meaning |
|---------|---------|
| `hold` | Named object matches the named lock (or sits in the registered band). |
| `hold_not_kill` | Direction agrees; registered 3σ kill has not fired. |
| `tension_row` | Real tension; not the lock's kill object. |
| `frozen_isolate` | Ugly residual kept on purpose (wrong object / class vs mixture). |
| `awaiting` | Catalog/paper not yet measured. |
| `theory_rebase` | Theory target moved; experimental lock unchanged. |
| `sibling_owned` | Genetics/Quantum product, not this hub's remaining work. |
| `remedied` | Wrong apply retired; replacement already gated. |
| `local_green_hold` | In-repo panel already ≤0.5%; survey is a catalog count. |
| `no-map` | Paper number is not the FSOT object (CLOE FoM, sequence-only Å). |

Kill: retuning a frozen central when a paper lands. Kill: scoring Perfect Host
as PRED-001. Kill: DES-alone as PRED-002. Kill: Euclid CLOE as measured.

Related: [`OBJECT_SCORING.md`](OBJECT_SCORING.md) · [`ISOLATED_RESIDUALS.md`](ISOLATED_RESIDUALS.md) ·
[`../results/literature/2026-09-01_prediction_status.md`](../results/literature/2026-09-01_prediction_status.md)
