#!/usr/bin/env python3
"""Evaluate preregistered open-science holdouts against on-disk benchmarks/caches."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
HOLD = ROOT / "data" / "preregistered_open_science_holdouts.yaml"
SEED = ROOT / "data" / "open_science_seed_constants_benchmark.json"
CONCORD = ROOT / "data" / "open_science_live_concordance_benchmark.json"
INGEST = ROOT / "data" / "open_science_ingest_report.json"
OUT = ROOT / "data" / "open_science_holdout_evaluation.json"


def _load_yaml(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text)
    # minimal fallback for our simple structure if PyYAML missing
    raise RuntimeError("PyYAML required for holdout evaluation (pip install PyYAML)")


def _max_err(rows: list[dict], prefix: str | None = None) -> float | None:
    errs = []
    for r in rows:
        if prefix and not str(r.get("id", "")).startswith(prefix) and prefix not in str(r.get("id", "")):
            if prefix not in str(r.get("name", "")).lower() and prefix not in str(r.get("id", "")).lower():
                continue
        if r.get("error_pct") is None:
            continue
        errs.append(float(r["error_pct"]))
    return max(errs) if errs else None


def main() -> int:
    if not HOLD.exists():
        print(f"missing {HOLD}")
        return 1
    doc = _load_yaml(HOLD)
    seed = json.loads(SEED.read_text(encoding="utf-8")) if SEED.exists() else {"records": []}
    concord = json.loads(CONCORD.read_text(encoding="utf-8")) if CONCORD.exists() else {"records": []}
    ingest = json.loads(INGEST.read_text(encoding="utf-8")) if INGEST.exists() else {}

    seed_rows = seed.get("records") or []
    conc_rows = concord.get("records") or []
    results = []

    for h in doc.get("holdouts") or []:
        hid = h["id"]
        disc = h.get("discriminant") or ""
        status = "fail"
        detail = {}
        if hid == "HOLD-OPEN-001":
            rows = [r for r in seed_rows if r.get("kind") == "seed_vs_nist_codata"]
            mx = _max_err(rows)
            detail = {"n": len(rows), "max_error_pct": mx}
            status = "pass" if rows and mx is not None and mx <= 0.01 else ("skip" if not rows else "fail")
        elif hid == "HOLD-OPEN-001b":
            rows = [r for r in seed_rows if r.get("kind") == "seed_vs_open_literature"]
            mx = _max_err(rows)
            detail = {"n": len(rows), "max_error_pct": mx}
            status = "pass" if rows and mx is not None and mx <= 0.01 else ("skip" if not rows else "fail")
        elif hid == "HOLD-OPEN-002":
            rows = [r for r in seed_rows if r.get("kind") == "seed_math_identity"]
            mx = _max_err(rows)
            detail = {"n": len(rows), "max_error_pct": mx}
            status = "pass" if rows and mx is not None and mx <= 1e-10 else "fail"
        elif hid == "HOLD-OPEN-003":
            rows = [r for r in conc_rows if r.get("id") == "pubchem_aspirin_mw_vs_literature"]
            mx = _max_err(rows)
            detail = {"n": len(rows), "max_error_pct": mx}
            status = "pass" if rows and mx is not None and mx <= 0.5 else ("skip" if not rows else "fail")
        elif hid == "HOLD-OPEN-004":
            rows = [r for r in conc_rows if r.get("id") == "chembl_aspirin_mw_vs_literature"]
            mx = _max_err(rows)
            detail = {"n": len(rows), "max_error_pct": mx}
            status = "pass" if rows and mx is not None and mx <= 0.5 else ("skip" if not rows else "fail")
        elif hid == "HOLD-OPEN-005":
            res = ingest.get("results") or []
            if not res:
                # fall back to stream_ok rows
                ok_rows = [r for r in conc_rows if r.get("kind") == "open_stream_evidence" and float(r.get("error_pct") or 1) == 0]
                total = max(len([r for r in conc_rows if r.get("kind") == "open_stream_evidence"]), 1)
                rate = len(ok_rows) / total
            else:
                ok = sum(1 for r in res if r.get("status") == "ok")
                total = len(res)
                rate = ok / total if total else 0.0
            detail = {"ok_rate": rate, "total": total if res else len(conc_rows)}
            status = "pass" if rate >= 0.90 else "fail"
        else:
            status = "skip"
            detail = {"note": "unknown holdout id"}

        results.append(
            {
                "id": hid,
                "name": h.get("name"),
                "discriminant": disc,
                "status": status,
                "detail": detail,
                "claim": h.get("claim"),
            }
        )

    passed = sum(1 for r in results if r["status"] == "pass")
    failed = sum(1 for r in results if r["status"] == "fail")
    skipped = sum(1 for r in results if r["status"] == "skip")
    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "policy": "no_signup_no_credentials",
        "holdout_file": str(HOLD.relative_to(ROOT)),
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "overall_ok": failed == 0,
        "results": results,
    }
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} pass={passed} fail={failed} skip={skipped} overall_ok={out['overall_ok']}")
    for r in results:
        print(f"  {r['status'].upper():4} {r['id']} {r['name']}")
    return 0 if out["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
