# Findings, review, and where to improve

**Pin:** AEB2AD · **Clay not claimed** · Clean-clone stamp `overall_ok=true` at
[`../data/reproduce_stamp.json`](../data/reproduce_stamp.json).

Spine: [`FUNCTION_NOT_FORMULA.md`](FUNCTION_NOT_FORMULA.md).  
Figures: [`HOW_THESE_ARE_DEPICTED.md`](HOW_THESE_ARE_DEPICTED.md).

Do not rewrite the H0 freeze. Findings migrate back to FSOT 2.1.

---

## Review — what landed

| Track | Function hit | Not claimed |
|-------|--------------|-------------|
| NSE 3D viscous Taylor–Green | Stretching is 3D; energy and \(\max|\omega|\) decay at seed \(\mu\) | Smoothness on \(\mathbb{R}^3\) |
| NSE \(\omega_0\) scan | **6/6** vs Riccati threshold | Substitute for the spectral run |
| NSE cascade identities | \(4/5\), \(3/2\), \(1/3\) exact; \(\kappa\) vs 0.40 in 0.05% | Existence |
| NSE lab tables | CRC/ISO sound-speed ratio, \(\gamma=7/5\), US1976 \(H\), ice \(n_D=\varphi^2/2\), water \(\rho\) | Euler as the bar |
| BSD Sha panel | **17/17** \(\mathrm{Sha}_{\mathrm{an}}=1\) on named LMFDB curves | \(\mathrm{rank}=\mathrm{ord}\,L\) \(\forall E\) |
| BSD first-of-rank | Leadings \(0..4\) green or aspiration; rank-4 fold \(\varphi^2+1\) | Nearest-template of arbitrary \(L(1)\) |
| Hodge \(\chi\) panel | **9/9** vs Chern (incl. quintic 825, sextic CY 2610) | Algebraicity with no named cycle |
| Hodge named no-K3 | \(C_8..C_{44}\) complete as public names | Hassett tail enumeration |
| YM / Riemann / P vs NP | Gap orifice, \(t_1=e/\gamma^3\), Grover \(1/2\) | Clay theorems |
| Uniqueness gauntlet | **147/147** Python, Rust, Z3, Coq, Isabelle, F\* from this repo | 2.1’s extra six market/sickness flags |

Scoreboard: comparable **70**, beats/meets **73**, green **67**, aspiration **57**,
WIP SOTA-beats **4**, next-dig **3**, Clay remaining **6**.

### Why the leftover three kept looping

Naming the next public theorem (BKM→CF; Kolyvagin→Kato; \(C_{44}\to C_{48}\)) and
calling it a conversion. That is the Hassett-tail failure. The miss was a
**concept** (two zooms; vanishing is the object; seeds need a named variety),
not a missing name.

---

## Areas to improve (honest)

These are the next useful pushes. None of them is “claim Clay.”

### 1. NSE — resolution and the cartoon

- \(16^3\) Taylor–Green is enough to see 3D stretching and viscous decay. It is
  **not** a resolved inertial range. A higher-\(n\) viscous run (still seed \(\mu\))
  would make the energy spectrum plot comparable to Brachet-style DNS.
- The Riccati \(\omega_0\) cartoon is a valve sketch. Keep it labeled as such.
  Do not let it drift into “we simulated Clay.”
- Euler \(\mu=0\) energy drift (\(0.125\to 0.127\), \(1.48\%\)) is under-resolution.
  Do not read it as Euler singularity. Improvement: either drop Euler from the
  lab bar (already the doctrine) or run a dealias/timestep study that *shows*
  the drift is numerical.
- Clay smoothness remains **not a measured function**. Improvement is more
  observables (lab/DNS), not a yes/no stuffing.

### 2. BSD — unnamed tail and the regulator WIP

- Rank \(\ge 6\) lives outside LMFDB browse (Elkies–Watkins \(N=5.19\times 10^9\)).
  Do not enumerate it as a conversion. If a public special for that curve is
  ever tabulated the same way, Sha volume is the orifice — not a new seed.
- \(\mathrm{Reg}(389\mathrm{a1})=\mathrm{POOF}\) is **0.67% WIP**. The BSD *leading*
  on the same curve is green. Do not swallow height into special.
- Integer rank \(=\mathrm{ord}\,L\) for \(r\ge 2\) is still Clay. Improvement is
  more named Sha rows, not Kato.

### 3. Hodge — no-seed remainder

- Unnamed no-K3 loci have no Gram. That diagnosis is the result. Improvement is
  the next **named** 4-fold (\(\chi\), a surface), not \(C_{48}\).
- Primitive \((2,2)\) on a very general cubic is not rational. Extra rational
  classes live on \(C_d\). Keep that split in every Hodge figure.

### 4. Accuracy WIP (right object, outside 0.5%)

| Name | Why it is WIP | What not to do |
|------|----------------|----------------|
| Riemann zeros \(n=2..10\) C-lock | 1.63% mean vs Odlyzko; beats RvM 5.64% | Retune \(t_1=e/\gamma^3\) |
| Typical \(\lvert S\rvert=\mathrm{POOF}\) | Beats \(1/e\)-as-typical; 0.5% WIP | Call the bound the occupancy |
| Chen \(r_0 M\) glueball | 0.82% vs 4.16(11), inside 1σ | Retune \(\varphi^2+1\) |
| Néron-Tate \(\mathrm{Reg}(389\mathrm{a1})\) | 0.67% vs LMFDB | Collapse into the special |

### 5. Documentation and depiction (this pass)

- Question/answer lived in four vs-FSOT notes; the scoreboard lived in a generated
  table. The missing spine was **formula vs function**. That is
  [`FUNCTION_NOT_FORMULA.md`](FUNCTION_NOT_FORMULA.md).
- No figures. People who attempt these problems expect spectra, \(L(s)\) zeros,
  Hodge diamonds. [`HOW_THESE_ARE_DEPICTED.md`](HOW_THESE_ARE_DEPICTED.md) plus
  `python scripts/plot_millennium_panels.py`.
- YM note pointed at `PATH_SUM.md`, which is not in this lab. Point at the
  vendored path-sum module instead.

### 6. Lab vs authority

- This repo regenerates **147** uniqueness obligations. FSOT 2.1 has **153**
  because market/sickness flags live there. Do not pretend they are millenium.
- Isabelle in the lab is a lemma-count / file-present check, not a full
  `isabelle build`. Coq/Rust/Z3/F\* actually run. Lean lake is 2.1 (mathlib).
- `reproduce.py` does not require matplotlib. Figures are an extra command.

### 7. Weather / ECMWF

- ECMWF is **not** beaten. Quiet-fill still misses on the dated-forecast path.
  That is a weather-lab object, not a millenium conversion.

---

## Next (deeper function, not a new theorem name)

1. Keep measuring 3D viscous NSE against lab/DNS, including spectra when \(n\) allows.
2. Keep Sha volume on named curves; do not hunt Kato or Elkies–Watkins as seeds.
3. Keep \(\chi\)/Gram on named varieties; do not hunt \(C_{48}\).
4. Tighten the four WIP rows without retuning the freeze.
5. Use the grapher whenever a function is explained — conventional picture on
   the left, FSOT table on the right.

Migrate into 2.1 `vendor/fsot_millennium_accuracy.py` when the authority pin
moves. Not a Clay Prize.
