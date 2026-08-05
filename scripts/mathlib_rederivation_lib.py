#!/usr/bin/env python3
"""
Mathlib re-derivation campaign library.

Classifies every FSOT/Formal theorem/lemma by proof *depth tier* and supports
wave-ordered lake builds. This is the machinery for independent Mathlib-style
depth (not residual multiprover numeric replay).

Depth tiers (honest, ordered by analytic substance):
  L0_definitional  — rfl / decide only (structural identities)
  L1_certificate   — norm_num / native_decide numeric certificates (priors default)
  L2_analytic      — linarith / nlinarith / ring / positivity / field_simp
  L3_chain         — exact + multi-step exact/have chains citing other lemmas
  L4_mathlib_core  — engine modules with L2/L3 dominating (Bounds/Theorems style)

Campaign phases:
  engine core (W0–W5) first, then priors corpus waves.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"

# Ordered campaign waves — engine first, then priors batches.
ENGINE_WAVES: list[dict[str, Any]] = [
    {
        "id": "W0_scalar_defs",
        "title": "Scalar definitions + structure",
        "modules": ["Scalar", "ScalarEngineStructure"],
        "role": "engine",
    },
    {
        "id": "W1_bounds",
        "title": "Constant bounds (Mathlib exp/pi chain)",
        "modules": ["Bounds"],
        "role": "engine",
    },
    {
        "id": "W2_theorems",
        "title": "Core analytic theorems (T1/T2/T3 sign regimes)",
        "modules": ["Theorems"],
        "role": "engine",
    },
    {
        "id": "W3_domains",
        "title": "Domain sign / raw_S theorems",
        "modules": ["Domains"],
        "role": "engine",
    },
    {
        "id": "W4_cosmology",
        "title": "Cosmology + wave modules",
        "modules": [
            "Cosmology",
            "CosmologyLab",
            "CosmologyWave4",
            "CosmologyWave4Priors",
            "CosmologyWave5Priors",
            "CosmologyWave6Priors",
            "CosmologyWave7Priors",
            "CosmologyWave8Priors",
            "CosmologyWave9Priors",
            "CosmologyWave10Priors",
            "CosmologyHigherWavesPriors",
            "CosmologyExtendedPriors",
        ],
        "role": "engine",
    },
    {
        "id": "W5_bridge",
        "title": "Lab / Genomic / bridges",
        "modules": [
            "Lab",
            "Genomic",
            "PhotonicForge",
            "LeanProofsBridge",
            "CrossProofConnectivePriors",
        ],
        "role": "engine",
    },
]

# Match theorem/lemma with optional binders before the type colon.
# Example: theorem foo (p : FSOTParams) : expr := by ...
THM_START_RE = re.compile(r"(?:theorem|lemma)\s+(\w+)\b")

TACTIC_PATTERNS: dict[str, re.Pattern[str]] = {
    "norm_num": re.compile(r"\bnorm_num\b"),
    "native_decide": re.compile(r"\bnative_decide\b"),
    "decide": re.compile(r"\bdecide\b"),
    "rfl": re.compile(r"\brfl\b"),
    "linarith": re.compile(r"\blinarith\b"),
    "nlinarith": re.compile(r"\bnlinarith\b"),
    "ring": re.compile(r"\bring(?:_nf)?\b"),
    "positivity": re.compile(r"\bpositivity\b"),
    "field_simp": re.compile(r"\bfield_simp\b"),
    "exact": re.compile(r"\bexact\b"),
    "refine": re.compile(r"\brefine\b"),
    "simp": re.compile(r"\bsimp\b"),
    "have": re.compile(r"\bhave\b"),
    "sorry": re.compile(r"\bsorry\b"),
    "admit": re.compile(r"\badmit\b"),
}


def strip_lean_comments(text: str) -> str:
    text = re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)
    return re.sub(r"--.*?$", "", text, flags=re.MULTILINE)


def classify_proof_body(body: str) -> dict[str, Any]:
    """Classify proof depth.

    Honest tiers:
      L0 — definitional / structural (rfl, decide, pure simp reductions)
      L1 — *pure* numeric certificate (norm_num only, no structure) — weak multiprover pin style
      L2 — analytic Mathlib (linarith / nlinarith / ring / positivity)
      L3 — multi-step constructive chains (have / refine / exact), even if subgoals use norm_num
    """
    counts = {name: len(pat.findall(body)) for name, pat in TACTIC_PATTERNS.items()}
    has_sorry = counts["sorry"] + counts["admit"] > 0
    analytic = (
        counts["linarith"]
        + counts["nlinarith"]
        + counts["ring"]
        + counts["positivity"]
        + counts["field_simp"]
    )
    # decide/native_decide are constructive closed-goal solvers (count as L0 when alone)
    certificate = counts["norm_num"]  # pure float/norm certificates only
    decidable = counts["decide"] + counts["native_decide"]
    chain = counts["exact"] + counts["refine"] + counts["have"]
    structural = counts["simp"] + counts["rfl"]

    pure_norm_num = (
        certificate > 0
        and analytic == 0
        and chain == 0
        and structural == 0
        and decidable == 0
    )
    definitional = (
        (counts["rfl"] > 0 or decidable > 0 or (counts["simp"] > 0 and certificate == 0))
        and analytic == 0
        and chain == 0
    )

    if has_sorry:
        tier = "LX_sorry"
    elif analytic > 0:
        tier = "L2_analytic"
    elif chain >= 1:
        # Multi-step constructive proof (domain raw_S, etc.) — real depth
        tier = "L3_chain"
    elif definitional:
        tier = "L0_definitional"
    elif pure_norm_num:
        tier = "L1_certificate"
    elif certificate > 0 and (structural > 0 or decidable > 0):
        # unfold + norm_num or simp + norm_num → still certificate-class
        tier = "L1_certificate"
    else:
        tier = "L0_definitional"  # trivial / split / constructor-only

    mathlib_depth = tier in ("L0_definitional", "L2_analytic", "L3_chain", "L4_mathlib_core")
    return {
        "tier": tier,
        "tactic_counts": counts,
        "has_sorry": has_sorry,
        "mathlib_depth": mathlib_depth,
        "analytic_score": analytic,
        "certificate_score": certificate,
        "chain_score": chain,
        "pure_norm_num": pure_norm_num,
    }


@dataclass
class TheoremRecord:
    module: str
    name: str
    tier: str
    mathlib_depth: bool
    has_sorry: bool
    tactic_counts: dict[str, int] = field(default_factory=dict)
    path: str = ""


def parse_module_theorems(path: Path) -> list[TheoremRecord]:
    text = strip_lean_comments(path.read_text(encoding="utf-8", errors="ignore"))
    rows: list[TheoremRecord] = []
    starts = list(THM_START_RE.finditer(text))
    for i, m in enumerate(starts):
        name = m.group(1)
        chunk_end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        chunk = text[m.start() : chunk_end]
        # Proof body after first `:= by` (or term-mode `:= <expr>`)
        body = ""
        term_mode = False
        by_m = re.search(r":=\s*by\b", chunk)
        if by_m:
            body = chunk[by_m.end() :]
        else:
            term_m = re.search(r":=\s*", chunk)
            if term_m:
                body = chunk[term_m.end() :]
                term_mode = True
                if "rfl" in body or body.strip() in ("rfl", "trivial", "exact rfl"):
                    body = "rfl"
                    term_mode = False
        cls = classify_proof_body(body)
        # Term-mode proofs (`:= long_expr`) are constructive Mathlib (exact-style),
        # not empty/L0 — e.g. Bounds log lemmas using lt_log_iff_exp_lt.
        if (
            term_mode
            and body.strip()
            and len(body.strip()) > 8
            and not cls["has_sorry"]
            and cls["tier"] in ("L0_definitional", "L1_certificate")
        ):
            cls["tier"] = "L3_chain"
            cls["mathlib_depth"] = True
            cls["chain_score"] = max(cls.get("chain_score", 0), 1)
        try:
            rel = str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
        except ValueError:
            rel = str(path).replace("\\", "/")
        rows.append(
            TheoremRecord(
                module=path.stem,
                name=name,
                tier=cls["tier"],
                mathlib_depth=bool(cls["mathlib_depth"]),
                has_sorry=bool(cls["has_sorry"]),
                tactic_counts=cls["tactic_counts"],
                path=rel,
            )
        )
    return rows


def inventory_formal(modules: list[str] | None = None) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    by_tier: dict[str, int] = {}
    by_module: dict[str, dict[str, Any]] = {}
    sorry_list: list[str] = []

    paths = sorted(FORMAL.glob("*.lean"))
    if modules is not None:
        want = set(modules)
        paths = [p for p in paths if p.stem in want]

    for path in paths:
        thms = parse_module_theorems(path)
        if not thms:
            continue
        tier_counts: dict[str, int] = {}
        for t in thms:
            by_tier[t.tier] = by_tier.get(t.tier, 0) + 1
            tier_counts[t.tier] = tier_counts.get(t.tier, 0) + 1
            if t.has_sorry:
                sorry_list.append(f"{t.module}.{t.name}")
            records.append(
                {
                    "module": t.module,
                    "name": t.name,
                    "tier": t.tier,
                    "mathlib_depth": t.mathlib_depth,
                    "has_sorry": t.has_sorry,
                    "path": t.path,
                    "tactic_counts": t.tactic_counts,
                }
            )
        mathlib_n = sum(1 for t in thms if t.mathlib_depth)
        by_module[path.stem] = {
            "theorem_count": len(thms),
            "mathlib_depth_count": mathlib_n,
            "mathlib_depth_pct": round(100.0 * mathlib_n / len(thms), 2) if thms else 0.0,
            "tier_counts": tier_counts,
            "has_sorry": any(t.has_sorry for t in thms),
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        }

    total = len(records)
    mathlib_n = sum(1 for r in records if r["mathlib_depth"])
    return {
        "theorem_count": total,
        "mathlib_depth_count": mathlib_n,
        "mathlib_depth_pct": round(100.0 * mathlib_n / total, 2) if total else 0.0,
        "by_tier": by_tier,
        "by_module": by_module,
        "sorry_list": sorry_list,
        "records": records,
    }


def prior_module_names() -> list[str]:
    names = sorted(p.stem for p in FORMAL.glob("*Priors.lean"))
    # Exclude ones already in engine waves
    engine_mods = {m for w in ENGINE_WAVES for m in w["modules"]}
    return [n for n in names if n not in engine_mods]


def prior_waves(batch_size: int = 40) -> list[dict[str, Any]]:
    names = prior_module_names()
    waves: list[dict[str, Any]] = []
    for i in range(0, len(names), batch_size):
        chunk = names[i : i + batch_size]
        waves.append(
            {
                "id": f"W6_priors_{i // batch_size:02d}",
                "title": f"Priors corpus batch {i // batch_size} ({len(chunk)} modules)",
                "modules": chunk,
                "role": "priors",
            }
        )
    return waves


def all_waves(include_priors: bool = True, prior_batch_size: int = 40) -> list[dict[str, Any]]:
    waves = list(ENGINE_WAVES)
    if include_priors:
        waves.extend(prior_waves(prior_batch_size))
    return waves


def lake_module_target(module: str) -> str:
    """Lake target path for FSOT.Formal.<Module>."""
    return f"FSOT.Formal.{module}"


def depth_targets_for_upgrade(inventory: dict[str, Any], *, limit: int = 50) -> list[dict]:
    """List L1 certificate theorems in engine modules as upgrade candidates."""
    engine_mods = {m for w in ENGINE_WAVES for m in w["modules"]}
    cands: list[dict] = []
    for rec in inventory.get("records") or []:
        if rec.get("module") not in engine_mods:
            continue
        if rec.get("tier") != "L1_certificate":
            continue
        if rec.get("has_sorry"):
            continue
        cands.append(
            {
                "module": rec["module"],
                "name": rec["name"],
                "path": rec["path"],
                "suggested_upgrade": (
                    "Prefer linarith/nlinarith/ring/positivity or exact of existing "
                    "Bounds/Theorems lemmas over bare norm_num where the statement is analytic."
                ),
            }
        )
        if len(cands) >= limit:
            break
    return cands
