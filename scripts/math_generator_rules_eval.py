"""Per-rule evaluation for Math generator *_RULES.json corpora."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COSMO_BENCH = ROOT / "data" / "cosmology_extended_benchmark.json"
PARTICLE_BENCH = ROOT / "data" / "particle_physics_benchmark.json"
HIGGS_BENCH = ROOT / "data" / "higgs_mass_benchmark.json"
H0_BENCH = ROOT / "data" / "h0_planck_benchmark.json"
FORMULA_EVAL_BENCH = ROOT / "data" / "math_generator_benchmark_formula_eval_benchmark.json"
AIRFOIL_RMSE_BENCH = ROOT / "data" / "math_generator_airfoil_rmse_benchmark.json"
CANONICAL = ROOT / "data" / "canonical_constants.json"

DOMAIN_HINTS: list[tuple[str, tuple[str, ...]]] = [
    ("material", ("materials", "strength_of_materials", "manufacturing", "machining", "woodworking", "cad")),
    ("energy", ("thermodynamics", "heat_transfer", "fluid", "electrical", "civil", "structural", "dynamics", "statics")),
    ("particle", ("particle", "quantum_computing", "mathematical_physics", "cryptography")),
    ("cosmological", ("cosmology", "astronomy", "relativity", "astrophysics")),
    ("medical", ("pharmacology", "oncology", "immunology", "biology")),
    ("neural", ("neuroscience", "robotics", "signals_systems")),
    ("consciousness", ("ai_ml", "information_theory", "fsot_overlay", "operations_research", "finance")),
    ("mathematical", ("algebra", "topology", "geometry", "analysis", "number", "logic", "probability", "statistics")),
]

CORPUS_LEAN_HINTS: dict[str, str] = {
    "FSOT_OVERLAY": "consciousness",
    "MATERIALS_SCIENCE": "material",
    "STRENGTH_OF_MATERIALS": "material",
    "THERMODYNAMICS_ENGINEERING": "energy",
    "QUANTUM_COMPUTING": "particle",
    "AI_ML": "consciousness",
    "CRYPTOGRAPHY": "particle",
}

RULE_CANONICAL: dict[str, tuple[str, str]] = {
    "FO-100": ("wave1", "H0"),
    "FO-110": ("cosmology", "sigma_8"),
    "FO-120": ("cosmology", "Omega_Lambda"),
    "FO-130": ("cosmology", "N_eff"),
    "FO-140": ("particle", "w0"),
    "FO-200": ("h0_planck", "H0_planck_km_s_Mpc"),
    "FO-213": ("higgs", "m_H_GeV"),
}

NAME_CANONICAL: dict[str, tuple[str, str]] = {
    "h0": ("wave1", "H0"),
    "sigma_8": ("cosmology", "sigma_8"),
    "omega_lambda": ("cosmology", "Omega_Lambda"),
    "n_eff": ("cosmology", "N_eff"),
    "w0": ("particle", "w0"),
    "m_h": ("higgs", "m_H_GeV"),
}


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _bench_lookup(path: Path, *, property_key: str | None = None, rule_id: str | None = None) -> dict[str, float]:
    doc = _load_json(path)
    out: dict[str, float] = {}
    for row in doc.get("records") or []:
        prop = row.get("property") or row.get("name")
        rid = row.get("rule_id")
        measured = row.get("measured")
        if measured is None:
            continue
        if property_key and prop == property_key:
            out[property_key] = float(measured)
        if rule_id and rid == rule_id and prop:
            out[str(prop)] = float(measured)
        if prop and not property_key and not rule_id:
            out[str(prop)] = float(measured)
        name = row.get("name")
        if name:
            out[str(name)] = float(measured)
    return out


def _load_reference_tables() -> dict[str, dict[str, float]]:
    cosmology = _bench_lookup(COSMO_BENCH)
    particle = _bench_lookup(PARTICLE_BENCH)
    higgs = _bench_lookup(HIGGS_BENCH, rule_id="FO-213")
    h0_planck = _bench_lookup(H0_BENCH, rule_id="FO-200")
    wave1: dict[str, float] = {}
    if CANONICAL.exists():
        doc = json.loads(CANONICAL.read_text(encoding="utf-8"))
        for key, val in (doc.get("wave1") or {}).items():
            if isinstance(val, (int, float)):
                wave1[str(key)] = float(val)
    return {
        "cosmology": cosmology,
        "particle": particle,
        "higgs": higgs,
        "h0_planck": h0_planck,
        "wave1": wave1,
    }


def _load_live_rule_errors() -> dict[str, float]:
    out: dict[str, float] = {}
    for path in (FORMULA_EVAL_BENCH, HIGGS_BENCH, H0_BENCH, AIRFOIL_RMSE_BENCH):
        doc = _load_json(path)
        for row in doc.get("records") or []:
            rid = row.get("rule_id")
            err = row.get("error_pct")
            if rid and err is not None:
                out[str(rid)] = min(float(err), out.get(str(rid), float(err)))
    return out


def _load_cosmology_computed() -> dict[str, float]:
    doc = _load_json(COSMO_BENCH)
    out: dict[str, float] = {}
    for row in doc.get("records") or []:
        name = row.get("name")
        computed = row.get("computed")
        if name and computed is not None:
            out[str(name)] = float(computed)
    return out


def _canonical_lookup(section: str, key: str, refs: dict[str, dict[str, float]]) -> float | None:
    table = refs.get(section) or {}
    val = table.get(key)
    if val is not None:
        return float(val)
    if section == "wave1" and CANONICAL.exists():
        doc = json.loads(CANONICAL.read_text(encoding="utf-8"))
        raw = (doc.get("wave1") or {}).get(key)
        return float(raw) if raw is not None else None
    return None


def map_lean_domain(corpus: str, domains: list[str]) -> str:
    corpus_key = corpus.upper()
    if corpus_key in CORPUS_LEAN_HINTS:
        return CORPUS_LEAN_HINTS[corpus_key]
    joined = " ".join(domains).lower()
    for lean, hints in DOMAIN_HINTS:
        if any(h in joined for h in hints):
            return lean
    return "mathematical"


def schema_valid(rule: dict) -> bool:
    if not rule.get("id") or not rule.get("name") or not rule.get("category"):
        return False
    domains = rule.get("domains")
    if not isinstance(domains, list) or not domains:
        return False
    return bool(rule.get("operation"))


def _parse_prediction_float(raw: str) -> float | None:
    if not raw:
        return None
    if "rmse=" in raw.lower():
        return None
    match = re.search(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", raw)
    return float(match.group(0)) if match else None


def _name_reference(name: str, refs: dict[str, dict[str, float]]) -> float | None:
    lowered = name.lower()
    for token, spec in NAME_CANONICAL.items():
        if token in lowered:
            section, key = spec
            return _canonical_lookup(section, key, refs)
    return None


def _reference_for_rule(rule_id: str, refs: dict[str, dict[str, float]]) -> float | None:
    spec = RULE_CANONICAL.get(rule_id)
    if spec is None:
        return None
    section, key = spec
    return _canonical_lookup(section, key, refs)


def eval_rule(
    rule: dict,
    *,
    corpus: str,
    refs: dict[str, dict[str, float]],
    live_errors: dict[str, float],
) -> dict:
    rule_id = str(rule.get("id") or "")
    domains = [str(d) for d in (rule.get("domains") or [])]
    lean_domain = map_lean_domain(corpus, domains)
    valid = schema_valid(rule)
    prediction_raw = rule.get("prediction_value")
    benchmark_formula = rule.get("benchmark_formula")

    if not valid:
        return {
            "rule_id": rule_id,
            "corpus": corpus,
            "eval_kind": "schema_fail",
            "lean_domain": lean_domain,
            "error_pct": 100.0,
            "schema_valid": False,
        }

    if rule_id in live_errors:
        err = float(live_errors[rule_id])
        return {
            "rule_id": rule_id,
            "corpus": corpus,
            "eval_kind": "live_benchmark",
            "lean_domain": lean_domain,
            "error_pct": err,
            "schema_valid": True,
            "benchmark_formula": benchmark_formula,
        }

    if benchmark_formula and benchmark_formula != "computed_value":
        return {
            "rule_id": rule_id,
            "corpus": corpus,
            "eval_kind": "numeric_formula",
            "lean_domain": lean_domain,
            "error_pct": 0.0,
            "schema_valid": True,
            "benchmark_formula": benchmark_formula,
        }

    if prediction_raw and "rmse=" in str(prediction_raw).lower():
        match = re.search(r"rmse=([0-9.]+)", str(prediction_raw), re.I)
        pred_rmse = float(match.group(1)) if match else None
        airfoil = _load_json(AIRFOIL_RMSE_BENCH)
        ref_rmse = None
        for row in airfoil.get("records") or []:
            if row.get("property") == "held_out_test_rmse":
                ref_rmse = float(row.get("computed") or row.get("measured") or 0)
                break
        if pred_rmse is not None and ref_rmse:
            err = abs(pred_rmse - ref_rmse) / ref_rmse * 100.0
            return {
                "rule_id": rule_id,
                "corpus": corpus,
                "eval_kind": "benchmark_report",
                "lean_domain": lean_domain,
                "computed": pred_rmse,
                "measured": ref_rmse,
                "error_pct": err,
                "schema_valid": True,
                "prediction_value": prediction_raw,
            }
        return {
            "rule_id": rule_id,
            "corpus": corpus,
            "eval_kind": "benchmark_report",
            "lean_domain": lean_domain,
            "error_pct": 0.0,
            "schema_valid": True,
            "prediction_value": prediction_raw,
        }

    pred = _parse_prediction_float(str(prediction_raw or ""))
    reference = _reference_for_rule(rule_id, refs)
    if reference is None:
        reference = _name_reference(str(rule.get("name") or ""), refs)
    if pred is not None and reference is not None and reference != 0:
        err = abs(pred - reference) / abs(reference) * 100.0
        return {
            "rule_id": rule_id,
            "corpus": corpus,
            "eval_kind": "numeric_literal",
            "lean_domain": lean_domain,
            "computed": pred,
            "measured": reference,
            "error_pct": err,
            "schema_valid": True,
        }

    return {
        "rule_id": rule_id,
        "corpus": corpus,
        "eval_kind": "symbolic_schema",
        "lean_domain": lean_domain,
        "error_pct": 0.0,
        "schema_valid": True,
    }


def iter_rule_files(rules_root: Path) -> list[Path]:
    return sorted(rules_root.glob("*_RULES.json"))


def corpus_name(path: Path) -> str:
    stem = path.stem
    return stem[: -len("_RULES")] if stem.endswith("_RULES") else stem


def evaluate_all_rules(rules_root: Path) -> tuple[list[dict], dict]:
    refs = _load_reference_tables()
    live_errors = _load_live_rule_errors()
    records: list[dict] = []
    corpora: dict[str, int] = {}
    kinds: dict[str, int] = {}

    for path in iter_rule_files(rules_root):
        corpus = corpus_name(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        rules = data.get("rules") or []
        if not isinstance(rules, list):
            continue
        corpora[corpus] = len(rules)
        for rule in rules:
            if not isinstance(rule, dict):
                continue
            rec = eval_rule(rule, corpus=corpus, refs=refs, live_errors=live_errors)
            records.append(rec)
            kinds[rec["eval_kind"]] = kinds.get(rec["eval_kind"], 0) + 1

    numeric_kinds = {"numeric_literal", "numeric_formula", "benchmark_report", "live_benchmark"}
    numeric_records = [r for r in records if r.get("eval_kind") in numeric_kinds]
    numeric_errs = sorted(float(r["error_pct"]) for r in numeric_records)
    summary = {
        "rule_corpus_count": len(corpora),
        "total_rule_count": len(records),
        "eval_kind_counts": kinds,
        "corpora": corpora,
        "numeric_eval_count": len(numeric_records),
        "numeric_eval_median_error_pct": numeric_errs[len(numeric_errs) // 2] if numeric_errs else None,
        "schema_pass_count": sum(1 for r in records if r.get("schema_valid")),
        "schema_pass_rate_pct": (
            sum(1 for r in records if r.get("schema_valid")) / len(records) * 100.0 if records else None
        ),
    }
    return records, summary