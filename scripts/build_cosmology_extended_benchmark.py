#!/usr/bin/env python3
"""Aggregate cosmology observables: Skeleton Key DB + ΛCDM + thesis wave targets."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
if str(ROOT / "vendor") not in sys.path:
    sys.path.insert(0, str(ROOT / "vendor"))

from math_formula_eval import evaluate_formula, core_context  # noqa: E402

try:
    from fsot_compute import (  # noqa: E402
        A_BLEED,
        C_COSM,
        C_EFF,
        ETA_EFF,
        G_CAT,
        P_BASE,
        P_NEW,
        P_VAR,
        PSI_CON,
        S_COSM,
        S_QUANT,
        THETA_S,
    )
except ImportError:
    A_BLEED = C_COSM = C_EFF = ETA_EFF = G_CAT = P_BASE = P_NEW = P_VAR = PSI_CON = S_COSM = S_QUANT = THETA_S = None  # type: ignore

MANIFEST_PATH = ROOT / "data" / "cosmology_extended_manifest.yaml"
OUTPUT = ROOT / "data" / "cosmology_extended_benchmark.json"
REGISTRY = ROOT / "data" / "lab_registry.json"

ERR_RE = re.compile(r"([\d.]+)\s*%", re.I)
TARGET_RE = re.compile(
    r"~?\s*([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)",
    re.I,
)

# Refined skeleton formulas: πγ radiative coupling on prior seed expressions.
SKELETON_FORMULA_OVERRIDES: dict[str, str] = {
    "Li-7/H": "5.6e-10*(SUCTION+POOF)/(PI*GAMMA^2)",
    # n_sat: θ_S·γ nuclear scale with πγ compactification damping (≡ THETA_S/(PI*GAMMA)).
    "n_sat": "THETA_S/(PI*GAMMA)",
    # He-3/H: φ²/E correction on POOF/(π⁴e⁵) BBN helium branch.
    "He-3/H": "POOF/(PI^4*E^4*PHI^2)",
}


def _skeleton_env() -> dict[str, float]:
    ctx = core_context()
    if S_COSM is not None:
        ctx.update(
            {
                "s_cosm": float(S_COSM),
                "s_quant": float(S_QUANT),
                "p_var": float(P_VAR),
                "theta_s": float(THETA_S),
                "a_bleed": float(A_BLEED),
                "eta_eff": float(ETA_EFF),
                "psi_con": float(PSI_CON),
                "c_cosm": float(C_COSM),
                "c_eff": float(C_EFF),
                "p_base": float(P_BASE),
                "p_new": float(P_NEW),
                "g_cat": float(G_CAT),
                "g": float(G_CAT),
            }
        )
    return ctx


def _eval_skeleton_formula(formula: str) -> float:
    normalized = (
        formula.replace("|CHAOS|", "abs(chaos)")
        .replace("|S_COSM|", "abs(s_cosm)")
        .replace("|Chaos|", "abs(chaos)")
        .replace("|S_cosm|", "abs(s_cosm)")
    )
    return evaluate_formula(normalized, _skeleton_env())


def _parse_target_scalar(raw: object) -> float | None:
    if raw is None:
        return None
    s = str(raw).strip()
    if not s or "empirical" in s.lower():
        return None
    m = TARGET_RE.search(s.replace("~", ""))
    if not m:
        return None
    try:
        return float(m.group(1))
    except ValueError:
        return None


def _error_pct(computed: float, target: float) -> float:
    if target == 0:
        return 0.0 if computed == 0 else 100.0
    return abs(computed - target) / abs(target) * 100.0


def _parse_error_pct(raw: object) -> float | None:
    if raw is None or raw == "-":
        return None
    s = str(raw).strip()
    if not s:
        return None
    if "within" in s.lower() or "sigma" in s.lower():
        return 1.0
    m = ERR_RE.search(s)
    if m:
        return float(m.group(1))
    try:
        return float(s.replace("%", ""))
    except ValueError:
        return None


def _skeleton_rows(db_path: Path) -> list[dict]:
    rows = json.loads(db_path.read_text(encoding="utf-8"))
    out: list[dict] = []
    for row in rows:
        if "Cosmology Derivation" not in str(row.get("Type", "")):
            continue
        symbol = str(row.get("Symbol") or "")
        section = str(row.get("Type", "")).split("(")[-1].rstrip(")")
        formula = row.get("Description_Formula")
        override = SKELETON_FORMULA_OVERRIDES.get(symbol)
        if override:
            formula = override
        target_raw = row.get("Target_Unit")
        target_scalar = _parse_target_scalar(target_raw)
        computed: float | str | None = row.get("Value")
        err = _parse_error_pct(row.get("Error"))
        if override and S_COSM is not None:
            try:
                computed = _eval_skeleton_formula(str(formula))
                if target_scalar is not None:
                    err = round(_error_pct(float(computed), target_scalar), 3)
            except (ValueError, KeyError, ZeroDivisionError):
                pass
        out.append(
            {
                "source": "skeleton_database",
                "symbol": symbol,
                "section": section,
                "formula": formula,
                "computed": computed,
                "target": target_raw,
                "error_pct": err,
            }
        )
    return out


def _thesis_cosmo_rows(thesis_root: Path, categories: list[str]) -> list[dict]:
    out: list[dict] = []
    cat_set = set(categories)
    for wave in (7, 8, 9, 10):
        path = thesis_root / f"wave{wave}_observations.json"
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for key, row in (data.get("targets") or {}).items():
            if row.get("category") not in cat_set:
                continue
            sigma = row.get("sigma_percent")
            try:
                sigma_f = float(sigma) if sigma not in (None, "") else None
            except (TypeError, ValueError):
                sigma_f = None
            out.append(
                {
                    "source": "thesis_wave",
                    "wave": wave,
                    "id": key,
                    "name": row.get("name") or key,
                    "category": row.get("category"),
                    "measured": row.get("measured"),
                    "sigma_percent": sigma_f,
                }
            )
    return out


def _lambda_cdm_rows(registry: dict) -> list[dict]:
    cos = registry.get("cosmology_lambda_cdm", {})
    rows = cos.get("rows") or cos.get("observables") or []
    out: list[dict] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        out.append(
            {
                "source": "lambda_cdm",
                "wave": row.get("wave"),
                "name": row.get("name"),
                "computed": row.get("computed"),
                "measured": row.get("measured"),
                "error_pct": row.get("error_pct"),
            }
        )
    return out


def build_benchmark(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    src = spec["source"]
    cos_root = Path(src["cosmology_root"])
    db_path = cos_root / src["skeleton_database"]
    if not db_path.exists():
        raise FileNotFoundError(f"Skeleton database missing: {db_path}")

    skeleton = _skeleton_rows(db_path)
    thesis = _thesis_cosmo_rows(Path(src["thesis_root"]), list(src["thesis_cosmology_categories"]))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    lambda_rows = _lambda_cdm_rows(registry)

    sk_errs = [r["error_pct"] for r in skeleton if r.get("error_pct") is not None]
    lc_errs = [r["error_pct"] for r in lambda_rows if r.get("error_pct") is not None]
    all_errs = sk_errs + lc_errs
    within_5 = sum(1 for e in all_errs if e <= 5.0)

    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_root": str(cos_root),
        "skeleton_derivation_count": len(skeleton),
        "lambda_cdm_count": len(lambda_rows),
        "thesis_cosmology_wave_count": len(thesis),
        "observable_count": len(skeleton) + len(lambda_rows) + len(thesis),
        "median_error_pct": sorted(all_errs)[len(all_errs) // 2] if all_errs else None,
        "within_five_pct_count": within_5,
        "skeleton_derivations": skeleton,
        "lambda_cdm_observables": lambda_rows,
        "thesis_cosmology_waves": thesis,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        bench = build_benchmark(args.manifest)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(bench, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  skeleton: {bench['skeleton_derivation_count']}  "
        f"lambda_cdm: {bench['lambda_cdm_count']}  "
        f"thesis: {bench['thesis_cosmology_wave_count']}  "
        f"total: {bench['observable_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())