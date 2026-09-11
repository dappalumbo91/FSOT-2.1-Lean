#!/usr/bin/env python3
"""Ledger B null models. Catalog scaling is not a ToE headline.

Four numbers per the hostile-reader spec:
  FSOT residual (file pooled median, then median-of-medians)
  null c=m  (0 by construction — B uses m)
  null c=catalog mean
  null random-domain fold (fsot_correct with a wrong frozen domain)

B may exist as engineering. It may not be cited as evidence the fluid exists
unless it beats catalog-mean and random-fold on held-out rows.
"""
from __future__ import annotations

import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_api_predict_lib import fsot_correct  # noqa: E402
from fsot_precision_constants import AUDIT_EXCLUDED_BENCHMARKS  # noqa: E402

OUT = ROOT / "data" / "ledger_b_null_models.json"
WRONG_FOLD = "Cosmology"
MAX_FILES_FOR_RANDOM = 40
MAX_ROWS_PER_FILE = 8


def _records(doc: dict) -> list[dict]:
    recs = doc.get("records")
    if isinstance(recs, list):
        return [r for r in recs if isinstance(r, dict)]
    return []


def _measured(row: dict) -> float | None:
    for k in ("measured", "target", "anchor"):
        v = row.get(k)
        if isinstance(v, (int, float)):
            return float(v)
    return None


def _err(row: dict) -> float | None:
    v = row.get("error_pct")
    if isinstance(v, (int, float)):
        return abs(float(v))
    return None


def _domain(row: dict, fallback: str) -> str:
    d = row.get("domain") or row.get("fsot_domain") or fallback
    return str(d)


def main() -> int:
    fsot_meds: list[float] = []
    mean_meds: list[float] = []
    rand_meds: list[float] = []
    n_files = 0
    n_rand_files = 0
    for path in sorted((ROOT / "data").glob("*_benchmark.json")):
        if path.name in AUDIT_EXCLUDED_BENCHMARKS:
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        recs = _records(doc)
        if not recs:
            continue
        errs = [e for e in (_err(r) for r in recs) if e is not None]
        ms = [m for m in (_measured(r) for r in recs) if m is not None and m != 0.0]
        if not errs or not ms:
            continue
        n_files += 1
        fsot_meds.append(statistics.median(errs))
        mu = statistics.mean(ms)
        mean_meds.append(statistics.median([abs(m - mu) / abs(m) * 100.0 for m in ms]))
        if n_rand_files >= MAX_FILES_FOR_RANDOM:
            continue
        fallback = str(doc.get("domain") or "Chemistry")
        sample = recs[:MAX_ROWS_PER_FILE]
        rerrs: list[float] = []
        for row in sample:
            m = _measured(row)
            if m is None or m == 0.0:
                continue
            dom = _domain(row, fallback)
            wrong = WRONG_FOLD if dom != WRONG_FOLD else "Biology"
            try:
                _c, e = fsot_correct(m, wrong)
            except Exception:
                continue
            rerrs.append(float(e))
        if rerrs:
            rand_meds.append(statistics.median(rerrs))
            n_rand_files += 1

    def _med(xs: list[float]) -> float | None:
        return float(statistics.median(xs)) if xs else None

    fsot = _med(fsot_meds)
    ident = 0.0
    cat = _med(mean_meds)
    rnd = _med(rand_meds)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ledger": "B",
        "n_files": n_files,
        "n_random_fold_files": n_rand_files,
        "fsot_median_of_medians_pct": fsot,
        "null_identity_cm_error_pct": ident,
        "null_catalog_mean_median_error_pct": cat,
        "null_random_fold_median_error_pct": rnd,
        "beats_identity_cm": False,
        "beats_catalog_mean": (fsot is not None and cat is not None and fsot < cat),
        "beats_random_fold": (fsot is not None and rnd is not None and fsot < rnd),
        "pre_registered_margin_pct": 0.0,
        "cite_as_toe_accuracy": False,
        "note": (
            "null c=m is 0 by construction because Ledger B is c=m(1+|S|f). "
            "B is engineering. Do not quote 477/477 as ToE accuracy. "
            "ToE-paragraph numbers must come from Ledger A fsot_predict."
        ),
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({k: payload[k] for k in payload if k != "note"}, indent=2))
    print(payload["note"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
