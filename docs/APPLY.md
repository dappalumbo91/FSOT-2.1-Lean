# How to apply FSOT in any domain

This is the **trial-and-error** protocol. It is not a free-parameter hunt.

Authority: pin **D1D38A** · [`FSOT_MATH_KEY.md`](FSOT_MATH_KEY.md) §4–5 · [`FSOT_PROPER_DENSIFY_POLICY.md`](FSOT_PROPER_DENSIFY_POLICY.md) · [`TOE_CLAIM_BOUNDARIES.md`](TOE_CLAIM_BOUNDARIES.md)

---

## The only prediction law

\[
\texttt{computed} = \texttt{measured}\cdot\bigl(1 + |S(\mathrm{domain})|\cdot f_{\mathrm{domain}}\bigr)
\]

\(S = K(T_1+T_2+T_3)\) at a **preregistered** \((D_{\mathrm{eff}}, h, \delta\psi, \delta\theta, \mathrm{observed})\).

---

## Steps (do them in order)

| Step | Do this | Do **not** do this |
|------|---------|---------------------|
| 1 | Name a **measured** \(m\) with public/lab provenance | Invent “measured × 0.999” |
| 2 | Pick the **dimensional interface** (scale of the substance) | Invent a new \(D_{\mathrm{eff}}\) to fit one row |
| 3 | `S = domain_scalar(name)` from the pin | Add a spring constant / Yukawa / dark density |
| 4 | `computed, err% = fsot_scaled(m, name)` | Least-squares a new \(f\) |
| 5 | Green if domain **median** residual ≤ **0.5%** | Call HTTP 200 a residual |
| 6 | If it fails: **change the interface** (wrong fold) | Add a free parameter |

Worked example already in-repo: MPCORB eccentricity failed ~62% on the wrong fold; Planetary_Science \(D=21\) brought the panel to **~0.023%**. Log: `docs/MPCORB_REFINEMENT_PROCESS.md`.

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
