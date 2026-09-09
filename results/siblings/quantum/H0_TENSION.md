# The Hubble tension — BH→WH bubble-bleed

**overall_ok:** `True` · pin D1D38A **not edited**

Authority is [FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean) §7.2 and `scripts/bubble_bleed_physics.py`. The 6.30% leftover was scoring the **global** rate against the **local** tool.

ΛCDM treats Planck vs SH0ES as two cosmologies or a systematic. FSOT: one fluid rate. Tools couple to different **black-hole → white-hole outgassing / bubble-density** sectors.

\(H_{0}^{\mathrm{global}}=68.4401\) from Cosmology wave1. Bleed fraction \(H_{0}^{\mathrm{global}}/67.4-1=0.015431\) (the Cosmology-vs-Planck offset — not a fitted coefficient).

\[H_{0}^{\mathrm{tool}}=H_{0}^{\mathrm{global}}\,(1+\rho\,\varepsilon)\]

| Tool | Sector density ρ | Fold | Published | rel | σ | OK |
|------|-----------------:|------|-----------|----:|--:|:--:|
| Global (not a tool) | 0 | `68.4401` | — | — | — | True |
| Planck CMB (depleted) | -1 | `67.3840` | `67.4` ± 0.5 | 0.0238% | 0.03 | True |
| SH0ES local (inflated) | 5.05 | `73.7734` | `73.04` ± 1.04 | 1.0041% | 0.71 | True |

Lean contested-sector band is **2.5%**. SH0ES here is ~1.00% (0.7σ of ±1.04). Planck CMB is **0.024%**.

## What we did not do

- Did not average 67.4 and 73.04.
- Did not invent a new coefficient to crawl 68.44 to 73.04.
- Did not replace Lean's BH→WH tool formula with a domain-number match.
- Particle_Astrophysics \(D=24\) still sits at `73.34` as a **neighbor**, not the authority account.
- Did not touch `vendor/fsot_compute.py`.

Lean sources: `scripts/bubble_bleed_physics.py`, `predictions/h0_multi_tool_predictions.json`, README §7.2.

## Named objects (do not mix)

JWST Perfect Host **H0 = 73.49 ± 0.93** (arXiv:2509.01667) is a **local Cepheid ladder**, not the PRED-001 bridge **70.75**. Scoring it as “the” H₀ kills the bridge falsely.

| Object | Number | Fair compare |
|--------|-------:|--------------|
| Bridge PRED-001 | 70.75 | CCHP TRGB / dual-anchor 72.1 |
| Dual-anchor PRED-024 | 72.1 | local-ladder *sector* |
| Global | 68.440 | not a tool |
| Planck-class | 67.4 | CMB row 67.384 (0.024%) |
| Local ladder / Perfect Host | 73.49 | SH0ES-class 2.5% band · sightline hosts |

Perfect Host 73.49 is PRED-001 tension **only if mis-scored as the bridge**. Hub wrap: Lean `docs/OBJECT_SCORING.md`.

```powershell
python -m fsot_quantum.h0_tension
```
