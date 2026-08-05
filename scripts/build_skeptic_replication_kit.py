#!/usr/bin/env python3
"""15-minute skeptic replication path — numbers from live status/margin audit."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "SKEPTIC_REPLICATION_KIT.md"
STATUS = ROOT / "data" / "repo_status_snapshot.json"
MARGIN = ROOT / "data" / "benchmark_margin_audit.json"
CROSS = ROOT / "data" / "cross_proof_verification_report.json"
TOE = ROOT / "data" / "toe_gap_closure_report.json"


def _git_head() -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        return r.stdout.strip()[:12]
    except Exception:
        return "unknown"


def _load(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    st = _load(STATUS)
    mg = _load(MARGIN)
    cp = _load(CROSS)
    toe = _load(TOE)
    emp = st.get("empirical") or {}
    auth = st.get("authority") or {}
    mp = st.get("multiprover") or {}
    g = mg.get("green_gate_pass_count", emp.get("green_gate_pass_count", "?"))
    n = mg.get("benchmark_file_count", emp.get("benchmark_file_count", "?"))
    pin = auth.get("pin_prefix", "D1D38A")
    pin_ok = auth.get("pin_match", "?")
    overall = mp.get("overall_ok", cp.get("overall_ok", "?"))
    label_a = (toe.get("evaluation") or {}).get("label_A_empirical_framework", "?")
    label_b = (toe.get("evaluation") or {}).get("label_B_classical_toe", "?")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    head = _git_head()

    body = f"""# FSOT Skeptic Replication Kit

*15-minute verification path · {ts} · commit `{head}`*

Run this if you want to **break FSOT fast** — not read 12,000 lines of narrative first.

**Live authority:** pin **{pin}** (match={pin_ok}) · green **{g}/{n}** · multiprover overall_ok={overall}  
Full human guide: [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) · audience map: [`DOCUMENTATION_MAP.md`](DOCUMENTATION_MAP.md) · math: [`FSOT_MATH_KEY.md`](FSOT_MATH_KEY.md)

Plain-language ladder: [`CLEAR_PATH_FOR_INDEPENDENTS.md`](CLEAR_PATH_FOR_INDEPENDENTS.md) ·  
Claim tiers: [`RESIDUAL_HONESTY_AND_CLAIM_TIERS.md`](RESIDUAL_HONESTY_AND_CLAIM_TIERS.md) ·  
Status snapshot: [`CURRENT_STATUS.md`](CURRENT_STATUS.md)

## Step 1 — Clone and install (~2 min)

```bash
git clone https://github.com/dappalumbo91/FSOT-2.1-Lean.git
cd FSOT-2.1-Lean
pip install -r requirements.txt
```

## Step 2 — Status + green gate (~3–10 min)

```bash
python scripts/build_repo_status_snapshot.py
python scripts/audit_all_benchmark_margins.py
python scripts/audit_parameter_count.py
```

**Expect (at generation of this kit):**

| Check | Expected |
|-------|----------|
| Pin | **{pin}** with `pin_match: true` in `docs/CURRENT_STATUS.md` |
| Benchmark green | **{g}/{n}** fail 0 (`data/benchmark_margin_audit.json`) |
| Gate | pooled median ≤ **0.5%** |
| Parameter audit | **ZERO_FREE** |
| Label A / B (if toe report present) | A={label_a}, B={label_b} |

Optional one-command publication bundle:

```bash
python scripts/run_publication_verification_bundle.py
```

## Step 3 — Spot-check three domains (~3 min)

```bash
python scripts/reproduce_domain_panel.py --panel Fuel_Lab_Live_Panel --deep
python scripts/query_fsot_domain_navigator.py --intent cosmology_cmb
python scripts/query_fsot_domain_navigator.py --query hubble
```

**Expect:** Fuel Lab pooled ≤0.5%; cosmology/Hubble panels present.

## Step 4 — Near-miss transparency (~1 min)

```bash
python scripts/build_benchmark_near_miss_ledger.py
```

Open `data/publication/BENCHMARK_NEAR_MISS_LEDGER.md` — worst green domains published openly.

## Step 5 — Formal spine (optional, longer)

```bash
python scripts/run_cross_proof_verification.py
```

**Expect when toolchains installed:** `overall_ok: true` in `data/cross_proof_verification_report.json`  
(at kit generation: multiprover overall_ok={overall}).

## What would falsify FSOT?

1. Any active benchmark fails green gate after fresh clone (no local edits).
2. `overall_ok: false` in cross-proof report with provers installed.
3. Authority pin leaves D1D38A without a documented migration.
4. Preregistered prediction PRED rows violated after manifest-locked registration.
5. Parameter audit finds per-observable least-squares tuning.

## Artifacts to cite

- `docs/CURRENT_STATUS.md` / `data/repo_status_snapshot.json`
- `data/benchmark_margin_audit.json`
- `data/publication_claims_manifest.json`
- `data/cross_proof_verification_report.json`
- `data/publication/domain_atlas.csv`
- Math key: [`FSOT_MATH_KEY.md`](FSOT_MATH_KEY.md)
- Main thesis: [`README.md`](../README.md)

Regenerate this kit: `python scripts/build_skeptic_replication_kit.py`  
(after `python scripts/build_repo_status_snapshot.py` and margin audit).
"""
    OUT.write_text(body.strip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT} green={g}/{n} pin={pin}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
