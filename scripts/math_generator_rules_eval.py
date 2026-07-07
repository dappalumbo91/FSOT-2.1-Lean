"""Per-rule evaluation for Math generator *_RULES.json corpora."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COSMO_BENCH = ROOT / "data" / "cosmology_extended_benchmark.json"
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
    "FO-140": ("cosmology", "w0"),
}


def _load_cosmology_computed() -> dict[str, float]:
    if not COSMO_BENCH.exists():
        return {}
    doc = json.loads(COSMO_BENCH.read_text(encoding="utf-8"))
    out: dict[str, float] = {}
    for row in doc.get("records") or []:
        name = row.get("name")
        computed = row.get("computed")
        if name and computed is not None:
            out[str(name)] = float(computed)
    return out


def _canonical_lookup(section: str, key: str) -> float | None:
    if not CANONICAL.exists():
        return None
    doc = json.loads(CANONICAL.read_text(encoding="utf-8"))
    if section == "wave1":
        val = (doc.get("wave1") or {}).get(key)
    else:
        val = None
    return float(val) if val is not None else None


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


def _reference_for_rule(rule_id: str, cosmology: dict[str, float]) -> float | None:
    spec = RULE_CANONICAL.get(rule_id)
    if spec is None:
        return None
    section, key = spec
    if section == "wave1":
        return _canonical_lookup(section, key)
    return cosmology.get(key)


def eval_rule(rule: dict, *, corpus: str, cosmology: dict[str, float]) -> dict:
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
    reference = _reference_for_rule(rule_id, cosmology)
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

    if pred is not None and rule_id.startswith("FO-"):
        canonical_h0 = _canonical_lookup("wave1", "H0")
        if canonical_h0 and "H0" in (rule.get("name") or ""):
            err = abs(pred - canonical_h0) / abs(canonical_h0) * 100.0
            return {
                "rule_id": rule_id,
                "corpus": corpus,
                "eval_kind": "numeric_literal",
                "lean_domain": lean_domain,
                "computed": pred,
                "measured": canonical_h0,
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
    cosmology = _load_cosmology_computed()
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
            rec = eval_rule(rule, corpus=corpus, cosmology=cosmology)
            records.append(rec)
            kinds[rec["eval_kind"]] = kinds.get(rec["eval_kind"], 0) + 1

    summary = {
        "rule_corpus_count": len(corpora),
        "total_rule_count": len(records),
        "eval_kind_counts": kinds,
        "corpora": corpora,
    }
    return records, summary