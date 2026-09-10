# Millennium functions — accuracy vs public SOTA

**Pin:** D1D38A · **Clay Prize claimed:** **no** · **Generated:** `2026-09-10T00:48:00.777209+00:00`

Clay’s three gates (Qualifying Outlet, two years, community acceptance) are a *social process*.
They live in [`MILLENNIUM_PRIZE_TRACK.md`](MILLENNIUM_PRIZE_TRACK.md) and stay honest zeros.

This page is the other question: **does the native math hit the same *function* more accurately than what is currently public?**
Consensus is not the scoring rule. Closed precision is. A miss stays a miss.

Kill: “we won a Millennium Prize.” Kill: stuffing a residual into the Clay statement.
Kill: retuning β / ρ / 0.2173 / 3.5 to swallow a compare. Kill: claiming ECMWF beaten.

## Live tally

| Bucket | n |
|--------|---|
| Comparable numeric functions | 6 |
| Beats or meets public SOTA | 6 |
| Comparable but does **not** beat | 1 |
| No fair numeric compare yet | 3 |
| Clay problems remaining | 6 |
| ECMWF beaten | 0 |
| Glueball beats Teper lattice precision | 0 |
| Glueball beats Teper 4√σ closed form | 1 |
| Glueball √2 beats 3/2 ratio | 1 |
| Riemann n=2..10 walk beats RvM | 1 |
| Weather 24 h beats majority class | 0 |

## Scoreboard

| Problem | Function scored | FSOT | Public SOTA | FSOT err % | Public typical err % | Verdict | Clay |
|---------|-----------------|------|-------------|----------------|----------------------|---------|------|
| Riemann hypothesis | Im(ρ1) of ζ — first non-trivial zero (closed form vs tabulated) | 14.1345 | Riemann–von Mangoldt / Gram main-term inversion N(T)=1 (zero-parameter public asymptotic) | 0.001661 | 26.27 | beats_public_closed_form | OPEN_NOT_CLAIMED |
| Riemann hypothesis | Im(ρ_n) n=2..10 — mean-spacing walk from seed t1 (out of sample) | 4.26054 | Riemann–von Mangoldt inversion N(T)=n for each n (same public closed form as t1) | 4.261 mean n=2..10 (7/9 zeros) | 5.638 | beats_rvm_panel_mean | OPEN_NOT_CLAIMED |
| Yang–Mills existence and mass gap | Confinement scale Λ_QCD (zero-parameter seed vs PDG-class / FLAG) | 0.21740442 | FLAG 2024 Λ_MS^(5)=213(8) MeV (Aoki et al. 2411.04268) | 0.04806 vs PDG 0.2173; 2.068 vs FLAG 213 | 3.756 | meets_flag_1sigma | OPEN_NOT_CLAIMED |
| Yang–Mills existence and mass gap | Lightest 0++ glueball / √σ vs lattice precision (measurement) | 3.48329 | Teper hep-lat/9711011 continuum 3.65±0.11 (lattice measurement, not a closed form) | 4.567 vs Teper 3.65; 0.4774 vs in-repo 3.5 | 3.014 | does_not_beat_lattice_precision | OPEN_NOT_CLAIMED |
| Yang–Mills existence and mass gap | Lightest 0++ glueball / √σ vs Teper's own closed-form ~4√σ | 3.48329 | Teper hep-lat/9711011 rule of thumb m(0++)~4√σ (same paper as the measurement) | 4.567 | 9.589 | beats_4sqrt_sigma_closed_form | OPEN_NOT_CLAIMED |
| Yang–Mills existence and mass gap | Glueball tensor/scalar m(2++)/m(0++) — geometric √2 vs 3/2 rule | 1.41421 | Teper ~3/2 flux-tube rule (hep-lat/9711011) | 0.2307 | 6.311 | beats_three_halves_rule | OPEN_NOT_CLAIMED |
| Yang–Mills existence and mass gap | Discrete valve path-sum w_POOF + w_hold = 1; a0/γ_color finite | 1 | No public numeric SOTA — Clay object is existence, not a residual | 1.11e-14 | — | native_structure_not_sota_contest | OPEN_NOT_CLAIMED |
| Navier–Stokes existence and smoothness | Global smooth (or blow-up) 3D incompressible NSE | — | Unsolved. No public accuracy percentage on smoothness. | — | — | no_fair_numeric_compare | OPEN_NOT_CLAIMED |
| Navier–Stokes existence and smoothness | Seed-locked transport coefficients on the 1D toy continuum | 1 | No public SOTA for this toy object | 0 | — | native_structure_not_sota_contest | OPEN_NOT_CLAIMED |
| Navier–Stokes existence and smoothness | Earth-fluid 24 h hold rate vs majority-class baseline (related fold, not NSE) | 78.5714 | Majority-class baseline on the same 28 observed rows | 8.333 | 14.29 | does_not_beat_majority_ecmwf_not_beaten | OPEN_NOT_CLAIMED |
| P versus NP | Unstructured-search query exponent (quantum query complexity) | 0.5 | Grover 1996 / Bennett et al. 1997 proven tight bound Θ(N^{1/2}) | 0 | 0 | meets_proven_bound | OPEN_NOT_CLAIMED |
| Birch and Swinnerton-Dyer | rank E(Q) = ord_{s=1} L(E,s) | — | Sage/PARI/Magma ranks on Cremona tables | — | — | no_fair_numeric_compare | OPEN_NOT_CLAIMED |
| Hodge conjecture | Hodge classes = algebraic cycles (rational) | — | No public numeric accuracy % — this is a existence/algebraicity theorem | — | — | no_fair_numeric_compare | OPEN_NOT_CLAIMED |

## What this does and does not say

| Function | Result | Why that is the right object |
|----------|--------|------------------------------|
| First Riemann zero Im(ρ1) | Seed `e/γ³` vs Odlyzko at **0.00166%**; Riemann–von Mangoldt inversion at **~26%** | Closed form vs tabulated zero. Odlyzko is the *measurement*. **Not** RH for all zeros. |
| Riemann zeros n=2..10 | Mean-spacing walk from seed t1, mean err **~4.26%** vs RvM **~5.64%** (7/9 zeros) | Public spacing `2π/log(t/2π)`, no new coefficient. Out of sample. **Not** RH. |
| Λ_QCD | Seed vs in-repo PDG-class 0.2173 GeV at **0.048%**; vs FLAG 213(8) MeV inside 1σ | Zero-parameter confinement scale. **Not** a Wightman mass gap. |
| Glueball m(0++)/√σ vs lattice | `φ²+e/π` vs Teper 3.65±0.11 — **does not beat lattice precision** | Lattice is the measurement. Still a miss. Do not retune 3.5. |
| Glueball m(0++)/√σ vs 4√σ | Same seed vs Teper's own ~4√σ rule — **beats** (4.57% vs 9.59%) | Closed-form competitor from the same paper. |
| Glueball m(2++)/m(0++) | Geometric `√2` vs Teper 5.15/3.65 — **beats** the 3/2 rule (0.23% vs 6.31%) | Spin-geometry on the existing 0++ probe, not a new coefficient. |
| Path-sum / μ>0 / c_s² | Executable identities | Structure, not a SOTA residual contest. |
| Weather 24 h hold | 22/28 = 78.6% vs majority 85.7% — **does not beat majority**; ECMWF **not** beaten | Finer `dt` is still the path. |
| Grover exponent 1/2 | **Meets** Bennett et al. proven bound | Cannot beat a tight bound. **Not** P vs NP. |
| BSD / Hodge | No fair compare | No native rank or Hodge-class predictor. Next push, not a stuffed residual. |

## Reproduce

```powershell
python vendor/fsot_millennium_accuracy.py
python scripts/run_goal_tracks_verification.py
```

Prize-process flags (separate file, all honest): [`MILLENNIUM_PRIZE_TRACK.md`](MILLENNIUM_PRIZE_TRACK.md).
Yang–Mills object split: [`MILLENNIUM_YM_VS_FSOT.md`](MILLENNIUM_YM_VS_FSOT.md).

Accuracy contest on native function-objects. Not a Clay Prize. GitHub is not a Qualifying Outlet. Glueball vs lattice precision is still a miss; vs Teper's 4√σ and 3/2 rules it wins. ECMWF is not beaten. Weather hold does not beat majority class.
