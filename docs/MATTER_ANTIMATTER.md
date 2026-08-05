# Matter / antimatter under FSOT fluid spacetime

**Module:** `vendor/fsot_matter_antimatter.py`  
**Benchmark:** `data/matter_antimatter_benchmark.json`  
**Research:** `data/matter_antimatter_research.json`  
**Builder:** `python scripts/build_matter_antimatter_benchmark.py`

---

## Why this was missing

The residual atlas already gated **ordinary particle masses** (PDG) and **cosmology densities**, and the seed engine already contained:

| Quantity | Formula (already in `fsot_compute`) | Anchor class |
|----------|-------------------------------------|--------------|
| \(\eta = n_b/n_\gamma\) | \(\mathrm{Poof}^{11}/(\pi\gamma)\) | Planck ~\(6.14\times10^{-10}\) |
| \(\Omega_b h^2\) | \(\|S_{\mathrm{cosmo}}\|\cdot(1-S_{\mathrm{quant}})\) | Planck ~0.02237 |

What was **not** explicit: a dedicated **matter–antimatter domain panel**, conjugate duals, CPT mass equality, pair thresholds, and bulk antimatter damping as **reality-syntax** under the same fluid.

---

## FSOT ontology (apply the model)

| Concept | FSOT reading |
|---------|----------------|
| **Matter** | Emergence-class vortices of the fluid at particle / nuclear interfaces (\(S>0\)) |
| **Antimatter** | Charge-conjugate dual of the **same** continuum mode (\(\delta\psi\to\delta\psi+\pi\)), not a second free Lagrangian |
| **CPT mass equality** | Structural: \(m=\bar m\) for the dual of one mode |
| **Pair production** | Threshold \(2m\) identity (energy to open both duals) |
| **Baryon asymmetry \(\eta\)** | Seed-closed residual; explains scarcity of bulk antimatter |
| **Late universe** | Cosmology \(S_{\mathrm{cosmo}}<0\) damps bulk antimatter residual density while matter remains load-bearing |

**Not claimed:** full continuum Sakharov path-integral baryogenesis uniqueness theorem.  
**Claimed:** executable residual + dynamics duals under pin D1D38A fluid omni-theory.

---

## Dual channels (emergence syntax)

On `Particle_Physics` (\(D_{\mathrm{eff}}=5\)):

- **Matter route:** standard `domain_scalar` → \(S_m > 0\) (emergence)  
- **Conjugate route:** \(\delta\psi+\pi\) → \(S_{\mathrm{conj}}\) distinct from \(S_m\)  
- **Preference:** \(A=(S_m-S_{\mathrm{conj}})/(|S_m|+|S_{\mathrm{conj}}|)>0\)  
- **Cosmology:** \(S_{\mathrm{cosmo}}<0\) + \(\eta\ll 1\) ⇒ bulk antimatter non-load-bearing  

This is the same emerge/damp syntax as the hierarchical building-block audit.

---

## Hierarchy attachment

```
L0 seeds → POOF, π, γ, …
L4 S
L5 Particle (D=5) matter duals + Nuclear emergence
L5 Cosmology (D=25) damps bulk antimatter residual
L6 residual η, Ω_b h², CPT identities
```

Strings: shared fluid + conjugate phase; not a separate antimatter universe.

---

## Commands

```powershell
python scripts/build_matter_antimatter_benchmark.py
python scripts/audit_all_benchmark_margins.py   # after panel is in data/
```

Optional multiprover export can follow the uniqueness-research spine pattern once residuals are green in the margin audit.

---

## Claim language

| Allowed | Forbidden |
|---------|-----------|
| Seed \(\eta\) residual-gates Planck class | “Sakharov theorem proved in Coq” |
| CPT \(m=\bar m\) structural | “Antimatter needs free parameters” |
| Conjugate dual distinct; bulk antimatter damped | “Matter and antimatter are unrelated Lagrangians” |
| Matter = fluid vortices (emergence) | Absolute rest frame required |
