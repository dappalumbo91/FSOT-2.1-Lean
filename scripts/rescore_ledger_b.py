#!/usr/bin/env python3
"""Re-score stored Ledger B rows with the live law. Does not overwrite them.

Live law: c = m (1 + |S| ALPHA), S from vendor/fsot_compute.py (pin AEB2AD).
Stored rows that predate that law keep their values. This report is the
side-by-side count for Damian. Replacing stored values is a separate decision.
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from benchmark_margin_lib import is_ledger_b_scale_step  # noqa: E402
from fsot_api_predict_lib import fsot_correct, round_sig  # noqa: E402

DATA = ROOT / "data"
OUT = DATA / "ledger_b_rescore_report.json"

# Factors seen on rows written before f was ALPHA for every domain.
LEGACY_FACTORS = (
    0.0002,
    0.00025,
    0.0003,
    0.00035,
    0.0004,
    0.0005,
    0.0008,
    0.001,
)


def _law_history() -> dict:
    """Commit that made the writer amplitude ALPHA, if git can see it."""
    try:
        log = subprocess.run(
            [
                "git",
                "log",
                "-1",
                "--format=%H %cI %s",
                "-S",
                "Ledger B amplitude is ALPHA",
                "--",
                "scripts/fsot_api_predict_lib.py",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        line = (log.stdout or "").strip()
    except OSError as exc:
        return {"inferred": False, "error": str(exc)}
    if not line:
        return {
            "inferred": False,
            "note": "No commit message search hit for the ALPHA amplitude switch.",
        }
    parts = line.split(" ", 2)
    return {
        "inferred": True,
        "alpha_writer_commit": parts[0],
        "alpha_writer_committed_at": parts[1] if len(parts) > 1 else None,
        "subject": parts[2] if len(parts) > 2 else "",
        "note": (
            "Rows that match c = m(1+|S|ALPHA) are labeled AEB2AD-ALPHA. "
            "Rows whose implied factor is one of the older per-domain constants "
            "are labeled pre-ALPHA-domain-table. Stored files were not rewritten."
        ),
    }


def _close(stored: float, live: float) -> bool:
    """True when the stored value is the live value at writer precision.

    An absolute tolerance of 5e-7 would call a 1e-4 row a match when the
    relative gap is still a different factor. Use relative agreement, or an
    exact hit on the old absolute rounding.
    """
    if stored == round(live, 6) or (abs(live) >= 1e6 and stored == round(live, 4)):
        return True
    if stored == round_sig(live):
        return True
    scale = max(abs(stored), abs(live))
    if scale == 0.0:
        return True
    return abs(stored - live) / scale <= 1e-6


def _legacy_factor(computed: float, measured: float, scalar: float | None) -> float | None:
    if measured == 0.0 or scalar is None or abs(scalar) < 1e-15:
        return None
    implied = (computed / measured - 1.0) / abs(scalar)
    for factor in LEGACY_FACTORS:
        if abs(implied - factor) <= max(5e-6, 0.02 * factor) or abs(implied + factor) <= max(5e-6, 0.02 * factor):
            return factor
    return None


def main() -> int:
    history = _law_history()
    by_version: Counter[str] = Counter()
    round6_match = 0
    by_file: dict[str, Counter[str]] = {}
    examples: dict[str, list] = {"AEB2AD-ALPHA": [], "pre-ALPHA-domain-table": [], "unresolved": []}
    unrouted = 0
    scored = 0
    for path in sorted(DATA.glob("*_benchmark.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        recs = doc.get("material_records") or doc.get("records") or []
        if not isinstance(recs, list):
            continue
        file_counts: Counter[str] = Counter()
        for rec in recs:
            if not isinstance(rec, dict) or not is_ledger_b_scale_step(rec):
                continue
            measured = rec.get("measured")
            computed = rec.get("computed")
            if not isinstance(measured, (int, float)) or not isinstance(computed, (int, float)):
                file_counts["missing_pair"] += 1
                by_version["missing_pair"] += 1
                continue
            if float(measured) == 0.0:
                file_counts["measured_zero"] += 1
                by_version["measured_zero"] += 1
                continue
            domain = str(rec.get("fsot_domain") or rec.get("domain") or "")
            try:
                live_c, live_err = fsot_correct(float(measured), domain)
            except Exception:
                unrouted += 1
                file_counts["unrouted"] += 1
                by_version["unrouted"] += 1
                continue
            scored += 1
            stored_c = float(computed)
            live_c = float(live_c)
            scalar = rec.get("fsot_scalar")
            scalar_f = float(scalar) if isinstance(scalar, (int, float)) else None
            grain = round(stored_c, 6) == round(live_c, 6) or (
                abs(live_c) >= 1e6 and round(stored_c, 4) == round(live_c, 4)
            )
            if grain:
                round6_match += 1
            if _close(stored_c, live_c) or _close(stored_c, round(live_c, 6)) or _close(stored_c, round_sig(live_c)):
                version = "AEB2AD-ALPHA"
            elif _legacy_factor(stored_c, float(measured), scalar_f) is not None:
                version = "pre-ALPHA-domain-table"
            else:
                version = "unresolved"
            by_version[version] += 1
            file_counts[version] += 1
            if len(examples[version]) < 8:
                examples[version].append(
                    {
                        "file": path.name,
                        "name": rec.get("name"),
                        "property": rec.get("property"),
                        "fsot_domain": domain,
                        "stored_computed": stored_c,
                        "live_computed": round_sig(live_c),
                        "stored_error_pct": rec.get("error_pct"),
                        "live_error_pct": round_sig(float(live_err)),
                        "law_version": version,
                    }
                )
        if file_counts:
            by_file[path.name] = dict(file_counts)
    report = {
        "law": "c = m (1 + |S| ALPHA)",
        "pin": "AEB2AD",
        "stored_values_overwritten": False,
        "decision": "Left for Damian. This file is the side-by-side count only.",
        "rows_scored": scored,
        "rows_matching_live_at_6_decimal_grain": round6_match,
        "rows_unrouted": unrouted,
        "law_version_counts": dict(by_version),
        "law_version_source": history,
        "examples": examples,
        "by_file": by_file,
    }
    OUT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"rows_scored": scored, "law_version_counts": report["law_version_counts"], "out": str(OUT)}, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
