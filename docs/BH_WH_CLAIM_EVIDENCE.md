# Black hole → white hole (C2 / C3 / C10) — claim → panel → kill command

**Purpose:** A skeptic who thinks “FSOT has no BH/WH cycle / bubble H₀ / information valve” should be able to **run machines**. This is the map.

**Pin:** **D1D38A** (`vendor/fsot_compute.py`)  
**Picture:** [`CONCEPTS.md`](CONCEPTS.md) **C2** (valve) · **C3** (bubble bleed) · **C10** (valves at every scale)  
**Engine:** `scripts/bubble_bleed_physics.py`

This page is **not** a gadget spec. Warp / portal titles stay on the [names-only tech index](../data/publication/TECH_BLUEPRINTS_REGISTRY.md).

---

## What is already represented (do not re-invent)

| Claim (founding language) | Operational object | Live artifact | n | Residual | Kill |
|---------------------------|--------------------|---------------|--:|----------|------|
| BH is a condenser, not a trash can | POOF / SUCTION / \(C_{\mathrm{eff}}\) cycle | `data/blackhole_whitehole_cycle_live_panel_benchmark.json` | 24 | **0.026472%** | pooled ≤ 0.5% |
| One fluid rate; tools sit in different sectors | \(H_0^{\mathrm{tool}}=H_0^{\mathrm{global}}(1+\rho\varepsilon)\) | `predictions/h0_multi_tool_predictions.json` | **25** tools | Planck **0.024%** | kill a *tool row*, not the sky |
| Global H₀ from Cosmology wave1 | \(H_0^{\mathrm{global}}\approx 68.440\) | same + Quantum replay | 1 | identity vs engine | do not average 67.4 and 73 |
| Bleed fraction | \(\varepsilon=H_0^{\mathrm{global}}/67.4-1\approx 0.015431\) | same | 1 | Cosmology-vs-Planck offset — **not a fit** | pin must still produce 68.440 |
| Planck CMB = depleted sector \(\rho=-1\) | tool row `planck_cmb_local` | Quantum `results/siblings/quantum/h0_tension.json` | 1 | **67.384 vs 67.4 (0.024%)** | 2.5% contested band |
| SH0ES = inflated sector \(\rho=5.05\) | tool row SH0ES | same | 1 | **73.773 vs 73.04 (1.00%)** | stays on the **2.5% contested band** — do **not** stuff into the 0.5% green gate |
| Bubble-bleed cosmology panel | sector / nebula / FRB overlays | `data/cosmology_bubble_bleed_benchmark.json` | 110 | **0.0%** pooled | `audit_all_benchmark_margins.py` |
| Sibling replay (same pin) | FSOT-Quantum H₀ suite | `results/siblings/quantum/H0_TENSION.md` | 3 rows | `overall_ok: true` | `python -m fsot_quantum.h0_tension` |

Valve constants (engine, not new seeds): POOF ≈ 0.1535 · SUCTION ≈ 0.1470 · \(C_{\mathrm{eff}}\) ≈ 0.9577.

PRED-001 (H₀ bridge) stays in `predictions/`. Score the outcome in `results/` when the next survey paper lands. Until then SH0ES **1%** is an honest tool-row residual on the contested band.

---

## One-command kill path

```powershell
python scripts/audit_parameter_count.py
python scripts/audit_all_benchmark_margins.py
```

Then confirm:

1. `BlackHole_WhiteHole_Cycle_Live_Panel` pooled **0.026472%**.  
2. `predictions/h0_multi_tool_predictions.json` still has **25** tools and Planck **0.024%**.  
3. SH0ES is still ~**1.00%** on the **2.5%** contested band — if someone “fixed” it into 0.5% by adding a coefficient, the claim is broken.  
4. `H0_global` is still **68.440** from Cosmology wave1, not an average of the two walls.

If (1)–(4) fail, the BH→WH *operational* claim is broken.

---

## What stays interpretive (do not promote to residual)

| Founding picture | Why it is not a green-gate row |
|------------------|--------------------------------|
| Warp drive / portal hardware | Names-only registry. No unpublished wattages. |
| “We built a white hole in the shop” | Cycle panel scores **invariants**, not a garage device. |
| Every lab-scale orifice is a named astrophysical BH | C10 is the *pattern* (codon / QC collapse / Hubble sector). Do not invent micro-BH catalogs. |

---

## Related

- Conjugate dual: [`MATTER_ANTIMATTER_CLAIM_EVIDENCE.md`](MATTER_ANTIMATTER_CLAIM_EVIDENCE.md)  
- Consciousness: [`CONSCIOUSNESS_CLAIM_EVIDENCE.md`](CONSCIOUSNESS_CLAIM_EVIDENCE.md)  
- Quantum replay: [`../results/siblings/quantum/H0_TENSION.md`](../results/siblings/quantum/H0_TENSION.md)
