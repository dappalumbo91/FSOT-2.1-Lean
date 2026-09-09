# FSOT Protein Formula Derivations — Zero-Free-Parameter Reference

**Status:** v7 (post free-parameter elimination, 2026-05-12).
**Build:** `cargo run -p fsot_protein --bin benchmark` (WSL Ubuntu, Smart App Control blocks native).
**Canon source:** `Genetics/fsot_core/src/lib.rs` (mirrors `FSOT NeuroLab/fsot_compute.py`).

Every coefficient below reduces to a closed form in the FSOT seeds **{π, e, φ, γ}** or to one of the FSOT-derived scalars (`P_NEW`, `C_EFF`, `ETA_EFF`, `S_biochem`, `S_molchem`). No free parameters.

---

## Canonical constants

| Symbol | Definition | Numerical value |
|---|---|---|
| `π` | FSOT seed | 3.14159265358979 |
| `e` | FSOT seed | 2.71828182845905 |
| `φ` | FSOT seed = (1+√5)/2 | 1.61803398874989 |
| `γ` | FSOT seed (Euler–Mascheroni) | 0.57721566490153 |
| `P_NEW` | (γ/e)·√2 | ≈ 0.30033 |
| `C_EFF` | (1 − POOF·sin θ_S)·(1 + 0.01·G_CAT/(π·φ)) | ≈ 1.00097 |
| `ETA_EFF` | 1/(π − 1) | ≈ 0.46694 |
| `S_biochem` | `domain_scalar("Biochemistry", D=13, δψ=0.1)` | (FSOT engine output) |
| `S_molchem` | `domain_scalar("Molecular_Chemistry", D=9, δψ=0.4)` | (FSOT engine output) |

---

## F01 — Amino-acid trinary phase
20 AAs → balanced-ternary signature `(c, p, v) ∈ {-1,0,+1}³` representing (charge, polarity, volume). Single source of truth in `secondary::trinary_phase`. Five large-nonpolar AAs (I,L,M,F,W) share `[0,-1,+1]`; discrimination must come from downstream geometric layers, not from re-encoding F01.

## F02 — AA chemical scalars (REFINED v7)
Derived purely from `trinary_phase`:

$$
h(\text{AA}) = \varphi^{-p}\, e^{v/\pi}\qquad
V(\text{AA}) = \pi\,e\,\varphi^{v}\qquad
q(\text{AA}) = c\qquad
\mu(\text{AA}) = \gamma\,e^{|c|+p+1}
$$

- Pivot: `(p=0, v=0) → h = 1` (FSOT neutral).
- Large nonpolar h = φ·e^{1/π} ≈ 2.218; small nonpolar = φ·e^{−1/π} ≈ 1.181.
- All polar AAs (T,S,Y,N,Q) collapse to `h = e^{v/π}/φ`. **By design** — partner discrimination at long range must come from geometry (F17), not from this layer.
- Eliminated 16 magic decimals from v6 lookup table.

## F03 — Disulfide bridge
`fsot_chemical_interaction(C,C) = φ⁶ ≈ 17.94`. Dominant covalent force in the field.
- Gate (pending F18): sequence-separation envelope to suppress sterically forbidden short loops.

## F04 — Hydrophobic interaction (REFINED v7)

$$
h_\text{term} = \frac{h_1-1}{\varphi}\cdot\frac{h_2-1}{\varphi}
$$

Centered at the FSOT pivot 1.0 (was φ in v6 — wrong centering caused W-W to exceed disulfide).

## F05 — Electrostatic interaction
$\text{elec} = -q_1 q_2\, e$ with charges in `{-1, -½, 0, +½, +1}`. Max magnitude ≈ e for K↔D.

## F06 — Dipole interaction
$\text{dip} = \sqrt{\mu_1\mu_2}/(\gamma\pi e^2)$. Always attractive (orientation not modeled). Weakest term.

## F07 — Backbone proximity (REFINED v7)

$$
\text{bb}(s) = \frac{1}{s^{1/\pi}}
$$

The exponent 1/π ≈ 0.318 is the FSOT-derived collapsed-globule scaling, replacing the Flory ½ (theta-solvent random walk — wrong physics for folded proteins).

## F08 — Chemistry envelope
$\text{env}(s) = s/(s + \pi e)$. Crossover at s = πe ≈ 8.54 (FSOT contact scale).

## F09 — Chemistry / region amplitudes (REFINED v7)

$$
\text{chem\_amp} = |S_\text{molchem}| \cdot P_\text{NEW}\qquad
\text{region\_amp} = |S_\text{biochem}| \cdot P_\text{NEW} \cdot C_\text{EFF}
$$

`.max()` guards removed — amplitudes are fully deterministic.

## F10 — Helix periodicity bonus
For `sep ∈ {3,4,7}`: $\text{bonus} = (\sqrt{p^\alpha_i p^\alpha_j})^3 / e$. Cube = trinary triad self-attenuation.

## F11 — Sheet pair bonus
For `sep ≥ 3`: $\text{bonus} = \sqrt{p^\beta_i p^\beta_j}^2 \cdot \frac{1}{1 + \max(\ln(s/\pi), 0)} / \varphi$.

## F12 — Region detection (trinary triadic collapse)
Collapse residue → {H, E, C} using gate `p_dominant > 1/e` (uniform prior + 1 nat). Minimum run length 3 = 3¹ (smallest trinary triad). Yields contiguous regions for F13.

### F12c candidate — expanded topology + cooperative backbone

Development-only candidate; production F15 remains on baseline F12 until a
frozen external validation is recorded.

The expanded trinary syntax contributes side-chain topology to beta propensity:

$$
x_\beta = \max(b,0)+|a|+|h|/\varphi,
\qquad
p_\beta^\mathrm{raw}=e^{(v-p+x_\beta)/\pi}
$$

where $b$, $a$, and $h$ are branch, aromatic, and heteroatom trits. A three-state
Viterbi collapse models cooperative backbone hydrogen bonding by multiplying a
same-state transition by $\varphi^{1/\varphi}$. The factor is seed-derived and
not fitted per amino acid. Minimum helix and strand lengths remain 4 and 3.

The disclosed development family used continuity exponents
$\{1/\pi,1/\varphi,1,\varphi\}$; $1/\varphi$ maximized mean per-protein H/E/C
macro recall while retaining nonzero beta recall on every beta-containing
development protein.

## F13 — Region-pair contact (long-range coupling)
For same-kind regions, different regions, `sep ≥ ⌈η_eff·D_biochem⌉ = ⌈0.467·13⌉ = 7`:

$$
\text{bonus} = \sqrt{p_i p_j}\cdot \max(0, \ln\sqrt{L_i L_j})\cdot \text{region\_amp}
$$

**Missing register information — see F16/F17 below.**

## F14 — Long-range gate
`⌈η_eff · D_biochem⌉ = 7`. The minimum sequence separation for cross-region coupling.

## F15 — Distogram assembly
$M_{ij} = \text{bb}(s) + \text{chem}\cdot\text{env}\cdot\text{chem\_amp} + \text{helix} + \text{sheet} + \text{region\_pair}$

---

## Proposed additions (open work)

### F16 — Heptad register (helix-helix)
Helix packing is heptad-periodic: positions `k mod 7 ∈ {0, 3}` (a, d) face the partner.
Proposed multiplier in F13 when `kind = H`:

$$
r_\text{heptad}(i, j) = \begin{cases} \varphi & (i \bmod 7, j \bmod 7) \in \{0,3\}^2\\ 1/\varphi & \text{otherwise}\end{cases}
$$

Closed-form. Expected to push 1ENH LR from 7.41% upward.

### F17 — Strand register (β-pair direction)
For two β-regions A=[s_A,e_A], B=[s_B,e_B], score both registers and take the max:

- **Antiparallel:** ideal partner of `i` is `j* = e_B - (i - s_A)`.
- **Parallel:** ideal partner of `i` is `j* = s_B + (i - s_A)`.

Multiplier: $\varphi^{-|j - j^*|/\pi}$ (decays in 1/π per register offset).

Expected to push 2GB1 LR from 7.14% upward. Also expected to lift 1UBQ LR (β1-β5 pairing).

### F18 — Disulfide geometry gate
Modulate F03 by a separation envelope:

$$
\text{gate}(s) = \exp(-(s - \pi e)^2 / (\pi e \cdot \varphi))
$$

Peaks at the canonical CASP contact separation, suppresses sterically forbidden short loops.

### F19 — Oriented backbone handedness

A symmetric distance matrix determines coordinates only up to reflection. For
four consecutive C-alpha positions in a predicted helix, define the normalized
signed volume

$$
\chi_i =
\frac{((b_i \times b_{i+1}) \cdot b_{i+2})}
{\lVert b_i\rVert\lVert b_{i+1}\rVert\lVert b_{i+2}\rVert},
\qquad b_i = x_{i+1}-x_i.
$$

The L-amino-acid alpha-helix convention selects the enantiomer with
$\sum_i \chi_i \ge 0$. If the sum is negative, reflect one coordinate axis.
This operation preserves every pair distance and therefore introduces no
interaction magnitude, threshold, or fitted coefficient. The Python runtime
exposes F19 as the development-only `canonicalize_chirality` option pending a
fresh coordinate holdout.

---

## v7 benchmark (5 proteins, zero free parameters)

| Protein | Fold | Pearson | Spearman | Top-L | LR (|i−j|≥6, top L/2) |
|---|---|---|---|---|---|
| 1UBQ | α/β (76 AA) | 62.69% | 36.18% | 98.68% | 7.89% |
| 1CRN | S-S (46 AA) | 62.18% | 45.67% | 80.43% | **30.43%** |
| 1VII | all-α (36 AA) | **83.83%** | **65.26%** | **100%** | 11.11% |
| 2GB1 | α+β (56 AA) | 62.14% | 28.04% | **100%** | 7.14% |
| 1ENH | 3-α bundle (54 AA) | 78.57% | 48.24% | **100%** | 7.41% |

vs v6 (pre-refactor): Pearson +4 to +19 points on every protein; Top-L hit 100% on 3/5; 1CRN long-range jumped 21.74% → 30.43%.

---

## Lessons captured (for future memory)

1. **Centering matters.** F04 used to center hydrophobicity on φ; that's a free choice. Centering on 1.0 (the natural pivot of `h = φ^{-p}·e^{v/π}` at p=0, v=0) is the only zero-free-parameter option.
2. **Magic decimals hide as physics.** The 16 multipliers in v6's AA table (1.1, 1.2, 1.4, 1.7, 1.8, 2.0) looked physical but were free parameters that happened to mask the lack of geometric register layers. Removing them exposed the real gap (F17).
3. **Flory ½ is wrong for folded proteins.** It models theta-solvent random walks. Collapsed globules want ν ≈ 1/3; the FSOT-native closest closed form is 1/π.
4. **`.max(constant)` guards are free parameters.** Even `.max(0.01)` injects a discontinuity that won't pass audit. Prove the raw expression is positive instead.
5. **Trinary collapse is a feature, not a bug.** Five large-nonpolar AAs sharing one signature means downstream layers must do geometric discrimination — that's what F16/F17 are for.
