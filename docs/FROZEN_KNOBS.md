# No decimal knobs — identities

**Live pin:** AEB2AD. Freeze-era pin D1D38A is historical — [`PIN_LINEAGE.md`](PIN_LINEAGE.md).  
**Peer review:** out of scope.

“Zero free parameters” means the engine is **self-derived**. Assigned decimals (`0.99`, `0.01`, `10`, per-domain `0.85`…) were a drift. They are replaced by seed identities. A miss goes to [`../results/MISSES.md`](../results/MISSES.md). We do **not** put the decimals back to chase a residual.

## What the decimals were

| Knob | Was | Identity |
|------|-----|----------|
| \(K\) polish | \(0.99\) | \(1-\pi^{-4}\) |
| \(C_{\mathrm{eff}}\) polish | \(0.01\) | \(\pi^{-4}\) |
| \(C_{\mathrm{cosm}}\) | \(1/(\varphi\cdot 10)\) | \(1/(\varphi\cdot\pi^2)\) |
| Ledger B \(f_{\mathrm{domain}}\) | 0.0001–0.001 table | \(\alpha=\ln\pi/(e\varphi^{13})\) |
| \(\delta\psi\) table | 0.08, 0.85, 0.95, … | default \(1\); Atomic \(e/\pi\); HEP \(1-\mathrm{POOF}/\pi\) |
| `hits` table | 0–3 | default \(0\); HEP collision \(=1\) |

\(\pi^2\approx 9.87\) was being rounded to \(10\). \(\pi^{-4}\approx 0.01027\) was being rounded to \(0.01\). \(1-\pi^{-4}\approx 0.9897\) was being rounded to \(0.99\).

## \(D_{\mathrm{eff}}\) is derived

Not an integer written on the domain. The 25-D fluid has one nested-orifice chain (micro → macro). Look-splits share a generation \(g\). Then

\[
D_{\mathrm{eff}}(g)=\mathrm{round}\bigl(5\cdot 5^{g/(G-1)}\bigr)
\]

Five seeds → \(D=5\) at \(g=0\). Ceiling \(5^2=25\) at the last generation. You cannot move Chemistry to \(D=9\) to green a file; you would have to change the nest, which is a new edition.

`observed`: medium (dark) vs specimen (look). Ontology of the fold, not a per-row switch. Named law: `_fold_observed` — a core is dark iff it is in `MEDIUM_ORIFICES` (the bulk fluid: Cosmology, QG, Biology, Fluid, Ecology, weather/ocean/crust columns, QC as compute medium, messenger Particle_Astrophysics). Everything else is a counted specimen.

## \(C\) does not enter \(S\)

`DomainConfig.C` is `_fold_C` — a named interpretation label (seed identity of the orifice). It is **not** an input to `compute_scalar`. Compactification is \(D_{\mathrm{eff}}\). Observer channel is look / hits / observed. Do not retune \(C\) to green a residual.

## Species are not a D

Brains sit on the Neuroscience nest (`D=11` this edition). Neuron count \(N\) and volume \(V\) are specimen literature. There is no Human-14 / Honeybee-4 table. Honeybee \(D=4\) was below the particle floor — that was a knob. Density is \(N/(|S_{\mathrm{neuro}}|\cdot V)\).

## Matter budget is the chemistry rung

After the nest, Quantum_Mechanics shares Particle at \(D=5\). \(\Omega_b h^2\) and \(\Omega_c h^2\) are the cosmological *inventory* of atoms, not free orbits. That orifice is Chemistry / Physical_Chemistry (first default-look specimen above the particle floor, \(D=6\)). See [`MATTER_BUDGET_OBJECT.md`](MATTER_BUDGET_OBJECT.md). Do not restore QM to \(D=6\).

## Live nest (this edition)

| \(g\) | \(D_{\mathrm{eff}}\) | Cores |
|------:|---------------------:|-------|
| 0 | 5 | Particle_Physics |
| 1 | 5 | Quantum_Mechanics |
| 2 | 6 | Atomic_Physics, High_Energy_Physics |
| 3 | 6 | Physical_Chemistry, Chemistry |
| 4 | 7 | Electromagnetism, Molecular_Chemistry |
| 5 | 8 | Optics, Acoustics, Materials_Science |
| 6 | 8 | Quantum_Computing, Quantum_Optics |
| 7 | 9 | Biology |
| 8 | 10 | Biochemistry |
| 9 | 11 | Neuroscience, Condensed_Matter |
| 10 | 12 | Thermodynamics, Fluid_Dynamics, Nuclear_Physics, Ecology |
| 11 | 13 | Meteorology, Psychology |
| 12 | 14 | Atmospheric_Physics, Oceanography |
| 13 | 15 | Seismology, Sociology |
| 14 | 16 | Geophysics |
| 15 | 18 | Astronomy, Economics |
| 16 | 19 | Planetary_Science |
| 17 | 21 | Quantum_Gravity |
| 18 | 23 | Particle_Astrophysics, Astrophysics |
| 19 | 25 | Cosmology |

## Extension parent is the name

`maps_to_lean: [particle, …]` is bookkeeping, not a parent. The parent core is the **leading orifice in the name** (earliest match, then longest). Acoustic_Resonance_Materials inherits Acoustics, not Particle. YAML `D_eff` is still ignored.

## Hash gate

`python scripts/audit_parameter_count.py` fails if these identities move without a new pin. Previous pin **D1D38A** held the rounded decimals. **3090BC** held π identities with assigned \(D\). **FE23A2** derived \(D_{\mathrm{eff}}\). **3FBCE5** derived observed/species and the baryon/DM chemistry object. This edition names `_fold_C` (unused by \(S\)). Python, `FSOT.Scalar` (Float), and Lean `FSOT.Formal` Real \(k\) / \(C_{\mathrm{eff}}\) use \(\pi\) identities (\(1-\pi^{-4}\), \(\pi^{-4}\)). `get_domain_params` (Real) follows `DerivedNest` \(D\) and the named look/hits/observed laws. Biology is a dark medium (live \(S<0\)).
