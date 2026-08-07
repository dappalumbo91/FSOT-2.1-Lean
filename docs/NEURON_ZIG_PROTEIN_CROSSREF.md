# Neuron Zig ↔ protein structure — cross-reference

**Date:** 2026-08-07  
**Pin:** D1D38A  

## Where the working Zig mind lives

| Location | Role |
|----------|------|
| `C:\Users\damia\Desktop\fsot neuron family\fsot-neuron-zig\` | **Working FSOT neuron implementation (Zig)** |
| GitHub | `dappalumbo91/fsot-neuron-zig` (when synced) |
| Archive notes | `I:\FSOT-Physical-Archive\` + monorepo `docs/NEURON_ZIG_TO_OS_ROADMAP.md` |

**Doctrine (from Zig docs):** one scalar law \(S=K(T_1+T_2+T_3)\); Zig is **embodiment**, not a second theory. Language (Zig vs Rust vs Python) is secondary — **binary parity of seeds + pair laws** is primary.

## Laws to reuse for protein / AlphaFold track

### 1. Scalar (authority twin)

`fsot-neuron-zig/src/scalar.zig` — same `computeScalar` as `vendor/fsot_compute.py`:

- \(T_1\): growth, base, \(1+P_{\mathrm{new}}\ln(D/25)\), observer quirk  
- \(T_3\): chaos \((D-25)/25\), POOF/SUCTION, bleed  
- Clamp product through \(K\)

### 2. Genetic pair geometry (same seeds as protein F07/F08)

`genetic.zig` / `genetic_fixed.zig`:

```text
geometricScaleDist(dist) = φ · dist^(-1/π)     // collapsed-globule scale
electrostaticTerm(qi,qj) = -qi·qj·e
env(s) = s / (s + π·e)                       // same F08 contact envelope
fsotPairWeight = geom · (base + 0.15·elec) · (0.35 + 0.65·env)
```

Protein **F07** in archive is `bb(s) = s^(-1/π)` (proximity).  
Neuron geometric scale is **φ · bb(s)**. Inverse for distance embedding:

```text
if proximity M ≈ s^(-1/π), then s ≈ M^(-π), d ≈ CA_CA · s^(1/π) = CA_CA / M
```

### 3. Genetics as trinary code

`codon.zig`, `genotype_fixed.zig`, docs `GENETICS_AS_TRINARY_CODE.md` — same trinary spine as `fsot_protein` F01.

### 4. All-atom MD is lab, not the fold runtime

`docs/WHY_NOT_ALL_ATOM_MD.md` + `allatom_md.zig`:

- MD = offline structural lab  
- Online structure path = **seed pair laws + fixed lattice process**, not femtosecond MD as the main engine  

Matches protein doctrine: **F15 distogram first**, coordinates second — not classical all-atom MD as the claim path.

### 5. Molecular cascade (spine chemistry)

`molecular_fixed.zig` — process scale after structure, not a substitute for sequence→fold.

## Protein structure authority split

| Layer | Authority source |
|-------|------------------|
| F01–F15 distogram / SS / chemistry / regions | `Genetics/fsot_protein` (Rust) + `FSOT_PROTEIN_DERIVATIONS.md` |
| Seed constants / scalar / pair geometry style | **`fsot-neuron-zig`** (`seeds.zig`, `scalar.zig`, `genetic.zig`) |
| Residual packs (UniProt, AF meta) | Lean monorepo `fsot_api_predict_lib` |
| Cα embedding from distogram | Monorepo `fsot_structure_engine.py` (must invert F07 like neuron geom) |

## Practical rule for this monorepo

1. **Do not invent** Chou-Fasman tables or free MD coefficients.  
2. **Do** port `fsot_protein` F15 matrix exactly.  
3. **Do** use neuron Zig **geometricScaleDist / env** pattern when turning proximity → Å.  
4. Optional later: Zig CLI twin of distogram for binary parity with Python.

## Paths checked on this machine

```
C:\Users\damia\Desktop\fsot neuron family\fsot-neuron-zig\
I:\FSOT-Physical-Archive\04_Genetics-Longevity\fsot_protein\
C:\Users\damia\Desktop\Genetics\fsot_protein\
```
