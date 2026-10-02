#!/usr/bin/env python3
"""Restore computed values that absolute 6-decimal rounding wiped.

Recovers c from measured and the stored error_pct when the stored computed
equals round(c, 6) or round(c, 4). Does not change the law. Skips frozen
panels. Writes only files whose JSON dump is byte-stable aside from the
restored numbers.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_api_predict_lib import err_pct, round_sig  # noqa: E402

DATA = ROOT / "data"
REPORT = DATA / "sigfig_restore_report.json"


def _frozen_reason(name: str) -> str | None:
    n = name.lower()
    if "sh0es" in n:
        return "SH0ES ladder panel is frozen"
    if "zebrafish" in n:
        return "zebrafish panel is frozen"
    if "prereg" in n:
        return "preregistration benchmark is frozen (TOE-PREREG-20260909)"
    return None


def _recover(computed: float, measured: float, error_pct: float) -> float | None:
    if measured == 0.0:
        return None
    for sign in (1.0, -1.0):
        full = measured * (1.0 + sign * error_pct / 100.0)
        rounded = round(full, 6) if abs(full) < 1e6 else round(full, 4)
        wiped = computed == 0.0 and rounded == 0.0 and 0.0 < abs(full) < 5e-7
        if rounded == computed or wiped:
            stored = round_sig(full)
            if stored != computed:
                return stored
    if error_pct == 0.0 and computed == 0.0 and 0.0 < abs(measured) < 5e-7:
        stored = round_sig(measured)
        if stored != computed:
            return stored
    return None


def _dump_bytes(doc: object, newline: str, trailing: bool) -> bytes:
    text = json.dumps(doc, indent=2, allow_nan=False)
    if trailing:
        text += "\n"
    text = text.replace("\n", newline)
    return text.encode("utf-8")


def _records(doc: dict) -> list[dict]:
    recs = doc.get("material_records")
    if isinstance(recs, list):
        return [r for r in recs if isinstance(r, dict)]
    recs = doc.get("records")
    if isinstance(recs, list):
        return [r for r in recs if isinstance(r, dict)]
    return []


def main() -> int:
    updated: list[dict] = []
    skipped_frozen: list[dict] = []
    skipped_unstable: list[str] = []
    skipped_nan: list[str] = []
    unchanged = 0
    for path in sorted(DATA.glob("*_benchmark.json")):
        reason = _frozen_reason(path.name)
        raw = path.read_bytes()
        newline = "\r\n" if b"\r\n" in raw else "\n"
        trailing = raw.endswith(b"\n") or raw.endswith(b"\r\n")
        try:
            doc = json.loads(raw.decode("utf-8"))
        except Exception:
            skipped_unstable.append(path.name)
            continue
        if reason:
            # Count recoverable rows so the report says what was left alone.
            n = 0
            for rec in _records(doc):
                try:
                    got = _recover(float(rec["computed"]), float(rec["measured"]), float(rec["error_pct"]))
                except (KeyError, TypeError, ValueError):
                    continue
                if got is not None:
                    n += 1
            if n:
                skipped_frozen.append({"file": path.name, "recoverable_rows": n, "reason": reason})
            continue
        try:
            stable = _dump_bytes(doc, newline, trailing) == raw
        except ValueError:
            skipped_nan.append(path.name)
            continue
        if not stable:
            skipped_unstable.append(path.name)
            continue
        n = 0
        for rec in _records(doc):
            try:
                computed = float(rec["computed"])
                measured = float(rec["measured"])
                error = float(rec["error_pct"])
            except (KeyError, TypeError, ValueError):
                continue
            restored = _recover(computed, measured, error)
            if restored is None:
                continue
            rec["error_pct_full"] = round_sig(error)
            rec["computed"] = restored
            rec["error_pct"] = round_sig(err_pct(restored, measured))
            n += 1
        if not n:
            unchanged += 1
            continue
        try:
            payload = _dump_bytes(doc, newline, trailing)
        except ValueError:
            skipped_nan.append(path.name)
            continue
        path.write_bytes(payload)
        updated.append({"file": path.name, "rows_restored": n})
        print(f"restored {n:6d} {path.name}")
    report = {
        "rows_restored": sum(item["rows_restored"] for item in updated),
        "files_updated": updated,
        "files_skipped_frozen": skipped_frozen,
        "files_skipped_unstable_json": skipped_unstable,
        "files_skipped_nan": skipped_nan,
        "files_unchanged": unchanged,
        "note": (
            "Restored computed is the significant-digit form of "
            "measured * (1 ± stored error_pct/100) when that value rounds "
            "back to the stored computed. The law is unchanged. "
            "Frozen panels were not rewritten."
        ),
    }
    REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] if k != "files_updated" else len(updated) for k in report if k != "note"}, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
