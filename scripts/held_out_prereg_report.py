#!/usr/bin/env python3
"""Score preregistered rows on their own. They stay out of the scalar gate.

classify_record returns structural for the preregistered eval kinds, so those
rows never enter the green count. This report does not change that.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from benchmark_margin_lib import (  # noqa: E402
    classify_record,
    gate_error_pct,
    recomputed_relative_error_pct,
)
from fsot_precision_constants import MAX_SCALAR_ERROR_PCT  # noqa: E402

DATA = ROOT / "data"
FREEZE = ROOT / "predictions" / "toe_prereg_freeze.json"
OUT = DATA / "held_out_prereg_report.json"
PREREG_EVAL = frozenset(
    {
        "w0_live",
        "wa_preregistered",
        "h0_live",
        "preregistered_falsifiable",
        "preregistered_certificate",
    }
)


def _records(doc: dict) -> list[dict]:
    recs = doc.get("material_records") or doc.get("records") or []
    if not isinstance(recs, list):
        return []
    return [r for r in recs if isinstance(r, dict)]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _row_name(rec: dict) -> str:
    for key in ("name", "id", "property", "observable"):
        if rec.get(key):
            return str(rec[key])
    return ""


def main() -> int:
    freeze_raw = json.loads(FREEZE.read_text(encoding="utf-8"))
    freeze_sha = _sha256(FREEZE)
    sectors = freeze_raw.get("sector_predictions") or []
    sector_ids = {str(row.get("id")) for row in sectors if row.get("id")}

    by_file: dict[str, dict] = {}
    matched_ids: set[str] = set()
    excluded = 0
    still_gated = 0
    scored = 0
    within = 0
    outside = 0
    unscored = 0
    outliers: list[dict] = []

    for path in sorted(DATA.glob("*_benchmark.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        file_hit = "prereg" in path.name.lower()
        file_row = None
        for rec in _records(doc):
            kind = str(rec.get("eval_kind") or "").lower()
            name = _row_name(rec)
            id_hit = name in sector_ids or str(rec.get("prediction_id") or "") in sector_ids
            if not file_hit and kind not in PREREG_EVAL and not id_hit:
                continue
            if file_row is None:
                file_row = {
                    "file": path.name,
                    "sha256": _sha256(path),
                    "rows": 0,
                    "excluded_from_scalar_gate": 0,
                    "still_in_scalar_gate": 0,
                    "scored": 0,
                    "within_half_pct": 0,
                    "outside_half_pct": 0,
                    "unscored": 0,
                }
            klass = classify_record(rec, file_name=path.name)
            file_row["rows"] += 1
            if klass == "scalar":
                file_row["still_in_scalar_gate"] += 1
                still_gated += 1
            else:
                file_row["excluded_from_scalar_gate"] += 1
                excluded += 1
            err, reason = gate_error_pct(rec)
            recomputed = recomputed_relative_error_pct(rec)
            if name in sector_ids:
                matched_ids.add(name)
            if str(rec.get("prediction_id") or "") in sector_ids:
                matched_ids.add(str(rec["prediction_id"]))
            if err is None and recomputed is None:
                file_row["unscored"] += 1
                unscored += 1
                continue
            used = recomputed if recomputed is not None else err
            file_row["scored"] += 1
            scored += 1
            flag = "within" if used is not None and used <= MAX_SCALAR_ERROR_PCT else "outside"
            if flag == "within":
                file_row["within_half_pct"] += 1
                within += 1
            else:
                file_row["outside_half_pct"] += 1
                outside += 1
                if len(outliers) < 40:
                    outliers.append(
                        {
                            "file": path.name,
                            "name": name,
                            "eval_kind": kind,
                            "classify": klass,
                            "gate_error_pct": err,
                            "gate_reason": reason,
                            "recomputed_error_pct": recomputed,
                        }
                    )
        if file_row is not None:
            by_file[path.name] = file_row

    sector_rows = []
    for row in sectors:
        sid = str(row.get("id") or "")
        sector_rows.append(
            {
                "id": sid,
                "fsot_predicted": row.get("fsot_predicted"),
                "unit": row.get("unit"),
                "kill": row.get("kill"),
                "future_survey": row.get("future_survey"),
                "matched_benchmark_row": sid in matched_ids,
            }
        )

    report = {
        "purpose": (
            "Scores preregistered and held-out rows on their own. "
            "An explicit record_kind of scalar is honored before the preregistered "
            "eval_kind check, so those rows remain in the scalar gate. "
            "Rows that reach the preregistered eval_kind check return structural "
            "and stay out of the green count."
        ),
        "half_pct_band": MAX_SCALAR_ERROR_PCT,
        "freeze_ref": {
            "path": FREEZE.relative_to(ROOT).as_posix(),
            "freeze_id": freeze_raw.get("freeze_id"),
            "frozen_at": freeze_raw.get("frozen_at"),
            "review_horizon": freeze_raw.get("review_horizon"),
            "sha256": freeze_sha,
            "pin_text": "D1D38A",
            "note": "Hash and date are read from the freeze file. This report does not edit it.",
        },
        "rows_seen": excluded + still_gated,
        "excluded_from_scalar_gate": excluded,
        "still_in_scalar_gate": still_gated,
        "scored": scored,
        "within_half_pct": within,
        "outside_half_pct": outside,
        "unscored_missing_pair": unscored,
        "sector_predictions": sector_rows,
        "sector_predictions_without_a_benchmark_row": [
            row["id"] for row in sector_rows if not row["matched_benchmark_row"]
        ],
        "by_file": list(by_file.values()),
        "outliers_outside_half_pct": outliers,
    }
    text = json.dumps(report, indent=2, allow_nan=False) + "\n"
    OUT.write_bytes(text.encode("utf-8"))
    print(
        "rows",
        report["rows_seen"],
        "excluded",
        excluded,
        "still_gated",
        still_gated,
        "scored",
        scored,
        "within",
        within,
        "outside",
        outside,
        "unscored",
        unscored,
        "files",
        len(by_file),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
