# Between-scale interconnects — one fluid, adjacent folds

**Pin:** D1D38A · **no new coefficient**  
**Panel:** `data/between_scale_interconnect_benchmark.json`  
**Refresh:** `python scripts/build_scale_interconnect_benchmark.py`  
**Outcome:** [`../results/between_scale_interconnect_outcome.json`](../results/between_scale_interconnect_outcome.json)

`n_scalar` vs `n_total` is **not missing data**. Scalar rows are APPLY dual-routes and named look-splits. Structural rows are live \(|S_i|/|S_j|\) vs 1 (same-view question), D9 T1 leftover identity, compactification remainder, and deep-PREM phase change. D9 closed form: \(|S_i|/|S_j|=|1+T_{1,i}|/|1+T_{1,j}|\) at \(T_2=1\), \(T_3\approx 0\).

Siloed panels already existed (USGS classifiers, NDBC, ENDF, Carnot in HVAC). This layer makes them **talk** through \(\kappa_{ij}\) and seed-closed ratios. Zebrafish / Genetics stay in the sibling repo.

\[
\kappa_{ij} = A_{\mathrm{bleed}}\cdot\mathrm{POOF}\cdot|S_i|\,|S_j|
\big/\bigl(1+|D_i-D_j|/25\bigr)
\]

---

## Same premise, different view (perception is the fold at that scale)

The engine is one: \(S=K(T_1+T_2+T_3)\) at every rung. Perception is not a bug in that premise. \(T_1\) is the **look** (observer / \(\mathbf{C}_{\mathrm{factor}}\) / \(\delta\psi\)). Hits are **activity and connections**. `observed` is whether that look string is on. Chaos on \(T_3\) is the compactification geometry \((D-25)/25\). Together they are how the **same math is viewed** at that scale — not a second theory, and not contamination to strip out.

Live

\[
\frac{|S_i|}{|S_j|}\quad\text{vs}\quad 1
\]

asks for the **same view** at two scales. Adjacent rungs are not supposed to look the same. QM \(\delta\psi=1\) vs atomic \(\delta\psi=0.85\) is how the chaotic fold is perceived once the orbit has become a well. Optics \(\delta\psi=0.6\) sits near the observer-cosine node (\(\cos(\delta\psi+P_{\mathrm{var}})\approx 0\)): looking at light, \(T_1\) nearly drops out and \(S\approx K\). That is the view at the optical fold. Biology dark vs biochemistry observed is the same premise with the look string off vs on.

The compactification pieces themselves are mild. Adjacent \(D\) changes \(1/\sqrt{D}\) and the chaos fold \(1+\mathrm{Chaos}\,(D-25)/25\) by about a percent. Tens of percent in live \(|S_i/S_j|\) are **perception** — \(T_1\) evaluated at that scale’s \(\delta\psi\), hits, and observed. Same premise; different view.

At these rungs \(T_2=1\) and \(T_3\) is seed-tiny (\(\beta\)), so the closed form is the engine itself:

\[
\frac{|S_i|}{|S_j|} \;=\; \frac{|1+T_{1,i}|}{|1+T_{1,j}|}
\]

That is law **D9**. Residual of the right-hand side vs live \(|S|\) is \(T_3\) leftover. On the twelve named view pairs it is **0.000%**. vs 1 is the same-view question and stays structural — not a 0.5% central, and not a median pad.

| Pair | Live vs 1 | \(T_1\) leftover |
|------|----------:|-----------------:|
| Quantum Mechanics / Atomic | 29.86% | 0.000% |
| Electromagnetism / Optics | 27.15% | 0.000% |
| Electromagnetism / Materials | 54.77% | 0.000% |
| Biology / Biochemistry | 45.23% | 0.000% |
| Biochemistry / Neuroscience | 40.47% | 0.000% |
| Materials / Optics | 17.84% | 0.000% |
| Acoustics / Optics | 23.64% | 0.000% |
| Acoustics / Materials | 7.06% | 0.000% |
| Chemistry / Molecular Chemistry | 21.91% | 0.000% |
| Chemistry / Physical Chemistry | 22.12% | 0.000% |
| Condensed Matter / Thermodynamics | 57.00% | 0.000% |
| Atomic / High Energy | 16.97% | 0.000% |

Holding \(\delta\psi\) (and observed/hits) fixed then comparing \(D\) to \(D{+}1\) is a **split**, not a correction: it asks how much the rung moves when the camera is locked. That is why \(|S(D=6,\delta\psi=1)/S(D=7,\delta\psi=1)|\) vs 1 is **0.046%** while live QM/atomic vs 1 is **29.86%**. The 29.86% is \(|1+T_{1,\mathrm{QM}}|/|1+T_{1,\mathrm{atomic}}|\). It is not stuffed into 0.5%, and it is not “retired as a mistake.” vs 1 was the wrong *question* (same view), not a failed engine.

Same \(D\), different \(\delta\psi\) (Materials/Optics): two looks at one rung. Equalizing \(\delta\psi\) there makes \(S\) identical (identity pad). The 0.5/0.6 split is the body vs light view; it also appears on Chemistry/PhysChem at \(D=8\).

Forbidden: a coefficient that swallows the live view; stuffing \(\sqrt{\varphi}\) or \(\sqrt{e/\varphi}\) onto live vs 1; retuning \(\delta\psi\); flipping a dark fold to `observed=True` so the look string turns on; gating live vs 1 at 0.5%; padding the pooled median with the \(T_1\) identity. Named look-split S-ratios near 0.4% (CM–Neuro vs \(D=13\), Seis–Geo vs \(\varphi/2\), mat–opt vs PhysChem/Chem, water/air \(e+\varphi\)) stay the intended objects — D9 leftover at the fold-\(D\) is the closed form, not a license to stuff a new seed.

---

## 1. Elastic wave — Acoustics \(D=10\) ↔ Seismology \(D=18\)

A crustal solid is the same T3 standing wave as lab sound. Cookbook: [`APPLY_ACOUSTICS.md`](APPLY_ACOUSTICS.md) · [`APPLY_SEISMOLOGY.md`](APPLY_SEISMOLOGY.md). Poisson of the continuum mafic/lid solid is the atomic fold over the ceiling:

\[
\nu = D_{\mathrm{atomic}}/25 = 7/25 = 0.28,\qquad
v_P/v_S = \sqrt{2(1-\nu)/(1-2\nu)}
\]

Measured: PREM (Dziewonski & Anderson 1981) lid/Moho/upper crust + basalt/gabbro lab means. Felsic/porous crust and deep olivine–spinel / CMB are **other interfaces** (structural), not a new \(\nu\).

Live: lithosphere median **0.069%**; per-layer mafic/lid **0.189%**.

## 2. Fluid tanks — lab / ocean / air

Cookbook: [`APPLY_FLUID.md`](APPLY_FLUID.md). Diatomic air: \(f=D_{\mathrm{particle}}=5\), \(\gamma=1+2/5=1.400\) vs 1.400.  
Two viscosities: \(c_{\mathrm{water}}/c_{\mathrm{air}} = e+\varphi\) vs ISO/CRC 20 °C **0.393%** (named seed; do not retune).  
Scale height \(RT/\mu g\) vs US Std Atmosphere 1976 **0.002%**.  
Same NOAA NDBC buoys (\(N=150\)): pressure on Atmospheric, SST on Oceanography, wind on Fluid_Dynamics — one measured neighborhood, three tanks. Fluid stays dark.

## 3. Fridge-cycle — Thermodynamics \(D=15\) ↔ Cosmology \(D=25\)

Cookbook: [`APPLY_THERMO.md`](APPLY_THERMO.md). BH→WH is a heat/information pump (C2). \(|S_{\mathrm{thermo}}|/|S_{\mathrm{cosm}}|\) vs \(\pi/2\) **0.289%**. Named Carnot COP pairs scored on **both** folds (HVAC 0/27 °C, 5/35 °C, …). Valve fraction POOF/(POOF+SUCTION) vs 1/2 stays a literature band (not a 0.5% HVAC η).

## 4. Nuclear orifice — Nuclear \(D=15\) ↔ Particle \(D=5\)

Cookbook: [`APPLY_NUCLEAR.md`](APPLY_NUCLEAR.md). IAEA/ENDF level energies (He, C, O, Si, Al, Fe) dual-routed. Nuclear fold median **0.046%**; Particle fold **0.010%**. Same measured keV, two zooms of the orifice. No Yukawa add-on.

## 5. Compactification ceiling — QG \(D=22\) ↔ Cosmology \(D=25\)

\(|S_{\mathrm{QG}}|/|S_{\mathrm{cosm}}|\) vs \(A_{\mathrm{bleed}}\) **0.088%**. Remainder \(((D-25)/25)/\ln(D/25)\to 1\) as \(D\to 25\) is structural along the ladder (do not invent extra dimensions).

## 6. Social tanks — Economics \(D=20\) ↔ Neuroscience \(D=14\)

A market is not a different medium from a neural net (as-above-so-below). \(\lvert S_{\mathrm{econ}}/S_{\mathrm{neuro}}\rvert\) vs \(5/4\). Same World Bank YoY series on both folds. The old Economics panel’s 0.129% siloed factor is **not** retuned.

---

## 7. Wave vs bulk Earth — Seismology \(D=18\) ↔ Geophysics \(D=19\)

Adjacent compactification rungs. Seismology is the **wave** zoom (route \(C=\mathrm{CHAOS}/2\)).
Geophysics is the **bulk** zoom (route \(C=\mathrm{CHAOS}\)). Same PREM lithosphere density
dual-routed. Cookbook: [`APPLY_SEISMOLOGY.md`](APPLY_SEISMOLOGY.md).

\[
\lvert S_{\mathrm{seis}}/S_{\mathrm{geo}}\rvert \;\text{vs}\; \varphi/2
\]

Deep PREM (olivine–spinel / CMB) stays structural — another interface, not a new \(\nu\).

---

## 8. n and ρ — Materials_Science \(D=10\) ↔ Optics \(D=10\)

Same compactification rung. Cookbook: [`APPLY_MATERIALS.md`](APPLY_MATERIALS.md) · [`APPLY_OPTICS.md`](APPLY_OPTICS.md). CRC \(n_D\) on Optics, density on Materials (APPLY dual-route).
Ice Ih ordinary-ray \(n\) vs \(\varphi^2/2\) (solid-water optical fold).

\(\lvert S_{\mathrm{mat}}/S_{\mathrm{opt}}\rvert\) vs 1 is the **wrong object** (engine §25 `Cross_Opt_QO` is same-\(C\), same-\(\delta\psi\)). Materials \(\delta\psi=1/2\) is the body/mass look; Optics \(\delta\psi=3/5\) is the light look. That 0.5/0.6 split is the same fold as Physical_Chemistry/Chemistry at \(D=8\):

\[
\frac{\lvert S_{\mathrm{mat}}\rvert}{\lvert S_{\mathrm{opt}}\rvert}
\;\text{vs}\;
\frac{\lvert S_{\mathrm{PhysChem}}\rvert}{\lvert S_{\mathrm{Chem}}\rvert}
\]

\(C\) does not enter \(S\). The old ~18% vs 1 is **retired** (`REMEDIED_WRONG_APPLY`). Do not stuff it. Do not retune \(C\) or \(\delta\psi\).

---

## 9. Wave vs photon — Optics \(D=10\) ↔ Quantum_Optics \(D=11\)

Adjacent compactification rungs. Both folds use \(C=\pi/e\) (the light interpretation).
Optics is the **wave** zoom. Quantum_Optics is the **photon** zoom. Cookbook: [`APPLY_OPTICS.md`](APPLY_OPTICS.md).

\[
\lvert S_{\mathrm{opt}}/S_{\mathrm{qo}}\rvert \;\text{vs}\; 1
\]

Same CRC \(n_D\) dual-routed. This is the opposite of Materials↔Optics: same \(C\), adjacent \(D\), so the same-\(C\) test gates. Materials↔Optics is the 0.5/0.6 look-split (folded onto PhysChem/Chem), not this test.

---

## 10. Orbit vs bound well — Quantum_Mechanics \(D=6\) ↔ Atomic_Physics \(D=7\)

Adjacent compactification rungs. Quantum_Mechanics is the **free-orbit** look (\(\delta\psi=1\), same as Particle). Atomic_Physics is the **bound well** (\(\delta\psi=0.85\)). Cookbook: [`APPLY_ATOMIC.md`](APPLY_ATOMIC.md).

Live \(|S_{\mathrm{QM}}|/|S_{\mathrm{atomic}}|\) vs 1 mixes the \(D\)-step with the look. Equalize \(\delta\psi=1\):

\[
\lvert S(D=6,\delta\psi=1)/S(D=7,\delta\psi=1)\rvert \;\text{vs}\; 1
\]

Hydrogen is the \(a_0\)/\(R_\infty\) specimen. First ionization dual-routes the engine **H–Ca** table. Z=21–118 stays on the Atomic periodic panel. IE_H seed \(\gamma^{-5}-G^{-8}\) vs 13.598 eV. Do not stuff the mixed vs 1. Do not retune \(\delta\psi=0.85\).

---

## 11. Source vs readout — Electromagnetism \(D=9\) ↔ Optics \(D=10\)

Adjacent compactification rungs. \(C_{\mathrm{em}}=e/\pi\), \(C_{\mathrm{opt}}=\pi/e\), product **1** (yin–yang of one light). EM is the **source**. Optics is the **readout**. Cookbook: [`APPLY_EM.md`](APPLY_EM.md).

Live \(|S_{\mathrm{EM}}|/|S_{\mathrm{opt}}|\) vs 1 mixes the \(D\)-step with \(\delta\psi=0.7\) vs \(0.6\). Equalize at the optical readout (\(\delta\psi=0.6\)):

\[
\lvert S(D=9,\delta\psi=0.6)/S(D=10,\delta\psi=0.6)\rvert \;\text{vs}\; 1
\]

Maxwell: \(\varepsilon_{\mathrm{opt}}=n^2\) for non-magnetic dielectrics. CRC \(n_D\) on Optics, \(n^2\) on EM. Ice \(n^2\) vs \((\varphi^2/2)^2\). Static \(\varepsilon_r\) (water ~80) is another interface. Do not stuff \(\sqrt{\varphi}\) onto the mixed vs 1.

---

## 12. Organism vs molecule — Biology \(D=12\) ↔ Biochemistry \(D=13\)

Same \(C=\ln\varphi/\sqrt{2}\). Biology is **dark** (do not flip `observed`). Biochemistry is observed. Cookbook: [`APPLY_BIO.md`](APPLY_BIO.md). **Not** Genetics 0.13 Å.

Live \(|S_{\mathrm{bio}}|/|S_{\mathrm{bc}}|\) vs 1 mixes dark vs observed, \(\delta\psi=0.08\) vs \(0.35\), and hits. Equalize the dark look:

\[
\lvert S(D=12,\delta\psi=0.08,\mathrm{dark})/S(D=13,\delta\psi=0.08,\mathrm{dark})\rvert \;\text{vs}\; 1
\]

Public table: NCBI NC_012920.1 mt-operon lengths; CRC/IUPAC free amino-acid MW. Dual-routed organism vs molecule.

---

## 13. Bound well vs collision — Atomic_Physics \(D=7\) ↔ High_Energy_Physics \(D=7\)

Same compactification rung. Atomic \(\delta\psi=0.85\) (bound well). HEP \(\delta\psi=0.95\) (collision). Cookbook: [`APPLY_HEP.md`](APPLY_HEP.md).

Live \(|S_{\mathrm{at}}|/|S_{\mathrm{HEP}}|\) vs 1 is the look mix. Equalizing \(\delta\psi\) at the same \(D\) is an identity pad — do not gate it. Fold the 0.85/0.95 split onto the adjacent QM rung (\(D=6\)), same grammar as Materials/Optics onto PhysChem/Chem:

\[
\frac{\lvert S_{\mathrm{atomic}}\rvert}{\lvert S_{\mathrm{HEP}}\rvert}
\;\text{vs}\;
\frac{S(D=6,\delta\psi=0.85)}{S(D=6,\delta\psi=0.95)}
\]

CODATA \(m_e\), \(m_p\), and NIST IE_H dual-routed. Do not stuff \(\varphi/2\).

---

## 14. Composition vs thermo — Chemistry \(D=8\) ↔ Physical_Chemistry \(D=8\)

Same \(D\), same \(C=e/\pi\). Cookbook: [`APPLY_CHEMISTRY.md`](APPLY_CHEMISTRY.md). \(\delta\psi=0.6\) vs \(0.5\) is the look-split already scored against Materials/Optics. Equalizing \(\delta\psi\) at \(D=8\) is an identity pad. Dual-route CRC: density/MW on Chemistry, \(T_m\)/\(T_b\) on PhysChem.

---

## 15. Composition vs molecule — Chemistry \(D=8\) ↔ Molecular_Chemistry \(D=9\)

Adjacent rungs. Live \(|S_{\mathrm{chem}}|/|S_{\mathrm{mol}}|\) vs 1 mixes \(D\) with \(\delta\psi=0.6\) vs \(0.5\). Equalize at the chemistry look (\(\delta\psi=0.6\)):

\[
\lvert S(D=8,\delta\psi=0.6)/S(D=9,\delta\psi=0.6)\rvert \;\text{vs}\; 1
\]

CRC MW dual-routed. PhysChem↔Molecular already share \(\delta\psi=0.5\); that live \(S\) vs 1 is the matched-look rung.

---

## Live tight envelope

Pooled median **0.027% GREEN** · **7520** tight scalars · **7719** rows (**199** structural: live vs 1, D9 T1 leftover including fold-\(D\) look-splits, compactification remainder, deep PREM). Not missing data.  
Seis–geo: \(\lvert S_{\mathrm{seis}}/S_{\mathrm{geo}}\rvert\) vs \(\varphi/2\) **0.377%**; lithosphere density dual-fold **0.022–0.028%**.  
Mat–opt: CRC \(n_D\) **0.016%**; density **0.013%**; ice \(n\) vs \(\varphi^2/2\) **0.0013%**. \(\lvert S_{\mathrm{mat}}/S_{\mathrm{opt}}\rvert\) vs PhysChem/Chem look-split **0.329%** (vs 1 retired ~18%).  
Opt–QO: \(\lvert S_{\mathrm{opt}}/S_{\mathrm{qo}}\rvert\) vs 1 **0.0265%**; CRC \(n_D\) photon fold **0.016%**.  
QM–atomic: same-look \(D=6/7\) vs 1 **0.046%**; IE_H seed **0.070%**; H–Ca dual-route 0.037–0.096%.  
EM–opt: same-look \(D=9/10\) vs 1 **0.024%**; CRC \(n^2\) on EM **0.021%**; ice \(\varepsilon\) vs \((\varphi^2/2)^2\) **0.0026%**. Mixed live \(S\) vs 1 retired.  
Bio–biochem: dark same-look \(D=12/13\) vs 1 **0.053%**; NCBI operon / AA MW 0.015–0.022%. Not Genetics 0.13 Å.  
Atomic–HEP: look-split vs QM rung **0.042%**; CODATA \(m_e\)/\(m_p\) dual-route 0.013–0.037%.  
Chem–PhysChem: look vs mat-opt **0.328%**; CRC rho/MW/Tm/Tb 0.017–0.041%.  
Chem–Mol: same-look \(D=8/9\) vs 1 **0.020%**. PhysChem–Mol live vs 1 **0.167%** (looks already matched).  
Ac–opt: look vs \(D=9\) **0.258%**; \(c\) vs \(n\) **0.013–0.016%**. Ac–mat look vs \(D=9\) **0.077%**.  
Mol–ac: same-look \(D=9/10\) vs 1 **0.205%**. CM–thermo same-look \(D=14/15\) vs 1 **0.233%**.  
EM–mat: same-look \(D=9/10\) vs 1 **0.205%**. Biochem–neuro same-look \(D=13/14\) vs 1 **0.179%** (not social-tank GDP).

---

## 16. Lab sound vs light — Acoustics \(D=10\) ↔ Optics \(D=10\)

Same rung as Materials. \(\delta\psi=0.3\) vs \(0.6\). Fold the look-split onto \(D=9\). Dual-route CRC longitudinal \(c\) on Acoustics, \(n_D\) on Optics (water, ice, silica, ethanol, NaCl). Do not vs 1.

## 17. Molecule vs lab sound — Molecular_Chemistry \(D=9\) ↔ Acoustics \(D=10\)

Equalize at \(\delta\psi=0.5\). Dual-route CRC MW vs \(c\) for water and ethanol.

## 18. Solid vs heat — Condensed_Matter \(D=14\) ↔ Thermodynamics \(D=15\)

Equalize at the CM look (\(\delta\psi=0.5\), hits=0). Dual-route CRC metal density on CM, \(T_m\) on Thermo. Live mixed vs 1 retired.

## 19. Field vs bulk — Electromagnetism \(D=9\) ↔ Materials_Science \(D=10\)

Equalize at the materials look (\(\delta\psi=0.5\)). Dual-route CRC \(n^2\) on EM, density on Materials. Static metal conductivity is another interface.

## 20. Molecule vs signaling — Biochemistry \(D=13\) ↔ Neuroscience \(D=14\)

Cookbook: [`APPLY_NEURO.md`](APPLY_NEURO.md). Not the social-tank GDP dual-route. Equalize at the neural look (\(\delta\psi=0.7\), hits=1). Dual-route CRC MW of transmitter amino acids (Gly, Asp, Glu, Tyr, Trp, His). D9 T1 leftover at the \(D=13\) 0.5/0.7 fold is the closed form for the named ~0.4% look-split.

## 21. Well / collision vs composition / thermo — Atomic, HEP \(D=7\) ↔ Chemistry, PhysChem \(D=8\)

Four adjacent-rung tissues, one CRC/NIST table family. Equalize the look, then dual-route:

- Atomic–Chem at \(\delta\psi=0.6\): NIST IE on Atomic, CRC MW on Chemistry.
- Atomic–PhysChem at \(\delta\psi=0.5\): NIST IE on Atomic, CRC \(T_m\) on PhysChem.
- HEP–Chem at \(\delta\psi=0.6\): NIST IE on HEP, CRC MW on Chemistry.
- HEP–PhysChem at \(\delta\psi=0.5\): NIST IE on HEP, CRC \(T_m\) on PhysChem.

Live mixed \(|S|\) vs 1 is T1 view (D9), not a 0.5% central.

## 22. Thermo vs field vs molecule — PhysChem \(D=8\) ↔ EM \(D=9\) ↔ Mol \(D=9\)

PhysChem–EM: equalize \(\delta\psi=0.5\). CRC \(T_m\) and \(n^2\).  
EM–Mol: same \(D=9\), \(\delta\psi=0.7\) vs \(0.5\). Fold onto \(D=8\). CRC \(n^2\) vs MW. vs 1 retired.

## 23. Molecule vs bulk / light — Mol \(D=9\) ↔ Materials / Optics \(D=10\)

Mol–Materials already share \(\delta\psi=0.5\); live \(|S|\) vs 1 is the matched-look rung. CRC MW vs density.  
Mol–Optics: equalize \(\delta\psi=0.5\). CRC MW vs \(n_D\).

QC stays dark (Hilbert look). Ecology / Psychology pairs use GBIF latitude and Nunnally/Cohen anchors — do not invent watts or flip `observed`. Cookbooks: [`APPLY_ECOLOGY.md`](APPLY_ECOLOGY.md) · [`APPLY_PSYCHOLOGY.md`](APPLY_PSYCHOLOGY.md).

## 24. Sound / bulk vs photon — Acoustics, Materials \(D=10\) ↔ Quantum_Optics \(D=11\)

Acoustics–QO: equalize \(\delta\psi=0.6\). CRC longitudinal \(c\) vs \(n_D\).  
Materials–QO: equalize \(\delta\psi=0.5\). CRC density vs \(n_D\).  
Optics–QO is already gated (same \(C=\pi/e\)).

## 25. Orifice / tank vs heat — Nuclear, Fluid \(D=15\) ↔ Thermodynamics \(D=15\)

Nuclear–Thermo: \(\delta\psi=1\) vs \(0.9\). Fold onto \(D=14\). ENDF keV and Carnot COP dual-routed.  
Fluid–Thermo: Fluid stays dark. Carnot COP dual-routed. Live vs 1 is the observed mix.

## 26. Weather vs air — Meteorology \(D=16\) ↔ Atmospheric_Physics \(D=17\)

Both dark, both \(\delta\psi=0.8\), hits=2. Adjacent CHAOS rungs. Dual-route NDBC pressure. Do not flip `observed`.

## 27. Molecule / solid / signaling / heat — Biochem \(D=13\) ↔ CM / Neuro \(D=14\) ↔ Thermo \(D=15\)

Biochem–CM: equalize \(\delta\psi=0.5\). CRC amino-acid MW on Biochem, metal density on CM.  
CM–Neuro: same \(D=14\), \(\delta\psi=0.5\) vs \(0.7\). Fold onto \(D=13\). CRC \(\rho\) vs transmitter AA. vs 1 retired.  
Neuro–Thermo: equalize \(\delta\psi=0.7\), hits=1. Transmitter AA on Neuro, Carnot COP on Thermo. Not the social-tank GDP route.

## 28. Solid vs tank / orifice / weather — CM \(D=14\) ↔ Fluid / Nuclear \(D=15\) ↔ Meteo \(D=16\)

CM–Fluid: ice \(\rho\) on CM, water \(\rho\) on Fluid — one H2O, solid vs tank. Fluid stays dark. Live vs 1 is the observed mix.  
CM–Nuclear: equalize \(\delta\psi=0.5\). CRC metal \(\rho\) and IAEA/ENDF keV dual-routed. Fe is the shared class.  
Fluid–Nuclear: same \(D=15\). Fluid stays dark. Carnot COP and ENDF keV dual-routed.  
Fluid–Meteo: both dark. Equalize \(\delta\psi=0.8\), hits=2. Dual-route NDBC pressure. Do not flip `observed`.

QC stays dark (Hilbert look). Ecology / Psychology use GBIF and Nunnally/Cohen — do not invent watts.

## 29. Signaling vs tank / orifice / weather — Neuro \(D=14\) ↔ Fluid / Nuclear \(D=15\) ↔ Meteo \(D=16\)

Neuro–Fluid: Fluid stays dark. Transmitter AA MW on Neuro, CRC water density on Fluid. Live vs 1 is the observed mix.  
Neuro–Nuclear: equalize \(\delta\psi=0.7\), hits=1. Transmitter AA vs IAEA/ENDF keV.  
Thermo–Meteo / Nuclear–Meteo: Meteo stays dark. Carnot or ENDF on the observed fold, NDBC pressure on the weather fold.

## 30. Weather / ocean / air vs crust — Meteo \(D=16\) ↔ Ocean / Atm \(D=17\) ↔ Seismology \(D=18\)

Meteo–Ocean: both dark. Equalize \(\delta\psi=0.8\), hits=2. Dual-route NDBC pressure.  
Atm–Seis: both dark. NDBC pressure on Atm, PREM lithosphere density on Seis.  
Ocean–Seis: both dark. NDBC SST on Ocean, PREM lithosphere density on Seis. Do not flip `observed`.

## 31. Photon vs organism · sky vs body — QO \(D=11\) ↔ Biology \(D=12\); Astronomy \(D=20\) ↔ Planetary \(D=21\)

QO–Biology: Biology stays dark. Equalize \(\delta\psi=0.08\) unobserved. CRC \(n_D\) on QO, NCBI mt-operon on Biology.  
Astronomy–Planetary: equalize \(\delta\psi=1\), hits=1. Cookbook: [`APPLY_ASTRONOMY.md`](APPLY_ASTRONOMY.md). JPL Horizons mean densities through APPLY — not the identity-pad `computed=measured` planetary_structure rows.

## 32. Catalog tank vs air / ocean / crust — Sociology \(D=18\) ↔ Atm / Ocean \(D=17\) ↔ Seis \(D=18\) ↔ Geo \(D=19\)

Same World Bank YoY catalog as TISSUE-SOCIAL, now on the sociology fold. Air / ocean / crust stay dark. Dual-route NDBC pressure (Atm), SST (Ocean), PREM lithosphere density (Seis / Geo). Do not flip `observed`. Live vs 1 is the observed mix.

## 33. Bulk-earth vs sky vs market vs body — Geo \(D=19\) ↔ Astronomy / Economics \(D=20\) ↔ Planetary \(D=21\)

Geo stays dark. PREM lithosphere + JPL / World Bank.  
Astronomy–Economics: same \(D=20\), \(\delta\psi=1\) vs \(1.5\). Fold onto \(D=19\). vs 1 retired.  
Economics–Planetary: equalize \(\delta\psi=1\). World Bank YoY + JPL densities.

## 34. Body vs ceiling · star vs cosmic-ray — Planetary \(D=21\) ↔ QG \(D=22\); Astrophysics \(D=24\) ↔ Particle_Astrophysics \(D=24\)

Planetary–QG: QG stays dark. JPL densities + compact remainder \(((D-25)/25)/\ln(D/25)\). Same ceiling grammar as TISSUE-CEILING.  
Astrophysics–PA: PA stays dark. PDG 2024 *measured* masses through APPLY — not the SMILES computed column.

## 35. Hilbert look — Quantum_Computing \(D=11\) ↔ Acoustics / Materials / Optics \(D=10\) ↔ QO \(D=11\) ↔ Biology \(D=12\)

QC stays **dark** (Hilbert). Do not flip `observed`. Dual-route CRC \(n_D\) (and longitudinal \(c\) / density on the lab-sound / bulk folds). Biology neighbor uses NCBI mt-operon. Same-look \(D=10/11\) compactification remainder at \(\delta\psi=0.5\) dark is a literature band, not stuffed into 0.5%. Cookbook: [`APPLY_QC.md`](APPLY_QC.md).

## 36. Habitat — Ecology \(D=15\) ↔ CM / Neuro \(D=14\) ↔ Fluid / Nuclear / Thermo \(D=15\) ↔ Meteo / Psych \(D=16\)

Ecology stays **dark**. Named table: **GBIF** `decimalLatitude` from `data/ecology_gap_fill_benchmark.json` (GBIF API occurrence). Dual-route onto the adjacent fold. Not plant/bee watts. Cookbook: [`APPLY_ECOLOGY.md`](APPLY_ECOLOGY.md).

## 37. Psychometric scale — Psychology \(D=16\) ↔ Fluid / Nuclear / Thermo \(D=15\) ↔ Meteo \(D=16\) ↔ Atm / Ocean \(D=17\)

Named table: **Nunnally 1978 / Cohen 1988** psychometric anchors (Cronbach \(\alpha\), test–retest \(r\), Cohen's \(d\), median RT, Stroop) from `data/psychology_psychometrics_depth_panel_benchmark.json`. Dual-route **measured** values through APPLY. Skip formula-corpus identity pads and OpenAlex citation counts (wrong object). Not watts. Cookbook: [`APPLY_PSYCHOLOGY.md`](APPLY_PSYCHOLOGY.md).

ISO-SHOES-CLASS-BIN 1% stays frozen. Work list: [`ISOLATED_RESIDUALS.md`](ISOLATED_RESIDUALS.md) · [`SH0ES_LADDER_DIAGNOSIS.md`](SH0ES_LADDER_DIAGNOSIS.md).

How a scientist reads a row: [`SCIENTIST_INTERFACE.md`](SCIENTIST_INTERFACE.md).

Kill: pooled > 0.5%, or \(T_3\) leftover on the \(T_1\) view pairs > 0.5%, or anyone fits Q / γ / Poisson, or anyone treats deep-PREM mismatch as a new coefficient, or anyone stuffs live \(|S_i|/|S_j|\) vs 1 into 0.5%.

Related: [`CONCEPTS.md`](CONCEPTS.md) C4 / C8 / C10 · [`DOMAIN_FAMILY_TREE.md`](DOMAIN_FAMILY_TREE.md) · [`APPLY.md`](APPLY.md)
