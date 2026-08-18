# Why SH0ES is the 1% leftover

**Pin:** D1D38A · **policy:** do **not** retune ρ to hit 73.04  
**Regenerate:** `python scripts/diagnose_sh0es_ladder.py`  
**Machine:** [`../results/sh0es_ladder_diagnosis.json`](../results/sh0es_ladder_diagnosis.json)

This is a diagnosis, not a retune. The 1% class-bin leftover is real. Stuffing SH0ES into the 0.5% green gate by moving ρ from 5.05 → 4.36 is forbidden.

**Filled (2026-08-18):** the published 73.04 is now residual-gated as the information-weighted ladder chain — [`SH0ES_Ladder_Chain`](../data/sh0es_ladder_chain_benchmark.json) · **72.856 vs 73.04 (0.252%)**. Frozen class row stays at 73.773. See [`../results/sh0es_ladder_chain_outcome.json`](../results/sh0es_ladder_chain_outcome.json).

---

## Short answer

SH0ES is not a second cosmology, and we are not missing the Hubble tension.

Planck is **0.024%**. Freedman JWST TRGB is **0.005%**. JAGB/Miras is **0.03%**. Those instruments already sit on the BH→WH sector formula

\[
H_0^{\mathrm{tool}} = H_0^{\mathrm{global}}\,(1 + \rho\,\varepsilon),
\qquad H_0^{\mathrm{global}} = 68.440,\quad \varepsilon = 0.015431.
\]

The leftover is this: we scored the **published SH0ES central** as one **class bin** (ρ = 5.05 → **73.773**) while Riess publishes a **three-rung ladder average** (**73.04**). Those rungs do not all live at ρ = 5.05.

Implied ρ to hit 73.04 exactly: **4.3556**. Assigned class ρ: **5.05**. Overshoot: **0.7334 km/s/Mpc** (1.00%, 0.7σ of SH0ES ±1.04). Inside the **2.5%** contested band on purpose.

---

## What SH0ES is actually looking at

SH0ES is not “the local universe” as one number. It is three rungs averaged into one H₀:

| Rung | What it sees | FSOT already assigns |
|------|----------------|----------------------|
| Geometric anchors | NGC 4258 maser, LMC DEBs, MW parallax | LMC **70.215** · NGC 4258 **70.389** — TRGB/Freedman-like, ρ ~ 1.7 |
| Cepheid PL in SN Ia hosts | Young disk Cepheids in ~20 star-forming galaxies (crowding, metallicity) | **73.47–74.16** — inflated local ladder |
| SN Ia Hubble flow | SNe whose absolute magnitude was *set* by those Cepheids | inherits the host mix |

CMB sees the last-scattering sound horizon (depleted sector ρ = −1).  
Freedman JWST TRGB sees **old** halo/disk tip-of-RGB stars — a different stellar population, different galactic real estate, ρ = 1.85, **0.005%**.  
BAO sees a baryon-acoustic ruler between those walls.

SH0ES sees **young Cepheids in the same galaxies that hosted SN Ia**, then uses those SNe as the Hubble-flow candle. That is a different coupling to the fluid than TRGB or Planck. The sector model already says that. The 1% is not “we forgot Cepheids exist.”

---

## The 1% is a mixture error, not a missing H₀

Per-host sightlines are already computed (`predictions/h0_sightline_predictions.json`, 22 hosts):

| Host | Method | Sector | FSOT H₀ |
|------|--------|--------|--------:|
| LMC | TRGB_anchor | sector_1_local_low | **70.215** |
| NGC4258 | Maser_anchor | sector_3_fsot_document | **70.389** |

Cepheid SN hosts span **73.47–74.16**.

| Readout | FSOT | vs 73.04 |
|---------|-----:|---------:|
| Class bin ρ = 5.05 (what the tool row uses) | **73.773** | **1.00%** |
| Equal-weight host mixture (already on disk) | **73.302** | **0.3593%** |

The published 73.04 sits between the **mild anchors** (~70.3) and the **hot SN hosts** (~73.5–74.2). A single ρ = 5.05 pretends the whole experiment lives in the hottest bin. That is what we are not solving for: **the ladder average is not a single-sector readout.**

Mean error by tool class (25-tool table):

| Class | Mean err % |
|-------|-----------:|
| Early-universe CMB | 0.034 |
| Intermediate ladder (TRGB / JAGB / Carnegie) | 0.529 |
| Local Cepheid ladder (SH0ES family) | 1.087 |

The Cepheid *family* is the outlier cluster (SH0ES HST 1.00%, SH0ES JWST 1.08%, JWST Cepheid Riess 1.18%). Things calibrated *to* that ladder (Pantheon+ SH0ES) inherit it. Freedman TRGB does not.

---

## What we are still not solving for

Filled this pass: ladder mixture, host-local sky, optical+NIR PL, host moduli vs Li+2024 TRGB, N4258 T1 crowding. Still labeled:

1. **Per-host \(H_0=cz/d\)** — not published; peculiar velocities dominate. Host *moduli* are gated.
2. **Full 42-host NIR sample** — this table is the R22 orig-19 release.

---

## What we will not do

| Temptation | Why not |
|------------|---------|
| Set ρ = 4.3556 to hit 73.04 | Forbidden LSQ. That is stuffing SH0ES into the 0.5% gate. |
| Average 67.4 and 73.04 and call it H₀ | Two sectors, one fluid. PRED-001 is the *bridge*, not a third cosmology. |
| Blame “SH0ES is wrong” | 0.73 km/s/Mpc is 0.7σ of ±1.04. The class bin is coarse, not a failed pin. |
| Invent a Cepheid metallicity knob | eta_eff/2 is seed-closed; do not LSQ Z_W on R22. |

---

## Full 25-tool inversion (frozen predictions)

ρ_implied = (H_lit / 68.440 − 1) / 0.015431. Freedman and Planck were placed on that inversion. SH0ES was placed in the “most inflated local ladder” class bin instead.

| Tool | Class | Lit | FSOT | ρ assigned | ρ implied | err % |
|------|-------|----:|-----:|-----------:|----------:|------:|
| planck_cmb_local | early_universe_cmb | 67.40 | 67.384 | -1.00 | -0.98 | 0.024 |
| tdcosmo_conservative | strong_lens_time_delay | 67.40 | 67.437 | -0.95 | -0.98 | 0.055 |
| planck_plus_bao_combo | early_universe_cmb | 67.66 | 67.648 | -0.75 | -0.74 | 0.018 |
| sn_h0_no_local_cal | snia_early_calibrated | 67.80 | 67.806 | -0.60 | -0.61 | 0.009 |
| act_dr6_cmb | early_universe_cmb | 67.90 | 67.859 | -0.55 | -0.51 | 0.060 |
| spt3g_cmb | early_universe_cmb | 68.30 | 68.282 | -0.15 | -0.13 | 0.027 |
| global_cmb_background | fsot_global | 68.44 | 68.440 | 0.00 | 0.00 | 0.000 |
| desi_bao_rs_anchored | bao_intermediate | 68.52 | 68.525 | 0.08 | 0.08 | 0.007 |
| sdss_bao_class | bao_intermediate | 68.60 | 68.598 | 0.15 | 0.15 | 0.002 |
| trgb_ground_class | intermediate_ladder | 69.60 | 70.257 | 1.72 | 1.10 | 0.943 |
| carnegie_h0 | intermediate_ladder | 69.80 | 70.594 | 2.04 | 1.29 | 1.138 |
| wmap9_cmb | early_universe_cmb | 70.00 | 69.971 | 1.45 | 1.48 | 0.041 |
| gw_standard_siren | multi_messenger_siren | 70.00 | 70.024 | 1.50 | 1.48 | 0.035 |
| freedman_jwst | intermediate_ladder | 70.39 | 70.394 | 1.85 | 1.85 | 0.005 |
| h0_bridge_scalar | fsot_bridge | 70.75 | 70.763 | 2.20 | 2.19 | 0.019 |
| jagb_miras_class | intermediate_ladder | 70.90 | 70.922 | 2.35 | 2.33 | 0.031 |
| fsot_document_local | fsot_local_bubble | 72.10 | 71.767 | 3.15 | 3.47 | 0.462 |
| jwst_cepheid_riess | local_ladder_cepheid | 72.60 | 73.457 | 4.75 | 3.94 | 1.180 |
| sh0es_hst_cepheid | local_ladder_cepheid | 73.04 | 73.773 | 5.05 | 4.36 | 1.004 |
| sh0es_jwst | local_ladder_cepheid | 73.04 | 73.826 | 5.10 | 4.36 | 1.076 |
| h0licow_tdcosmo | strong_lens_time_delay | 73.30 | 73.985 | 5.25 | 4.60 | 0.934 |
| surface_brightness_fluctuations | local_ladder_sbf | 73.30 | 74.037 | 5.30 | 4.60 | 1.006 |
| pantheon_plus_shoes_cal | local_ladder_snia | 73.50 | 74.090 | 5.35 | 4.79 | 0.803 |
| megamaser_cosmology | geometric_maser | 73.90 | 74.513 | 5.75 | 5.17 | 0.829 |
| tully_fisher_class | local_ladder_tf | 75.10 | 75.146 | 6.35 | 6.31 | 0.062 |

Kill: if someone changes `predictions/sector_h0_seed.json` ρ for `sh0es_hst_cepheid` to close the 1%, that commit is a policy fail. Score a *mixture* readout in `results/` when we promote the host-mean; do not rewrite the frozen class row.

Related: [`BH_WH_CLAIM_EVIDENCE.md`](BH_WH_CLAIM_EVIDENCE.md) · [`CONCEPTS.md`](CONCEPTS.md) C3 · `predictions/h0_sightline_predictions.json`
