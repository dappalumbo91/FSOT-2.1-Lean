# How to apply FSOT in any domain

This is the **trial-and-error** protocol. It is not a free-parameter hunt.

Authority: pin **D1D38A** · [`FSOT_MATH_KEY.md`](FSOT_MATH_KEY.md) §4–5 · [`FSOT_PROPER_DENSIFY_POLICY.md`](FSOT_PROPER_DENSIFY_POLICY.md) · [`TOE_CLAIM_BOUNDARIES.md`](TOE_CLAIM_BOUNDARIES.md)

---

## Two laws (do not mix)

**Ledger A predict** (no measured in the formula):

```text
python scripts/predict_closed_form.py --observable T_CMB
```

**Ledger B correct** (catalog residual, not a ToE headline):

\[
\texttt{computed} = \texttt{measured}\cdot\bigl(1 + |S(\mathrm{domain})|\cdot f_{\mathrm{domain}}\bigr)
\]

Call it `fsot_correct(m, domain)`, not predict. \(S = K(T_1+T_2+T_3)\) at a **frozen** \((D_{\mathrm{eff}}, h, \delta\psi, \delta\theta, \mathrm{observed})\). Changing those integers is a new pin.

---

## Steps (do them in order)

| Step | Do this | Do **not** do this |
|------|---------|---------------------|
| 1 | Name a **measured** \(m\) with public/lab provenance | Invent “measured × 0.999” |
| 2 | Pick the **dimensional interface** (scale of the substance) | Invent a new \(D_{\mathrm{eff}}\) to fit one row |
| 3 | `S = domain_scalar(name)` from the pin | Add a spring constant / Yukawa / dark density |
| 4 | `computed, err% = fsot_correct(m, name)` (Ledger B) | Least-squares a new \(f\); calling this a prediction |
| 5 | Green if domain **median** residual ≤ **0.5%** | Call HTTP 200 a residual |
| 6 | If it fails: log in `results/MISSES.md`. Do **not** edit \(D_{\mathrm{eff}}\) as a repair | Add a free parameter; change DomainConfig integers under the same pin |

Worked examples in-repo:

- Catalog fold: MPCORB eccentricity failed ~62% on the wrong fold; Planetary_Science \(D=21\) brought the panel to **~0.023%**. Log: [`MPCORB_REFINEMENT_PROCESS.md`](MPCORB_REFINEMENT_PROCESS.md).
- Wave fold: [`APPLY_SEISMOLOGY.md`](APPLY_SEISMOLOGY.md) — PREM / \(b\)-value / dated cells. Neighbor Geophysics \(D=19\).
- Light fold: [`APPLY_OPTICS.md`](APPLY_OPTICS.md) — CRC \(n_D\) wave vs photon. Neighbor Quantum_Optics \(D=11\).
- Bulk fold: [`APPLY_MATERIALS.md`](APPLY_MATERIALS.md) — CRC density. Same rung as Optics; look-split vs PhysChem/Chem.
- Lab-sound fold: [`APPLY_ACOUSTICS.md`](APPLY_ACOUSTICS.md) — CRC \(c\); PREM \(v_P/v_S\). Neighbor Seismology \(D=18\).
- Quantum-to-atom fold: [`APPLY_ATOMIC.md`](APPLY_ATOMIC.md) — NIST hydrogen \(a_0\)/\(R_\infty\); H–Ca ionization. Neighbor Quantum_Mechanics \(D=6\).
- EM fold: [`APPLY_EM.md`](APPLY_EM.md) — CRC \(n_D\) and Maxwell \(n^2\). Neighbor Optics \(D=10\).
- Chemistry ladder: [`APPLY_CHEMISTRY.md`](APPLY_CHEMISTRY.md) — CRC MW / \(T_m\) / \(T_b\) / density. Chemistry \(D=8\), Physical_Chemistry \(D=8\), Molecular_Chemistry \(D=9\).
- Biology fold: [`APPLY_BIO.md`](APPLY_BIO.md) — NCBI mt-operon / AA MW. Neighbor Biochemistry \(D=13\). Dark: do not flip `observed`.
- Signaling fold: [`APPLY_NEURO.md`](APPLY_NEURO.md) — CRC transmitter AA. Neighbor Biochemistry \(D=13\); not Psychology watts.
- Hilbert fold: [`APPLY_QC.md`](APPLY_QC.md) — CRC \(n_D\). Neighbor Optics / QO. Dark: do not flip `observed`.
- Tank fold: [`APPLY_FLUID.md`](APPLY_FLUID.md) — NDBC neighborhood; \(\gamma=1.400\); \(e+\varphi\). Dark: do not flip `observed`.
- Orifice fold: [`APPLY_NUCLEAR.md`](APPLY_NUCLEAR.md) — IAEA/ENDF keV. Neighbor Particle \(D=5\).
- Heat fold: [`APPLY_THERMO.md`](APPLY_THERMO.md) — Carnot COP; fridge vs Cosmology \(\pi/2\).
- Habitat fold: [`APPLY_ECOLOGY.md`](APPLY_ECOLOGY.md) — GBIF latitude. Dark: do not invent watts.
- Psychometric fold: [`APPLY_PSYCHOLOGY.md`](APPLY_PSYCHOLOGY.md) — Nunnally/Cohen anchors. Not watts; not OpenAlex citations.
- Sky fold: [`APPLY_ASTRONOMY.md`](APPLY_ASTRONOMY.md) — JPL densities; H0 sectors. Neighbor Planetary \(D=21\).
- How to read a row: [`SCIENTIST_INTERFACE.md`](SCIENTIST_INTERFACE.md).
- Using this as a tool (not a silo): [`SCIENTIFIC_INSTRUMENT.md`](SCIENTIFIC_INSTRUMENT.md).
- HEP fold: [`APPLY_HEP.md`](APPLY_HEP.md) — CODATA \(m_e\)/\(m_p\). Neighbor Atomic \(D=7\).

---

## Allowed densify

| Method | `computed` | `measured` |
|--------|------------|------------|
| Seed closed formula | `evaluate_formula(...)` | NIST / PDG / lab |
| Domain scalar route | `m × (1 + \|S\| · f)` | real anchor |
| Engine closed form | seed expression | PDG / survey |

## Forbidden

- Identity pads (`φ = φ` as a record)
- Process gates as empirical depth
- Copying another domain’s error without recompute
- Literature identity (`measured = computed = published`) as padding

---

## Kill criteria (do not negotiate mid-work)

| Layer | Kill |
|-------|------|
| Domain panel | Pooled median > **0.5%** on refresh |
| Global empirical | If **>25%** of extension domains fail that gate on the next full refresh — `data/falsification_registry_closure.json` |
| Tool-row prediction | Registered `kill_if` / discriminant in `predictions/` |
| Label A | A1–A6 in `TOE_CLAIM_BOUNDARIES.md` |
| Label B | T1–T6 — more domains alone do **not** complete B |

When a paper lands, log it in **`results/`**. Do not rewrite the frozen prediction.

---

## Paradigm note

Standard siloed formulas are a **reference readout**, like Newton inside relativity. They are not the directory we are walking. If biology and cosmology “do not talk,” that is an institutional cut. The engine still has one \(\kappa_{ij}\) between tanks.

---

## Commands

```powershell
python scripts/audit_all_benchmark_margins.py
python scripts/remediate_false_densify.py
python scripts/remediate_green_fail_panels.py
```
