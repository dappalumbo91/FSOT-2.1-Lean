# Cepheid PL — what the interconnects actually are

**Pin:** D1D38A · **no fitted slope or γ**  
**Panel:** `data/cepheid_pl_interconnect_benchmark.json`  
**Refresh:** `python scripts/build_cepheid_pl_benchmark.py`  
**Outcome:** [`../results/cepheid_pl_interconnect_outcome.json`](../results/cepheid_pl_interconnect_outcome.json)

SH0ES treats the period–luminosity relation as a fit (slope, zeropoint, \(Z_W\)). In FSOT it is four folds of the same fluid talking through \(\kappa_{ij}\).

---

## The physical machine (literature)

A classical Cepheid is a yellow supergiant sitting on the instability strip. The engine is the **κ mechanism**:

1. Helium in the envelope ionizes. Opacity rises. Radiation is trapped. The layer expands (**POOF**).
2. Expansion cools and recombines. Opacity drops. The layer falls back (**SUCTION**).
3. There are **two** helium ionization zones (He I and He II). That is why the valve is a pair, not one number.
4. Period follows Ritter’s law \(P\sqrt{\rho}\sim\mathrm{const}\) — a standing acoustic wave in the envelope (T3).
5. Metallicity changes envelope opacity, so the same valve runs at a slightly different luminosity (Chemistry).
6. We do not see the star in a vacuum. Dust reddens the look-path. Wesenheit \(W=I-R(V-I)\) is an **observer** combination (EM).
7. Crowding is extra light in the aperture — T1 look, not stellar structure. SH0ES already showed inner vs outer NGC 4258 intercepts agree to 0.05 mag (their Fig. 8). We do not residual-gate crowding as a star.

Riess+2022 (arXiv:2112.04510): NIR Wesenheit \(m_H^W=m_H-R(m_V-m_I)\), \(R=A_H/(A_V-A_I)\approx0.4\) from extinction laws; metallicity from H II \(R_{23}\) gradients; slope is a global χ² parameter. Optical release note: initial slope **−3.285**. Ripepi+2020 \(W_{VI}\) slope **−3.29±0.01**. Breuval+2022 \(\gamma=-0.239\pm0.069\) mag/dex.

---

## How that maps onto the engine

| Cepheid part | Literature object | FSOT fold | Seed expression |
|--------------|-------------------|-----------|-----------------|
| Period | Ritter / instability strip | Acoustics \(D=10\), T3 | cycle \(\pi\) |
| Expand / contract | κ mechanism | POOF / SUCTION | valve pair |
| Two He zones | He I + He II | glue split | \(\eta_{\mathrm{eff}}/2\) |
| Metals | \(\gamma\) mag/dex | Chemistry \(D=8\) → Astronomy \(D=20\) | \(\gamma=\eta_{\mathrm{eff}}/2\) |
| Wesenheit \(R\) | \(A_I/E(V-I)\) | EM look-path | \(R=1+\pi\cdot\mathrm{SUCTION}\) |
| Crowding | background in the aperture | T1 `observed` | not a stellar row |
| Host distance | LMC / NGC 4258 moduli | Astronomy \(D=20\) | geometric \(\mu\) is *measured* |

\[
|b| = \pi + \tfrac12(\mathrm{POOF}+\mathrm{SUCTION})
\]

\[
\gamma = \eta_{\mathrm{eff}}/2,\qquad
R = 1 + \pi\cdot\mathrm{SUCTION}
\]

The LMC vs NGC 4258 intercept test is the interconnect, not a new H₀:

\[
\Delta\mathrm{int}_{\mathrm{pred}} = (\mu_{\mathrm{LMC}}-\mu_{4258}) + (-\gamma)\,\Delta[\mathrm{O/H}]
\]

Geometric moduli stay literature (Pietrzyński 2019 18.477; Reid 2019 29.397). We do not invent distances.

---

## Live residuals (tight scalars)

| Claim | FSOT | Literature | err |
|-------|-----:|-----------:|----:|
| Optical \|slope\| | 3.29185 | SH0ES release 3.285 | **0.209%** |
| Optical \|slope\| | 3.29185 | Ripepi \(W_{VI}\) 3.29 | **0.056%** |
| LMC − N4258 intercept | −10.877 | R22 table −10.897 | **0.182%** |

Pooled median **0.209%**. GREEN. No fitted \(b\) or \(Z_W\).

## Literature-band (not 0.5% on the central)

| Claim | FSOT | Literature | note |
|-------|-----:|------------|------|
| \(\gamma\) | 0.2335 mag/dex | Breuval 0.239±0.069 | **0.08σ** — 2.3% relative is noise on a ±29% measurement |
| Optical \(R\) | 1.462 | Cardelli class ~1.45 (1.3–1.5) | inside the extinction-law range |

These two are used *inside* the intercept test. Gating them as 0.5% centrals would be pretending Breuval’s ±0.069 is a 0.001-mag/dex number.

---

## What this is not

- Not a claim we re-derived the κ mechanism in Lean.
- Not a NIR Wesenheit panel (primary SH0ES candle is \(W_H\); this table is optical I, V−I).
- Not crowding-as-physics. That stays T1.
- Not a license to fit \(b\) to the 1594 R22 rows.

Kill: tight-scalar median > 0.5%, or anyone least-squares a slope/γ on `data/sh0es_r22_optical_cepheids.dat`.
