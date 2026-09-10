# Millennium functions — accuracy vs public SOTA

**Pin:** D1D38A · **Clay Prize claimed:** **no** · **Generated:** `2026-09-10T00:57:24.958747+00:00`

Clay’s three gates (Qualifying Outlet, two years, community acceptance) are a *social process*.
They live in [`MILLENNIUM_PRIZE_TRACK.md`](MILLENNIUM_PRIZE_TRACK.md) and stay honest zeros.

This page is the other question: **does the native math hit the same *function* more accurately than what is currently public?**
Consensus is not the scoring rule. Closed precision is. A miss stays a miss.

**Two bars, never collapsed.** Beating a public competitor is not the same as landing inside the rest-of-system residual gates (**0.5%** green, **0.05%** aspiration). A SOTA beat outside 0.5% is **FSOT accuracy WIP**.

Kill: “we won a Millennium Prize.” Kill: stuffing a residual into the Clay statement.
Kill: retuning β / ρ / 0.2173 / 3.5 to swallow a compare. Kill: claiming ECMWF beaten.
Kill: calling a 4% SOTA-beat “0.5% green.”

## Live tally

| Bucket | n |
|--------|---|
| Beats or meets public SOTA | 6 |
| …of those, inside FSOT 0.5% green | 4 |
| …of those, inside 0.05% aspiration | 3 |
| **SOTA beat, FSOT accuracy still WIP** | **2** |
| Comparable but does **not** beat | 1 |
| **Next dig** (misses + open tracks) | **5** |
| Clay problems remaining | 6 |
| ECMWF beaten | 0 |

## Scoreboard

| Problem | Function | FSOT err % | Public typical err % | SOTA | FSOT 0.5% | FSOT 0.05% | Progress |
|---------|----------|------------|----------------------|------|-----------|------------|----------|
| Riemann hypothesis | Im(ρ1) of ζ — first non-trivial zero (closed form vs tabulated) | 0.001661 | 26.27 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Riemann hypothesis | Im(ρ_n) n=2..10 — mean-spacing walk from seed t1 (out of sample) | 4.261 mean n=2..10 (7/9 zeros) | 5.638 | beats/meets | wip | wip | beats_sota_fsot_accuracy_wip |
| Yang–Mills existence and mass gap | Confinement scale Λ_QCD (zero-parameter seed vs PDG-class / FLAG) | 0.04806 vs PDG 0.2173; 2.068 vs FLAG 213 | 3.756 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Yang–Mills existence and mass gap | Lightest 0++ glueball / √σ vs lattice precision (measurement) | 4.567 vs Teper 3.65; 0.4774 vs in-repo 3.5 | 3.014 | miss | wip | wip | miss_next |
| Yang–Mills existence and mass gap | Lightest 0++ glueball / √σ vs Teper's own closed-form ~4√σ | 4.567 | 9.589 | beats/meets | wip | wip | beats_sota_fsot_accuracy_wip |
| Yang–Mills existence and mass gap | Glueball tensor/scalar m(2++)/m(0++) — geometric √2 vs 3/2 rule | 0.2307 | 6.311 | beats/meets | pass | wip | beats_sota_in_green_aspiration_wip |
| Yang–Mills existence and mass gap | Discrete valve path-sum w_POOF + w_hold = 1; a0/γ_color finite | 1.11e-14 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | Global smooth (or blow-up) 3D incompressible NSE | — | — | — | n/a | n/a | open_track_next |
| Navier–Stokes existence and smoothness | Seed-locked transport coefficients on the 1D toy continuum | 0 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | Earth-fluid 24 h hold rate vs majority-class baseline (related fold, not NSE) | 8.333 | 14.29 | miss | wip | wip | miss_next |
| P versus NP | Unstructured-search query exponent (quantum query complexity) | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Birch and Swinnerton-Dyer | rank E(Q) = ord_{s=1} L(E,s) | — | — | — | n/a | n/a | open_track_next |
| Hodge conjecture | Hodge classes = algebraic cycles (rational) | — | — | — | n/a | n/a | open_track_next |

## What this does and does not say

| Function | Result | Why that is the right object |
|----------|--------|------------------------------|
| First Riemann zero Im(ρ1) | **Beats SOTA and in 0.05%** (`e/γ³` 0.00166% vs RvM 26%) | Odlyzko is the measurement. **Not** RH. |
| Riemann zeros n=2..10 | **Beats RvM (4.26% vs 5.64%) — FSOT accuracy WIP** (outside 0.5%) | Public spacing walk. Do not stuff 4.26% into the green gate. |
| Λ_QCD vs PDG 0.2173 | **Beats/meets and in 0.05%** (0.048%) | FLAG 213(8) is a second measurement (2.07%, inside FLAG 1σ, outside 0.5% vs FLAG central). |
| Glueball 0++ vs 4√σ | **Beats 4√σ (4.57% vs 9.59%) — FSOT accuracy WIP** | Same 4.57% vs lattice measurement. Not 0.5% green. |
| Glueball 2++/0++ | **Beats 3/2 (0.23%) — in 0.5% green, aspiration WIP** | √2 geometry. 0.23% > 0.05%. |
| Grover 1/2 | **Meets proven bound and in 0.05%** | Not P vs NP. |

## Next dig (misses and open tracks)

| Item | Why it is next | First cut, no stuffing |
|------|----------------|------------------------|
| Glueball 0++ vs Teper lattice precision | 4.57% vs 3.01% (1.5σ). Lattice is the measurement. | Same seed as the 4√σ beat. Need a better 0++ identity, not a retune of 3.5. |
| Weather 24 h vs majority | Hold 22/28=78.6% vs majority 85.7%. ECMWF not beaten. | Six kills: five quiet-forecast / storm-observed (OLCN6, 42058, 44078) and one thin-obs false storm (62442, n=6). Valve/quiet look, then finer `dt`. |
| 3D NSE smoothness | No public accuracy %. Toy μ>0 is not Clay NSE. | 1D Stokes/heat manufactured solution at the right fold — still not 3D global smoothness. |
| BSD | No native rank predictor. | Cremona 11a1 / 37a1 / 389a1 as the first objects. Do not invent a seed residual. |
| Hodge | No native Hodge-class predictor. | Hodge numbers of a named variety, not a stolen 20 from another domain. |

## Reproduce

```powershell
python vendor/fsot_millennium_accuracy.py
python scripts/run_goal_tracks_verification.py
```

Prize-process flags (separate file, all honest): [`MILLENNIUM_PRIZE_TRACK.md`](MILLENNIUM_PRIZE_TRACK.md).
Yang–Mills object split: [`MILLENNIUM_YM_VS_FSOT.md`](MILLENNIUM_YM_VS_FSOT.md).

Two bars: (1) public SOTA, (2) FSOT green 0.5% / aspiration 0.05%. A SOTA beat outside 0.5% is FSOT accuracy WIP — not stuffed into the gate. Not a Clay Prize. GitHub is not a Qualifying Outlet. Misses (lattice precision, weather majority, NSE smoothness, BSD, Hodge) are next dig.
