# H₀ direction — priors, not a second law

**Live pin:** AEB2AD. **Freeze pin:** D1D38A. Frozen prediction JSON is not rewritten from this page.

## What is pinned

Global H₀ **68.44** is the wave-1 readout. Lean checks `h0_fsot_cached_approx_value` and the acoustic bleed bounds `acoustic_bleed_div_inflow_gt_62600` and `_lt_62961`. Those checks do not cover sky sectors, density seeds, or the host coupling.

## Assigned priors

These numbers are not derived from π, e, φ, γ, or Catalan's G. Reviewers should treat them as priors.

| Prior | Value | Role |
|-------|------:|------|
| ε | H₀_global / 67.4 − 1 = 0.015431 | Bleed fraction. The 67.4 anchor is Planck 2018, not a seed. |
| Cepheid class density | 5.1 | SH0ES-class sightline seed in `sector_h0_seed.json` |
| TRGB density | 1.85 | Freedman-class anchor |
| Maser density | 2.0 | Geometric anchor |
| Planck sector density | −1 | Early-universe depleted class |

The host formula stays `H0_host = H0_global * (1 + density_model * ε)`. Changing a prior would move the frozen host table. That table stays.

## Directional rule — exploratory

Until the next data drop freezes the choices below, the directional rule is exploratory. It lives in scripts. It is not in `vendor/fsot_compute.py` and not in Lean.

| Choice | Status now |
|--------|------------|
| Which rows get a direction | Host galaxies only. Hubble-flow supernovae inherit the host mix and have no direction rule. |
| Density catalog | `data/extragalactic_structure_catalog.json` (nearby cluster centers). The 20-row nebula cache is a lensing seed: 19 of those nebulae are in the Milky Way. It is not the H₀ direction catalog. |
| Line-of-sight structure | Not entered. |
| FRB positions | The live cache has 3390 rows, 3352 with no RA and none with a Dec. Those rows are dropped. Missing position is not (0°, 0°). |

## Null for supernova samples

Pantheon+SH0ES Hubble-flow supernovae (238) show no significant directional H₀ pattern. Every half-sky split is under 2σ. A full-sky dipole fit is 0.87% ± 0.61%, consistent with no dipole. That is the explicit null for the Rubin and Euclid supernova samples. Record: `results/exploratory/pantheon_shoes_directional_null.json`.

## Locks that match ΛCDM

N_eff **3.046** equals the Standard Model / Planck best-fit value. Tag: **matches ΛCDM, not discriminating.** The same tag applies to any other T5 lock that is copied from a Planck or Standard Model central.

## Frozen host coordinates

Six frozen host positions disagree with SIMBAD. The frozen file is left as hashed. The live catalog `data/sh0es_host_coordinates.json` carries the SIMBAD positions. Only UGC 9391 changes sector under the old sky bins (RA 175.6° → 218.7°, sector 2 → sector 3), which would read 73.497 instead of 73.470 on that old density map. The frozen number 73.470 stays in the frozen file. Log: `results/host_coordinate_audit.json`.
