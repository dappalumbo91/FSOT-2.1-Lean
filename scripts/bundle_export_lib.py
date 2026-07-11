"""Parse Lean structural bundle theorems into bundle_conj cross-proof obligations."""

from __future__ import annotations

import re
from typing import Any

BUNDLE_THEOREM_RE = re.compile(
    r"theorem\s+(\w+_bundle)\s*:\s*(.+?)\s*:=\s*by",
    re.DOTALL,
)
EXACT_WITNESS_RE = re.compile(r"\bexact\s+(\w+)")
NORM_NUM_RE = re.compile(r"\bnorm_num\b")
CONJ_SPLIT_RE = re.compile(r"\s*∧\s*")


def _strip_comments(text: str) -> str:
    return re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)


def _normalize_conjunct(raw: str) -> str:
    s = " ".join(raw.strip().split())
    s = s.strip("()")
    return s


def _parse_float_lit(lit: str) -> float | None:
    lit = lit.strip()
    m = re.fullmatch(r"\(([0-9.eE+-]+)\s*:\s*ℝ\)", lit)
    if m:
        lit = m.group(1)
    try:
        return float(lit)
    except ValueError:
        return None


def _parse_nat_lit(lit: str) -> int | None:
    lit = lit.strip()
    m = re.fullmatch(r"\((\d+)\s*:\s*ℕ\)", lit)
    if m:
        return int(m.group(1))
    if lit.isdigit():
        return int(lit)
    return None


def classify_conjunct(
    conj: str,
    r_defs: dict[str, float],
    n_defs: dict[str, int],
) -> dict[str, Any] | None:
    c = _normalize_conjunct(conj)
    if not c:
        return None

    m = re.fullmatch(r"(\w+)\s*=\s*(\d+)", c)
    if m and m.group(1) in n_defs:
        rhs = int(m.group(2))
        return {
            "kind": "eq_nat",
            "symbol": m.group(1),
            "value": n_defs[m.group(1)],
            "right_value": rhs,
            "statement": f"{n_defs[m.group(1)]} = {rhs}",
            "lean_conjunct": c,
        }

    m = re.fullmatch(r"(\w+)\s*<\s*\(0\.5\s*:\s*ℝ\)", c)
    if m and m.group(1) in r_defs:
        val = r_defs[m.group(1)]
        return {
            "kind": "lt_half",
            "symbol": m.group(1),
            "value": val,
            "statement": f"{val} < 0.5",
            "lean_conjunct": c,
        }

    m = re.fullmatch(r"(\w+)\s*<\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)", c)
    if m and m.group(1) in r_defs:
        bound = _parse_float_lit(m.group(2))
        if bound is not None:
            val = r_defs[m.group(1)]
            return {
                "kind": "lt_lit",
                "symbol": m.group(1),
                "value": val,
                "bound": bound,
                "statement": f"{val} < {bound}",
                "lean_conjunct": c,
            }

    m = re.fullmatch(r"\(0\s*:\s*ℝ\)\s*<\s*(\w+)", c) or re.fullmatch(r"0\s*<\s*(\w+)", c)
    if m:
        sym = m.group(1)
        if sym in n_defs:
            return {
                "kind": "nat_pos",
                "symbol": sym,
                "value": n_defs[sym],
                "statement": f"0 < {n_defs[sym]}",
                "lean_conjunct": c,
            }
        if sym in r_defs:
            return {
                "kind": "pos",
                "symbol": sym,
                "value": r_defs[sym],
                "statement": f"0 < {r_defs[sym]}",
                "lean_conjunct": c,
            }

    m = re.fullmatch(r"(\w+)\s*>\s*0", c)
    if m:
        sym = m.group(1)
        if sym in n_defs:
            return {
                "kind": "nat_pos",
                "symbol": sym,
                "value": n_defs[sym],
                "statement": f"0 < {n_defs[sym]}",
                "lean_conjunct": c,
            }
        if sym in r_defs:
            return {
                "kind": "pos",
                "symbol": sym,
                "value": r_defs[sym],
                "statement": f"0 < {r_defs[sym]}",
                "lean_conjunct": c,
            }

    m = re.fullmatch(r"raw_S\s*\(get_domain_params\s+\"(\w+)\"\)\s*>\s*0", c)
    if m:
        return {
            "kind": "pos",
            "symbol": f"raw_S_{m.group(1)}",
            "value": 1.0,
            "statement": f"raw_S({m.group(1)}) > 0",
            "lean_conjunct": c,
            "opaque": True,
        }

    return {
        "kind": "opaque_conj",
        "statement": c,
        "lean_conjunct": c,
    }


def _extract_proof_body(text: str, theorem: str) -> str:
    m = re.search(rf"theorem\s+{re.escape(theorem)}\s*:.+?:=\s*by", text, re.DOTALL)
    if not m:
        return ""
    start = m.end()
    rest = text[start:]
    depth = 0
    i = 0
    while i < len(rest):
        ch = rest[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif rest.startswith("theorem ", i) and depth == 0:
            break
        elif rest.startswith("end", i) and depth == 0:
            break
        i += 1
    return rest[:i]


def _witness_ids(proof_body: str) -> list[str | None]:
    witnesses: list[str | None] = []
    if "refine ⟨" in proof_body or "refine \u27e8" in proof_body:
        for line in proof_body.splitlines():
            line = line.strip()
            em = EXACT_WITNESS_RE.search(line)
            if em:
                witnesses.append(em.group(1))
            elif NORM_NUM_RE.search(line) and line.startswith("by"):
                witnesses.append(None)
            elif em := EXACT_WITNESS_RE.search(line.removeprefix("·").strip()):
                witnesses.append(em.group(1))
        if witnesses:
            return witnesses
    for em in EXACT_WITNESS_RE.finditer(proof_body):
        witnesses.append(em.group(1))
    return witnesses


def parse_bundle_obligations(
    text: str,
    *,
    r_defs: dict[str, float],
    n_defs: dict[str, int],
    atomic_by_id: dict[str, dict],
    lean_module: str,
    source_file: str,
    source_tier: str,
) -> list[dict]:
    clean = _strip_comments(text)
    out: list[dict] = []
    for m in BUNDLE_THEOREM_RE.finditer(clean):
        bundle_id = m.group(1)
        type_body = m.group(2).strip()
        conjunct_texts = [_normalize_conjunct(p) for p in CONJ_SPLIT_RE.split(type_body) if p.strip()]
        proof_body = _extract_proof_body(clean, bundle_id)
        witnesses = _witness_ids(proof_body)

        conjuncts: list[dict] = []
        for idx, conj_text in enumerate(conjunct_texts):
            row = classify_conjunct(conj_text, r_defs, n_defs) or {
                "kind": "opaque_conj",
                "statement": conj_text,
                "lean_conjunct": conj_text,
            }
            row["index"] = idx
            witness = witnesses[idx] if idx < len(witnesses) else None
            if witness:
                row["proof_witness_id"] = witness
                row["proof_style"] = "exact"
                if witness in atomic_by_id:
                    row["linked_obligation_id"] = witness
            elif NORM_NUM_RE.search(proof_body):
                row["proof_style"] = "norm_num"
            linked = row.get("linked_obligation_id")
            if not linked and row.get("kind") not in ("opaque_conj",):
                for aid, aob in atomic_by_id.items():
                    if aob.get("kind") == row.get("kind") and aob.get("symbol") == row.get("symbol"):
                        row["linked_obligation_id"] = aid
                        break
            conjuncts.append(row)

        unparsed = sum(1 for c in conjuncts if c.get("kind") == "opaque_conj")
        exportable = len(conjuncts) - unparsed
        statement = " ∧ ".join(c.get("statement", c.get("lean_conjunct", "")) for c in conjuncts)
        out.append(
            {
                "id": bundle_id,
                "kind": "bundle_conj",
                "lean_theorem": bundle_id,
                "statement": statement,
                "lean_statement": type_body.replace("\n", " ").strip(),
                "conjunct_count": len(conjuncts),
                "conjuncts": conjuncts,
                "proof_witness_ids": [c.get("proof_witness_id") for c in conjuncts],
                "unparsed_conjunct_count": unparsed,
                "exportable_conjunct_count": exportable,
                "lean_module": lean_module,
                "source_file": source_file,
                "source_tier": source_tier,
                "cross_proof_role": "structural_index",
            }
        )
    return out