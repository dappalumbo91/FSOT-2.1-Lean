### 3.1 The heartbeat (numbered)

At the center of FSOT is one scalar decomposition evaluated at seed-derived constants:

**(Eq. III.1)** — vitality scalar:

```
raw_S = term1 + term2 + term3
```

**(Eq. III.2)** — primary wave term with observer coupling:

```
term1 = (main_wave(N, P, D_eff)) × quirk_mod(observed, δψ, phase_variance, consciousness_factor)
```

**(Eq. III.3)** — environment and chaotic bleed:

```
term2 = baseline_trend(environment) + amplitude(environment)
term3 = chaotic_bleed(small_scale_turbulence)
```

In words:

- **Main wave term** — resonance at scale (size N, power P, effective dimension D_eff)
- **quirk_mod** — observer coupling: when `observed = true`, measurement modulates the wave
- **term2** — baseline trend and amplitude (environment)
- **term3** — chaotic bleed: small-scale turbulence from the fluid

Formal definitions: `FSOT/Scalar.lean`, `FSOT/Formal/Scalar.lean`, decimal authority `vendor/fsot_compute.py`.
