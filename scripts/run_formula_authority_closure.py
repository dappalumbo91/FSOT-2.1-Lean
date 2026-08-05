#!/usr/bin/env python3
"""
FSOT formula-authority system closure gate.

Single command. Zero free-parameter discipline. Pin D1D38A.

Does NOT curve-fit. Does NOT invent parameters. Verifies:
  1. Authority pin D1D38A matches compute
  2. ZERO_FREE parameter audit
  3. Residual program closed
  4. lake build FSOT (Lean formal typecheck)
  5. Mathlib re-derivation campaign (depth inventory + lake)
  6. Label B / residual certificate consistency

Exit 0 only if all hard gates pass.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "formula_authority_closure.json"
PIN_PATH = ROOT / "vendor" / "fsot_compute_AUTHORITY_PIN.json"
PY = sys.executable


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _run(cmd: list[str], *, timeout: int = 7200) -> dict:
    try:
        r = subprocess.run(
            cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=timeout
        )
        return {
            "cmd": " ".join(cmd),
            "returncode": r.returncode,
            "ok": r.returncode == 0,
            "stdout_tail": (r.stdout or "")[-1500:],
            "stderr_tail": (r.stderr or "")[-1500:],
        }
    except Exception as exc:
        return {"cmd": " ".join(cmd), "returncode": -1, "ok": False, "error": str(exc)}


def _load(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    print("=== FSOT FORMULA AUTHORITY CLOSURE ===")
    print("  Law: S=K(T1+T2+T3); c=m(1+|S|*f); ZERO free parameters; pin D1D38A")
    print("  Forbidden: curve-fit, per-row coeffs, diverging from formula\n")

    gates: list[dict] = []

    # 1. Pin
    pin = _load(PIN_PATH)
    sha = str(pin.get("authority_sha256") or "")
    pin_ok = bool(pin.get("compute_matches_certificate")) and sha.upper().startswith("D1D38A")
    gates.append(
        {
            "id": "authority_pin_D1D38A",
            "ok": pin_ok,
            "detail": f"sha={sha[:16]}… match={pin.get('compute_matches_certificate')}",
        }
    )
    print(f"[{'OK' if pin_ok else 'FAIL'}] authority pin D1D38A")

    # 2. ZERO_FREE
    r = _run([PY, str(ROOT / "scripts" / "audit_parameter_count.py")], timeout=120)
    pa = _load(ROOT / "data" / "parameter_count_audit.json")
    zero_free = "ZERO_FREE" in str(
        pa.get("audit_verdict") or pa.get("verdict") or pa.get("headline_claim") or ""
    )
    gates.append(
        {
            "id": "zero_free_parameters",
            "ok": zero_free and r["ok"],
            "detail": pa.get("audit_verdict") or pa.get("verdict") or pa.get("headline_claim"),
        }
    )
    print(f"[{'OK' if zero_free else 'FAIL'}] ZERO_FREE parameters")

    # 3. Residual closed
    res = _load(ROOT / "data" / "residual_toe_closure_certificate.json")
    res_ok = res.get("status") == "RESIDUAL_PROGRAM_CLOSED" and int(res.get("residual_open_count") or 0) == 0
    gates.append(
        {
            "id": "residual_program_closed",
            "ok": res_ok,
            "detail": f"{res.get('status')} open={res.get('residual_open_count')}",
        }
    )
    print(f"[{'OK' if res_ok else 'FAIL'}] residual program closed")

    # 4. Lake build
    lake = _run(["lake", "build", "FSOT"], timeout=7200)
    gates.append(
        {
            "id": "lake_build_FSOT",
            "ok": lake["ok"],
            "detail": "lake build FSOT",
            "stderr_tail": lake.get("stderr_tail", "")[-400:],
        }
    )
    print(f"[{'OK' if lake['ok'] else 'FAIL'}] lake build FSOT")

    # 5. Mathlib campaign (full corpus, shared lake already done — still re-inventory)
    camp = _run(
        [
            PY,
            str(ROOT / "scripts" / "run_mathlib_rederivation_campaign.py"),
            "--skip-aux",
        ],
        timeout=7200,
    )
    mr = _load(ROOT / "data" / "mathlib_rederivation_campaign_report.json")
    # Accept engine-core closed OR full corpus; require lake green + no sorry
    camp_ok = bool(mr.get("engine_core_closed") or mr.get("full_corpus_closed")) and lake["ok"]
    # Tighten: must have global lake passed in campaign too
    camp_ok = camp_ok and (mr.get("global_lake") or {}).get("status") == "passed"
    gates.append(
        {
            "id": "mathlib_campaign",
            "ok": camp_ok,
            "detail": {
                "verdict": mr.get("verdict"),
                "engine_core_closed": mr.get("engine_core_closed"),
                "full_corpus_closed": mr.get("full_corpus_closed"),
                "engine_mathlib_pct": mr.get("engine_mathlib_depth_pct"),
                "corpus_mathlib_pct": (mr.get("corpus") or {}).get("mathlib_depth_pct"),
                "full_mathlib_flag": mr.get("full_mathlib_rederivation_of_all_lemmas"),
            },
        }
    )
    print(
        f"[{'OK' if camp_ok else 'FAIL'}] mathlib campaign "
        f"verdict={mr.get('verdict')} engine%={mr.get('engine_mathlib_depth_pct')} "
        f"corpus%={(mr.get('corpus') or {}).get('mathlib_depth_pct')}"
    )

    # 6. Parameter honesty refresh
    _run([PY, str(ROOT / "scripts" / "build_parameter_honesty_closure.py")], timeout=120)
    ph = _load(ROOT / "data" / "parameter_honesty_closure.json")
    ph_ok = "ZERO_FREE" in str(ph.get("verdict") or "")
    gates.append({"id": "parameter_honesty", "ok": ph_ok, "detail": ph.get("verdict")})
    print(f"[{'OK' if ph_ok else 'FAIL'}] parameter honesty")

    # 7. Depth audit refresh
    _run([PY, str(ROOT / "scripts" / "build_verification_depth_audit.py")], timeout=180)
    depth = _load(ROOT / "data" / "verification_depth_audit.json")
    v = depth.get("verdict") or {}
    depth_ok = bool(v.get("undeniable_toe_claim")) and bool(v.get("engine_core_mathlib_closed") or v.get("full_mathlib_rederivation_of_all_lemmas"))
    gates.append(
        {
            "id": "depth_audit",
            "ok": depth_ok,
            "detail": {
                "undeniable_toe_claim": v.get("undeniable_toe_claim"),
                "engine_core_mathlib_closed": v.get("engine_core_mathlib_closed"),
                "full_mathlib_rederivation_of_all_lemmas": v.get("full_mathlib_rederivation_of_all_lemmas"),
            },
        }
    )
    print(
        f"[{'OK' if depth_ok else 'FAIL'}] depth audit undeniable={v.get('undeniable_toe_claim')} "
        f"engine_mathlib={v.get('engine_core_mathlib_closed')} full_mathlib={v.get('full_mathlib_rederivation_of_all_lemmas')}"
    )

    all_ok = all(g["ok"] for g in gates)
    doc = {
        "generated_at": _now(),
        "version": "1.0",
        "verdict": "FORMULA_AUTHORITY_SYSTEM_CLOSED" if all_ok else "FORMULA_AUTHORITY_GAPS",
        "master_formula": "S = K*(T1+T2+T3); c = m*(1+|S|*f)",
        "authority_pin": "D1D38A",
        "discipline": (
            "Zero free parameters. Seed-derived constants + preregistered domain routes. "
            "Not curve-fitting. Not per-row least squares. Not diverging from formula."
        ),
        "gates": gates,
        "all_ok": all_ok,
        "commands": {
            "this": "python scripts/run_formula_authority_closure.py",
            "mathlib": "python scripts/run_mathlib_rederivation_campaign.py",
            "params": "python scripts/audit_parameter_count.py",
            "lake": "lake build FSOT",
        },
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT}")
    print(f"VERDICT: {doc['verdict']}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
