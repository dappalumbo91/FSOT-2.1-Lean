# APPLY cookbook — Thermodynamics fold

**Pin:** D1D38A · **core:** `Thermodynamics` · \(D_{\mathrm{eff}}=15\) · `observed=True` · \(C=\gamma/e\) · \(\delta\psi=0.9\) · hits=1.  
**Ceiling zoom:** `Cosmology` \(D=25\) (same fridge cycle). Tissue: [`SCALE_INTERCONNECT_PHYSICS.md`](SCALE_INTERCONNECT_PHYSICS.md) §3.  
**Same rung:** `Nuclear_Physics` (orifice); `Fluid_Dynamics` (dark tank).  
**Neighbor:** `Condensed_Matter` \(D=14\) (solid).  
**General protocol:** [`APPLY.md`](APPLY.md). BH→WH is a heat/information pump, not a second cosmology.

---

## 1. Name the measured object

| Object | Public table | Not |
|--------|--------------|-----|
| Carnot COP | HVAC literature pairs (0/27 °C, 5/35 °C, 10/40 °C, −10/20 °C) | A fitted \(\eta\) as HVAC efficiency |
| Metal \(T_m\) | CRC (Al, Cu, Fe, Au, Ag, Pb) | A per-metal Lindemann \(c\) |
| Valve fraction | POOF/(POOF+SUCTION) vs 1/2 | A 0.5% HVAC \(\eta\) |

Wrong object: live \(\lvert S_{\mathrm{thermo}}/S_{\mathrm{cosm}}\rvert\) vs 1. Score vs \(\pi/2\). Live vs Fluid is the dark/observed mix.

---

## 2. Pick the interface

Thermo is the **heat** zoom of the \(D=15\) tank. Cosmology is the **ceiling** zoom of the same fridge. Nuclear is the **orifice** look. Fluid is the **tank** look (dark). CM is the **solid** on the adjacent rung.

---

## 3. Route

```text
S = domain_scalar("Thermodynamics")        # D=15, δψ=0.9
computed, err% = fsot_scaled(COP, "Thermodynamics")
```

Fridge-cycle test:

```text
|S_thermo|/|S_cosm|  vs  π/2
```

| Handle | Form | Use |
|--------|------|-----|
| Carnot COP | \(T_h/(T_h-T_c)\) dual-routed | HVAC pairs on Thermo and Nuclear / Fluid |
| Fridge | \(\lvert S_T/S_C\rvert\) vs \(\pi/2\) | BH→WH heat pump |
| Solid vs heat | same-look \(D=14/15\) at \(\delta\psi=0.5\) | CRC metal \(\rho\) vs \(T_m\) |
| Valve fraction | POOF/(POOF+SUCTION) vs 1/2 | literature band, not HVAC \(\eta\) |

---

## 4. Green gate

Domain **median** ≤ **0.5%**. Carnot dual-route and \(\lvert S_T/S_C\rvert\) vs \(\pi/2\) (~0.289%) are the tight scalars. Valve fraction stays a **literature band**. Live vs Fluid is **structural**.

---

## 5. If it fails

| Symptom | Do this | Do not |
|---------|---------|--------|
| COP ugly | Check \(T\) in kelvin, literature pair | A fitted \(\eta\) |
| Live vs Cosmology vs 1 | Score vs \(\pi/2\) | Stuff a new fridge coefficient |
| Valve vs 1/2 off | Literature band | Call it HVAC efficiency |

Worked interconnect: `python scripts/build_scale_interconnect_benchmark.py`

Kill: a fitted COP; stuffing live vs 1; retuning \(\delta\psi=0.9\).
