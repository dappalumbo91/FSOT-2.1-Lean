# Engineering, hardware, code — direction note

**Date:** 2026-08-03  
**Status:** active build path (Living FSOT hardware + VL-agent distill **parked**)

---

## What we are building toward

1. **Circuit / ESP32 engineering** — absolute rails (3.3 V, current, clocks, pull-ups, RC, LDO/buck) so BOM and bring-up are seed-grounded, not wall-banging.
2. **Coding structure verifier** — same *class* of panel as linguistics / Protofluid / code-genome: structure, parity, genome stats — **not** importing transformer weights into the seed spine.
3. **Neuron-zig bridge** — live bio-accurate mind stack on `I:\fsot-neuron-zig` (Lean wet-lab certificate, 0 free params on scalar path). Replaces “Living FSOT hardware” as the embodiment/bio direction.

---

## Parked / redirected

| Old panel | Status | Redirect |
|-----------|--------|----------|
| Living FSOT hardware | Parked | **fsot-neuron-zig** (running mind + Lean stamps) |
| VL agent distill | Parked | LLM architecture is free-param opposite of seed-closed FSOT |

---

## LLM architecture — honest cognitive map

Large language models are **large free-parameter function approximators**. FSOT’s core law is **zero free fit parameters** on the seed spine.

That is a real architectural opposition, not a temporary bug:

| | FSOT seed spine | Autoregressive LLM |
|--|-----------------|---------------------|
| Parameters | Closed seeds (π,e,φ,…) | 10⁹–10¹² fitted weights |
| Goal | Derive / residual-gate | Fit next-token distribution |
| Failure mode | Wrong *comparison object* | Shortcut / hallucination / brittleness |

### Approaches that stay honest

1. **Do not absorb weights into the seed spine.** That would break the zero-free-param claim.
2. **Optional secondary “potential / interface” layer** (your idea): connective tissue *between* systems — routing, attention *gates*, or interface indices derived from multi-sector coupling — **not** a replacement for seeds. Weights live only in that secondary layer, clearly labeled.
3. **Use FSOT where it is native:** verify structure of *code*, languages, hardware rails, biology (neuron-zig), and *steer* tools with seed metrics — without claiming the LLM *is* FSOT.
4. **Code verifier path** already half-built: `fsot code language` multi-lang parity, Protofluid densify exact rates, Tier I programming laws + OSS code-genome.

### What “solving LLM problems” might mean without free params in the core

- Seed-derived **kill criteria** for when a generation is out of band  
- **Structure** of token/operator maps (you already have language operator maps)  
- **Hardware** that runs fixed-point / trinary / Zig minds (neuron-zig), not GPU weight farms  
- Interface layer for *routing* among tools — potential between systems, not a third Yukawa fit

---

## Commands

```powershell
python -c "import sys; sys.path.insert(0,'scripts'); from engineering_code_bridge_lib import *; import json; from pathlib import Path
for name, fn in BUILDERS.items():
  d=fn(); p=output_path(name); p.write_text(json.dumps(d, indent=2), encoding='utf-8'); print(name, d.get('record_count'), d.get('median_error_pct'))"
python scripts/audit_all_benchmark_margins.py
```

---

## External paths referenced

- `I:\fsot-neuron-zig` — live bio mind + Lean wet-lab certificate  
- `I:\Protofluid-Language-Translator-2.0-Zig` — multi-lang densify ship baseline  
- `Desktop\fsot code language` — multi-implementation FSOT language parity  
- `verification/esp32/fsot_esp32_observer` — existing ESP32 Rust observer firmware  
