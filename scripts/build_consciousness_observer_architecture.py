#!/usr/bin/env python3
"""Generate Consciousness Observer Architecture — local stack, ESP32 deferred."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "CONSCIOUSNESS_OBSERVER_ARCHITECTURE.md"
PIPELINE = ROOT / "data" / "practical_pipeline_manifest.yaml"
INTUITIVE = ROOT / "data" / "intuitive_observation_fsot_map.yaml"


def _load_yaml(path: Path) -> dict:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8")) if path.is_file() else {}


def _bench_summary(path: Path) -> str:
    if not path.is_file():
        return "—"
    doc = json.loads(path.read_text(encoding="utf-8"))
    pool = doc.get("pooled_median_error_pct")
    rc = doc.get("record_count", "?")
    if pool is None:
        return f"{rc} records"
    return f"{rc} records · {float(pool):.4f}% pooled"


def build(ts: str) -> str:
    pipe = _load_yaml(PIPELINE)
    coa = pipe.get("consciousness_observer_architecture") or {}
    return f"""# Consciousness Observer Architecture (Local)

*Generated: {ts} · [Return to practical pipeline](PRACTICAL_PIPELINE.md)*

> **Local-first embodiment.** QEMU Living FSOT + desktop sensory observer loop. **ESP32 UART closure deferred** — not a math gap, a workflow convenience choice.

## 1. Architecture overview

```
Desktop sensors (mic / camera / keyboard timing)
        ↓
Observer flag: quirk_mod(observed=true) + consciousness_factor
        ↓
Seed scalar engine (vendor/fsot_compute.py) — ZERO_FREE
        ↓
Living FSOT QEMU trinary body + Rust mind gym
        ↓
FluidLink FPC timing spine (local sync, no cloud)
        ↓
Lean 4 priors → five-prover cross-check
```

## 2. Observer loop (software — start here locally)

| Layer | Component | Role |
|-------|-----------|------|
| Scalar | `raw_S = term1×quirk_mod + term2 + term3` | Seed-derived vitality readout |
| Coupling | `quirk_mod(observed=true)` | Measurement modulates term1 |
| Consciousness | `consciousness_factor`, `E_con` | Brain-power anchor (~21.79 W) |
| Sensory | Timing + display proxy + repo hash (no mic/camera) | Desktop software observer; mic/camera/ESP32 deferred |
| Runtime | Living FSOT QEMU | Closed-loop hardware verification |
| Timing | FluidLink FPC + Kronos | Private local time spine |

**Reproduce observer panels:**

```bash
python scripts/run_desktop_observer_loop.py
python scripts/build_fluidlink_local_bundle.py
python scripts/audit_living_fsot_hardware.py
```

## 3. Verified panels (current)

| Panel | Status |
|-------|--------|
| Living FSOT Hardware | {_bench_summary(ROOT / 'data/living_fsot_hardware_panel_benchmark.json')} |
| Trinary Hardware Live (sim) | {_bench_summary(ROOT / 'data/trinary_hardware_live_panel_benchmark.json')} |
| Consciousness expansion spine | {_bench_summary(ROOT / 'data/consciousness_expansion_spine_benchmark.json')} |
| FPC FluidLink timing | {_bench_summary(ROOT / 'data/fpc_temporal_coupling_benchmark.json')} |
| Longevity ↔ consciousness | {_bench_summary(ROOT / 'data/longevity_consciousness_coupling_panel_benchmark.json')} |

## 4. Dual identity / hybrid evolution (symbolic → testable)

The founding "dual identity / expanded awareness" cluster maps to:

- **Soul bridge:** `FSOT.Formal.ConsciousnessSoulBridgePriors` (234k+ Soul Simulator records)
- **Trinary embodiment:** simulation-first `Trinary_Hardware_Live_Panel` — not boot-button ESP32
- **Lean route credibility:** `consciousness_lean_route_credibility_benchmark.json`

See [`data/intuitive_observation_fsot_map.yaml`](../data/intuitive_observation_fsot_map.yaml) observation `dual_identity_hybrid`.

## 5. FluidLink — local private comms pattern

FluidLink is **not** a cloud SaaS — it is the FPC timing hub that couples local domains without subscription:

- Hub: `Time_Emergence_Simulation` → spine targets via `fluidlink_fpc_timing` edges
- Panel: `FPC_Temporal_Coupling` (Tier 50)
- Desktop anchor: **Kronos** spacetime ticker project

```bash
python scripts/build_tier_o_time_emergence_benchmarks.py
python scripts/build_domain_coupling_simulation.py
```

**Ownership principle:** data stays on device; reproducible from `vendor/` caches.

## 6. What we skip (explicit)

| Deferred | Authoritative substitute |
|----------|-------------------------|
| ESP32 boot-button flash | Living FSOT QEMU + Trinary simulation panel |
| Cloud observer APIs | Local fsot_compute + desktop sensors |
| Subscription mesh | FluidLink FPC local timing |

## 7. Next local build steps

1. Wire desktop sensor script → `observed=true` batch in fsot_compute replay
2. Expand X-style predictions in applied domains (AI coherence, fluid dynamics panels)
3. Per-blueprint numeric audit via [`TECH_BLUEPRINTS_REGISTRY.md`](../data/publication/TECH_BLUEPRINTS_REGISTRY.md)
4. Kaggle / R&D packaging after credibility depth bundle green

**Orchestrator:** `python scripts/build_practical_pipeline_bundle.py`
"""


def main() -> int:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    OUT.write_text(build(ts), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())