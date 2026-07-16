# FSOT Circuitry & Component Emergence Spine

*Tier 96 design scaffold · 2026-07-16 · [Return to main thesis](../README.md#97-circuitry-component-emergence-roadmap)*

> **Goal:** Label every schematic variable and industry component class so seed-derived FSOT readouts **emerge a bill of materials** from parametric availability — work smarter, not harder. No guessed resistor values; arithmetic + catalog tables.

## 1. Why this domain

FSOT already closes electrical and wiring panels at sub-percent precision. The next step is **intrinsic emergence**: when the math demands a build, the repository names the parts.

| Existing verified panel | Records | Pooled median |
|-------------------------|--------:|--------------:|
| `Electrical_Power_Systems` | 24 | 0.016% | verified panel |
| `Desktop_Application_Wiring_Spine` | 81 | 0.000% | verified panel |
| `Trinary_Hardware_Live_Panel` | 28 | 0.015% | verified panel |

**Manifest:** `data/circuit_component_emergence_manifest.yaml`

## 2. Component variable atlas (Phase 0)

Every designator class maps to measurable variables and industry parametric search keys:

| Class | Designators | FSOT variables | Industry refs |
|-------|-------------|----------------|---------------|
| resistor | R | `resistance_ohm`, `tolerance_pct`, `power_w`, `tcr_ppm` | IEC 60115, EIA-96, Digi-Key parametric |
| capacitor | C | `capacitance_f`, `esr_ohm`, `voltage_v`, `dielectric` | Murata catalogs, KEMET, IEC 60384 |
| inductor | L | `inductance_h`, `dcr_ohm`, `saturation_a`, `q_factor` | — |
| semiconductor | Q, U, D | `vce_sat`, `hfe`, `vgs_th`, `rdson`, `bandwidth_hz` | ON Semi, TI, Infineon datasheets |
| power | PS, J | `vin_v`, `vout_v`, `iout_a`, `efficiency`, `ripple_mv` | — |

## 3. Seed routing (no per-part tuning)

| Field | Value |
|-------|-------|
| Lean route | `material` |
| Formula branches | `term2.baseline_trend, term1.perceived_adjust, term3.acoustic_bleed` |
| Seed-only policy | `True` |

Routing coordinates (`D_eff`, `δψ`, `quirk_mod`) select component **classes** and tolerance bands; numeric values emerge from strict-empirical rows, not hand-entered BOM guesses.

## 4. Planned panels (not yet benchmarked)

- `Circuit_Component_Emergence_Panel`
- `Schematic_Netlist_Intrinsic_Panel`
- `BOM_Industry_Availability_Panel`

## 5. Emergence pipeline (target)

```
schematic netlist → variable labels → FSOT scalar @ seed folds
    → industry parametric filter (Digi-Key/Mouser class tables)
    → ranked BOM lines + tolerance proof
```

**Next scripts (Phase 1):**

```bash
python scripts/ingest_circuit_component_catalogs.py      # planned
python scripts/build_circuit_component_emergence_benchmarks.py
python scripts/gen_circuit_component_emergence_lean.py
```

## 6. Relation to wet-lab longevity

Tier 94/95 longevity panels established the **measured-biology → seed prediction** pattern. Tier 96 reuses that pattern for **measured-electrical** targets (NIST CODATA, IEEE grid specs, datasheet anchors).

See [`WETLAB_LONGEVITY_DEPTH.md`](WETLAB_LONGEVITY_DEPTH.md) and [`CREDIBILITY_HARDENING_AUDIT.md`](../data/publication/CREDIBILITY_HARDENING_AUDIT.md).

## 7. ESP32 / trinary hardware (deferred)

Physical ESP32 eight-way closure remains **convenience-deferred** (boot-sequence ergonomics). QEMU bare-metal and `Trinary_Hardware_Live_Panel` simulation benchmarks remain authoritative until laptop-bench workflow is ready.
