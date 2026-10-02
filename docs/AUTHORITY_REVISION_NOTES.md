# Authority revision notes

These notes are for the next time the authority file is deliberately re-pinned.
`vendor/fsot_compute.py` is unchanged. Pin **AEB2AD**. Nothing below is a value edit.

`full_report()` prints 343 constants with targets and 342 within 5%. Read that 342 as two groups:

| Group | Within 5% | Outside 5% |
|-------|----------:|-----------:|
| Identity or definition | 8 | 0 |
| Seed-derived | 334 | 1 |
| Total | 342 | 1 |

The row outside 5% is `Gluon_condensate` (`C_cosm − e⁻³`), about 6.94%.

`DNA_base_pair` is one of the 334 seed-derived rows and uses a measured input. See B-02.

## B-01 · Identity or definition rows

The computed side is the target literal, or a known exact rational. These rows are inside the 342. They are not seed-derived predictions.

| Row | Line | What the file stores |
|-----|-----:|----------------------|
| `Proton_radius` | 418 | formula `"exact"`, `mpf("0.8413")` against `mpf("0.8413")` |
| `STDP_Tau_Plus_ms` | 924 | `mpf(20)` against `mpf(20)` |
| `STDP_Tau_Minus_ms` | 925 | `mpf(20)` against `mpf(20)` |
| `Metatron_Spheres` | 881 | `mpf(13)` against `mpf(13)` |
| `Metatron_Pathways` | 882 | `mpf(27)` against `mpf(27)`, formula `3³=27` |
| `Max_Trits` | 977 | `mpf(27)` against `mpf(27)`, formula `3³` |
| `Potts3_beta` | 754 | `mpf(1)/9` against `mpf("0.11111")`. 1/9 is the exact 2-D 3-state Potts exponent. The target is the five-digit literal. |
| `Quark_condensate` | 757 | `mpf(1)/4` against `mpf("0.250")` |

Other rows land on their target because a seed expression evaluates to that integer or short decimal (`floor(2π)` against 6, `(25/25)^0.2` against 1, `φ + 1/φ²` against 2). Those stay in the 334. The computed side is an expression, not a copy of the target literal.

## B-02 · Measured input

Line 398 sets `a0 = mpf("0.529177")`, commented as the Bohr radius in angstroms. Line 412 uses it:

`DNA_base_pair`: `v = 2*PI*a0*(1 + GAMMA/(PI**2 * E))` against `mpf("3.4")`.

Mark this row **uses measured input**. CODATA 2022 is 0.529177210544. The literal stops at six decimals, about 4×10⁻⁷ relative. The next revision should say so on the row.

## B-03 · Fifteen-digit cube-root exponents

The engine works at 50 decimal digits. These four exponents are the literal `mpf("0.333333333333333")`. Each differs from 1/3 by about 3.3×10⁻¹⁶. The formula text already says 1/3.

| Row | Line |
|-----|-----:|
| `Feigenbaum_delta` | 433 |
| `Feigenbaum_alpha` | 436 |
| `Apery_zeta3` | 439 |
| `Water_anomaly_C` | 442 |

If the next revision means a cube root, write `mpf(1)/3`.

The same question appears once more, with a shorter literal: `CMB_tau` at line 987 uses `mpf("0.333333333333")` (twelve 3s).

## B-05 · Version label

Line 4 of the docstring says `FSOT 2.0 — Complete Computational Engine`. The printed banner in `full_report()` (line 1194) says the same. The hub and the pin are FSOT 2.1. The next revision should say 2.1.

## Left off this list

B-04 (older copies of `C_EFF` and `K` in other repos) and B-06 (the 50-digit `GAMMA` and `G_CAT` literals match mpmath) are context from the audit. They are not edits for this pin.
