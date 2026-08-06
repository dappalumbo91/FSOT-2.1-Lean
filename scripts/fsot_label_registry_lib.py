"""Human-readable labels for opaque FSOT codes (tiers, FO rules, PRED, obligations)."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_YAML = ROOT / "data" / "fsot_label_registry.yaml"
REGISTRY_JSON = ROOT / "data" / "fsot_label_registry.json"
OVERLAY_RULES = ROOT / "vendor" / "math_generator" / "rules" / "FSOT_OVERLAY_RULES.json"
PREREG_MANIFEST = ROOT / "predictions" / "preregistered_predictions_manifest.yaml"
EXTENSION_MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"
EXPANSION_ROADMAP = ROOT / "data" / "expansion_roadmap.yaml"

_KIND_LABELS = {
    "lt_half": "pooled median error < 0.5%",
    "nat_pos": "observable count > 0",
    "pos": "scalar > 0",
    "gt_one": "scalar > 1",
    "lt": "scalar ordering",
    "lt_lit": "scalar below literature bound",
    "gt_lit": "scalar above literature bound",
    "eq_nat": "count identity",
    "eq_nat_arith": "count arithmetic identity",
    "nat_gt_lit": "count exceeds bound",
    "nat_le_lit": "count within bound",
    "bundle_conj": "structural bundle index (conjunct witness linkage)",
}

_HEADLINE_COUNT_KIND = "headline ℕ count > 0 (not SOTA superiority proof)"

_CONNECTIVE_SYMBOLS = {
    "warp_psi_friction": "Warp ψ friction coupling (actuation)",
    "warp_psi_node": "Warp ψ node coupling (actuation)",
    "fusion_grid_coupling": "Fusion grid connective coupling",
    "e10d_wd_coupling": "E10d WD connective coupling",
}


def humanize_domain_key(key: str) -> str:
    """Plasma_Physics → Plasma Physics."""
    return re.sub(r"\s+", " ", key.replace("_", " ")).strip()


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        import yaml
    except ImportError:
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


@lru_cache(maxsize=1)
def load_registry() -> dict[str, Any]:
    if REGISTRY_JSON.exists():
        return json.loads(REGISTRY_JSON.read_text(encoding="utf-8"))
    return _load_yaml(REGISTRY_YAML)


def resolve_tier_label(tier: int | str) -> str:
    reg = load_registry()
    tiers = reg.get("tiers") or {}
    key = str(tier)
    if key in tiers:
        return str(tiers[key])
    if isinstance(tier, str) and tier in tiers:
        return str(tiers[tier])
    roadmap = _load_yaml(EXPANSION_ROADMAP)
    for tier_key, domains in (roadmap.get("completed_tiers") or {}).items():
        num = tier_key.replace("tier_", "")
        if key == num:
            sample = domains[0] if domains else tier_key
            return f"Tier {num} — {humanize_domain_key(str(sample))} cluster"
    return f"Tier {tier}"


def resolve_extension_domain(domain_key: str) -> dict[str, str]:
    reg = load_registry()
    domains = reg.get("extension_domains") or {}
    if domain_key in domains:
        row = domains[domain_key]
        return {
            "display_name": row.get("display_name") or humanize_domain_key(domain_key),
            "tier_label": row.get("tier_label") or resolve_tier_label(row.get("tier", "?")),
        }
    manifest = _load_yaml(EXTENSION_MANIFEST)
    cfg = (manifest.get("extension_domains") or {}).get(domain_key) or {}
    tier = cfg.get("tier", "?")
    return {
        "display_name": humanize_domain_key(domain_key),
        "tier_label": resolve_tier_label(tier),
    }


def resolve_fo_rule(rule_id: str) -> str:
    reg = load_registry()
    fo = reg.get("math_generator_rules") or {}
    if rule_id in fo:
        return str(fo[rule_id])
    if OVERLAY_RULES.exists():
        doc = json.loads(OVERLAY_RULES.read_text(encoding="utf-8"))
        for rule in doc.get("rules") or []:
            if str(rule.get("id")) == rule_id:
                return str(rule.get("name") or rule_id)
    return rule_id


def resolve_math_rule(rule_id: str) -> str:
    """AA-001, MS-001, PL-001 from math_generator rules."""
    reg = load_registry()
    mg = reg.get("math_generator_rule_codes") or {}
    if rule_id in mg:
        return str(mg[rule_id])
    rules_root = ROOT / "vendor" / "math_generator" / "rules"
    if rules_root.exists():
        for path in rules_root.glob("*_RULES.json"):
            doc = json.loads(path.read_text(encoding="utf-8"))
            for rule in doc.get("rules") or []:
                if str(rule.get("id")) == rule_id:
                    return str(rule.get("name") or rule_id)
    return rule_id


def resolve_prereg(pred_id: str) -> str:
    reg = load_registry()
    preds = reg.get("prereg_predictions") or {}
    if pred_id in preds:
        return str(preds[pred_id])
    manifest = _load_yaml(PREREG_MANIFEST)
    for row in manifest.get("predictions") or []:
        if str(row.get("id")) == pred_id:
            return str(row.get("name") or pred_id)
    return pred_id


def resolve_smiles_section(section: str) -> str:
    reg = load_registry()
    smiles = reg.get("smiles_sections") or {}
    if section in smiles:
        return str(smiles[section])
    if section.startswith("§"):
        return f"SMILES Lab {section}"
    return section


def resolve_obligation_label(ob: dict) -> str:
    """Turn acoustic_rm_pooled_median_under_half_pct into readable text."""
    oid = str(ob.get("id") or "")
    reg = load_registry()
    obligations = reg.get("obligations") or {}
    if oid in obligations:
        return str(obligations[oid])

    sym = str(ob.get("symbol") or "")
    if sym in _CONNECTIVE_SYMBOLS:
        kind = _KIND_LABELS.get(str(ob.get("kind")), str(ob.get("kind")))
        return f"{_CONNECTIVE_SYMBOLS[sym]}: {kind}"

    module = str(ob.get("lean_module") or "")
    module_name = humanize_domain_key(module.replace("Priors", "").replace(".lean", ""))
    kind = _KIND_LABELS.get(str(ob.get("kind")), str(ob.get("kind") or "certificate"))

    if sym:
        sym_readable = humanize_domain_key(sym.replace("_error_pct", "").replace("_", " "))
        return f"{module_name}: {sym_readable} — {kind}"

    return f"{module_name}: {kind} ({oid})"


def resolve_record_label(record: dict) -> dict[str, str]:
    """Resolve display labels for a benchmark material record."""
    name = str(record.get("name") or "")
    rule_id = str(record.get("rule_id") or "")
    prop = str(record.get("property") or "")

    out: dict[str, str] = {}
    if rule_id.startswith("FO-"):
        out["rule_display_name"] = resolve_fo_rule(rule_id)
    elif re.fullmatch(r"[A-Z]{2}-\d{3}", name):
        out["rule_display_name"] = resolve_math_rule(name)
    elif name.startswith("PRED-"):
        out["prediction_display_name"] = resolve_prereg(name)
    elif prop.startswith("§"):
        out["section_display_name"] = resolve_smiles_section(prop)

    if not out.get("rule_display_name") and not out.get("prediction_display_name"):
        if re.fullmatch(r"[A-Z]{2}-\d{3}", name):
            out["rule_display_name"] = resolve_math_rule(name)

    domain = str(record.get("domain") or record.get("lab") or "")
    if domain:
        out["domain_display_name"] = humanize_domain_key(domain.replace("_lab", "").replace("_benchmark", ""))

    return out


def annotate_obligation(ob: dict) -> dict:
    enriched = dict(ob)
    oid = str(ob.get("id") or "")
    if "_beats_sota_headlines_pos" in oid or oid.endswith("_beats_sota_headlines_pos"):
        module = str(ob.get("lean_module") or "")
        module_name = humanize_domain_key(module.replace("Priors", "").replace(".lean", ""))
        sym = str(ob.get("symbol") or "").replace("_beats_sota_headlines", "_headline_count")
        enriched["display_label"] = f"{module_name}: {humanize_domain_key(sym)} — {_HEADLINE_COUNT_KIND}"
        enriched["preferred_id_alias"] = oid.replace("_beats_sota_headlines_pos", "_headline_count_pos")
    else:
        enriched["display_label"] = resolve_obligation_label(ob)
    return enriched


def annotate_record(record: dict) -> dict:
    enriched = dict(record)
    labels = resolve_record_label(record)
    enriched.update(labels)
    if labels.get("rule_display_name"):
        enriched["display_name"] = labels["rule_display_name"]
    elif labels.get("prediction_display_name"):
        enriched["display_name"] = labels["prediction_display_name"]
    elif labels.get("section_display_name"):
        enriched["display_name"] = labels["section_display_name"]
    elif not enriched.get("display_name"):
        enriched["display_name"] = humanize_domain_key(str(record.get("name") or record.get("property") or ""))
    return enriched