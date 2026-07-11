#!/usr/bin/env python3
"""Verify strict-empirical FSOT formulas: thresholds + integrity + live recompute sample."""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "formula_corpus_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
DEBT_REPORT = ROOT / "data" / "formula_live_recompute_debt.json"

sys.path.insert(0, str(ROOT / "scripts"))
from formula_corpus import (  # noqa: E402
    err_pct_from_values,
    load_strict_empirical_jsonl,
    observable_key,
    summarize_formula_corpus,
)
from fsot_paths import rel_repo_path, strict_empirical_jsonl_path  # noqa: E402


def _extended_eval_context() -> dict[str, float]:
    from math_formula_eval import core_context  # noqa: E402

    ctx = core_context()
    ctx.update(
        {
            "eta": ctx["eta_eff"],
            "psi": ctx["psi_con"],
            "theta": ctx["theta_s"],
            "g": ctx["g_cat"],
        }
    )
    return ctx


def _dedupe_unique_observables(rows: list[dict]) -> list[dict]:
    """Keep first row per (concept, formula, target) — avoids triplicate oversampling."""
    seen: set[tuple[str, str, str]] = set()
    unique: list[dict] = []
    for row in rows:
        key = observable_key(row)
        if key in seen:
            continue
        seen.add(key)
        unique.append(row)
    return unique


def _live_recompute_sample(
    rows: list[dict],
    *,
    sample_size: int,
    max_drift_pct: float,
    dedupe_unique: bool = True,
) -> tuple[list[str], dict]:
    """Re-evaluate a deterministic sample via math_formula_eval (fail-closed)."""
    from math_formula_eval import evaluate_formula  # noqa: E402

    issues: list[str] = []
    eligible = [
        r
        for r in rows
        if (r.get("formula_canonical") or r.get("formula_publication"))
        and (r.get("outcome") or {}).get("target_value") is not None
    ]
    if not eligible:
        return ["formula_corpus: no rows eligible for live recompute"], {}

    pool = _dedupe_unique_observables(eligible) if dedupe_unique else eligible
    rng = random.Random(42)
    sample = pool if len(pool) <= sample_size else rng.sample(pool, sample_size)
    ctx = _extended_eval_context()
    checked = 0
    skipped_unsupported = 0
    recomputed_ok = 0
    max_live_drift = 0.0
    drift_debt: list[dict] = []
    for row in sample:
        formula = str(row.get("formula_canonical") or row.get("formula_publication"))
        outcome = row.get("outcome") or {}
        try:
            target = float(outcome["target_value"])
            cached_computed = float(outcome.get("computed_value", 0))
            cached_err = float(outcome.get("error_pct", 999))
        except (TypeError, ValueError, KeyError):
            issues.append(f"live_recompute: bad outcome for {row.get('concept_name')}")
            continue

        integrity_err = err_pct_from_values(target, cached_computed)
        if abs(integrity_err - cached_err) > max_drift_pct:
            issues.append(
                f"integrity: stored error mismatch on {row.get('concept_name')} "
                f"(stored={cached_err:.4f} recomputed={integrity_err:.4f})"
            )

        try:
            live_computed = float(evaluate_formula(formula, ctx))
        except Exception:
            skipped_unsupported += 1
            continue

        checked += 1
        live_err = err_pct_from_values(target, live_computed)
        drift = abs(live_err - cached_err)
        max_live_drift = max(max_live_drift, drift)
        if drift <= max_drift_pct:
            recomputed_ok += 1
        else:
            drift_debt.append(
                {
                    "concept_name": row.get("concept_name"),
                    "formula": formula,
                    "cached_error_pct": cached_err,
                    "live_error_pct": live_err,
                    "drift_pct": drift,
                }
            )

    min_ok_ratio = 0.95
    min_evaluable = 50
    ok_ratio = recomputed_ok / checked if checked else 0.0
    if checked < min_evaluable:
        issues.append(
            f"live_recompute: only {checked} evaluable rows in sample (need {min_evaluable})"
        )
    elif ok_ratio < min_ok_ratio:
        issues.append(
            f"live_recompute: only {recomputed_ok}/{checked} within {max_drift_pct}% drift"
        )

    debt_doc = {
        "drift_debt_count": len(drift_debt),
        "drift_debt": drift_debt,
        "note": "Rows where portable math_formula_eval disagrees with cached fsot_numeric_eval outcomes.",
    }
    DEBT_REPORT.write_text(json.dumps(debt_doc, indent=2), encoding="utf-8")

    return issues, {
        "live_recompute_pool_size": len(pool),
        "live_recompute_deduped": dedupe_unique,
        "live_recompute_sample_size": len(sample),
        "live_recompute_checked": checked,
        "live_recompute_skipped_unsupported": skipped_unsupported,
        "live_recompute_ok": recomputed_ok,
        "live_recompute_ok_ratio": round(ok_ratio, 4) if checked else 0.0,
        "live_recompute_drift_debt_count": len(drift_debt),
        "live_recompute_max_drift_pct": round(max_live_drift, 6),
        "live_recompute_debt_report": str(DEBT_REPORT.relative_to(ROOT)),
    }


def verify_formula_corpus(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    corpus_path = strict_empirical_jsonl_path()
    issues: list[str] = []

    if not corpus_path.exists():
        return [f"missing strict_empirical corpus: {corpus_path}"], {}

    rows = load_strict_empirical_jsonl(corpus_path)
    live = summarize_formula_corpus(rows)
    live["corpus_path"] = rel_repo_path(corpus_path)

    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    if not registry.get("formula_corpus"):
        issues.append("formula_corpus: not ingested — run ingest_formula_corpus.py")

    checks = [
        ("records_min", "records_total"),
        ("unique_observables_min", "unique_observables"),
        ("matched_min", "matched_count"),
        ("unique_matched_min", "unique_matched_count"),
        ("within_target_2pct_min", "within_target_2pct"),
        ("unique_within_target_2pct_min", "unique_within_target_2pct"),
        ("within_tolerable_5pct_min", "within_tolerable_5pct"),
    ]
    for min_key, live_key in checks:
        floor = ver.get(min_key)
        if floor is not None and (live.get(live_key) or 0) < floor:
            issues.append(f"formula_corpus: {live_key}={live.get(live_key)} < {floor}")

    unmatched_max = ver.get("unmatched_max", 0)
    if (live.get("unmatched_count") or 0) > unmatched_max:
        issues.append(f"formula_corpus: unmatched_count={live.get('unmatched_count')}")

    if ver.get("live_recompute_enabled", True):
        sample_size = int(ver.get("live_recompute_sample_size", 200))
        max_drift = float(ver.get("live_recompute_max_drift_pct", 0.05))
        dedupe_unique = bool(ver.get("live_recompute_dedupe_unique_observables", True))
        recompute_issues, recompute_stats = _live_recompute_sample(
            rows,
            sample_size=sample_size,
            max_drift_pct=max_drift,
            dedupe_unique=dedupe_unique,
        )
        issues.extend(recompute_issues)
        live.update(recompute_stats)

    return issues, {**live, "issues": len(issues)}


def main() -> int:
    issues, summary = verify_formula_corpus()
    print("=== Formula corpus verification (strict empirical) ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All formula corpus checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())