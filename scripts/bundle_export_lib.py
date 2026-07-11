"""Parse Lean structural bundle theorems into bundle_conj cross-proof obligations."""

from __future__ import annotations

import re
from typing import Any

BUNDLE_THEOREM_RE = re.compile(
    r"theorem\s+(\w+)\s*:\s*((?:(?!\n(?:theorem|lemma)\s).)+)\s*:=\s*by",
    re.DOTALL,
)
EXACT_WITNESS_RE = re.compile(r"\bexact\s+(\w+)")
NORM_NUM_RE = re.compile(r"\bnorm_num\b")
CONJ_SPLIT_RE = re.compile(r"\s*∧\s*")


def _strip_comments(text: str) -> str:
    return re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)


def _normalize_conjunct(raw: str) -> str:
    s = " ".join(raw.strip().split())
    s = s.replace("≤", "<=").replace("≥", ">=")
    s = re.sub(r":\s*ℤ", "", s)
    s = re.sub(r":\s*ℕ", "", s)
    if s.startswith("(") and s.endswith(")"):
        depth = 0
        wraps = True
        for i, ch in enumerate(s):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0 and i != len(s) - 1:
                    wraps = False
                    break
        if wraps:
            s = s[1:-1].strip()
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

    m = re.fullmatch(r"4 \* phi \^ 3 \+ 8 / phi \^ 2 = (\d+)", c)
    if m and "phi" in r_defs:
        try:
            from cross_proof_lib import _eval_r_expr  # noqa: WPS433

            val = _eval_r_expr("4 * phi ^ 3 + 8 / phi ^ 2", r_defs, n_defs)
            rhs = int(m.group(1))
            if val is not None and abs(val - rhs) < 1e-6:
                return {
                    "kind": "r_eq_lit",
                    "left_expr": "4 * phi ^ 3 + 8 / phi ^ 2",
                    "value": val,
                    "right_value": float(rhs),
                    "statement": f"{val} = {rhs}",
                    "lean_conjunct": c,
                }
        except Exception:
            pass

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

    m = re.fullmatch(r"(\w+)\s*\*\s*(\d+)\s*=\s*(\w+)", c)
    if m and m.group(1) in n_defs and m.group(3) in n_defs:
        lhs = n_defs[m.group(1)] * int(m.group(2))
        rhs = n_defs[m.group(3)]
        if lhs == rhs:
            return {
                "kind": "eq_nat_arith",
                "symbol": m.group(1),
                "value": lhs,
                "right_value": float(rhs),
                "statement": f"{lhs} = {rhs}",
                "lean_conjunct": c,
            }

    m = re.fullmatch(r"(\w+)\s*\^\s*(\d+)\s*=\s*(\d+)", c)
    if m and m.group(1) in n_defs:
        lhs = n_defs[m.group(1)] ** int(m.group(2))
        rhs = int(m.group(3))
        if lhs == rhs:
            return {
                "kind": "eq_nat_arith",
                "symbol": m.group(1),
                "value": float(lhs),
                "right_value": float(rhs),
                "statement": f"{lhs} = {rhs}",
                "lean_conjunct": c,
            }

    m = re.fullmatch(r"(\w+)\s*\+\s*(\w+)\s*\+\s*(\w+)\s*=\s*(\w+)", c)
    if m and all(m.group(i) in n_defs for i in range(1, 5)):
        lhs = n_defs[m.group(1)] + n_defs[m.group(2)] + n_defs[m.group(3)]
        rhs = n_defs[m.group(4)]
        if lhs == rhs:
            return {
                "kind": "eq_nat_arith",
                "symbol": m.group(1),
                "value": float(lhs),
                "right_value": float(rhs),
                "statement": f"{lhs} = {rhs}",
                "lean_conjunct": c,
            }

    m = re.fullmatch(r"(\w+)\s*\+\s*(\w+)\s*=\s*(\w+)", c)
    if m and all(m.group(i) in n_defs for i in range(1, 4)):
        lhs = n_defs[m.group(1)] + n_defs[m.group(2)]
        rhs = n_defs[m.group(3)]
        if lhs == rhs:
            return {
                "kind": "eq_nat_arith",
                "symbol": m.group(1),
                "value": float(lhs),
                "right_value": float(rhs),
                "statement": f"{lhs} = {rhs}",
                "lean_conjunct": c,
            }

    m = re.fullmatch(r"\(\((\d+)\s*:\s*ℝ\)\s*/\s*(\d+)\)\s*\^\s*(\d+)\s*=\s*\((\d+)\s*:\s*ℝ\)\s*/\s*(\d+)", c)
    if m:
        lhs = (int(m.group(1)) / int(m.group(2))) ** int(m.group(3))
        rhs = int(m.group(4)) / int(m.group(5))
        if abs(lhs - rhs) < 1e-9:
            return {
                "kind": "r_eq_lit",
                "value": lhs,
                "right_value": rhs,
                "statement": f"{lhs} = {rhs}",
                "lean_conjunct": c,
            }

    m = re.fullmatch(r"\((\d+)\s*:\s*ℝ\)\s*/\s*(\d+)\s*=\s*([0-9.eE+-]+)", c)
    if m:
        lhs = int(m.group(1)) / int(m.group(2))
        rhs = float(m.group(3))
        if abs(lhs - rhs) < 1e-9:
            return {
                "kind": "r_eq_lit",
                "value": lhs,
                "right_value": rhs,
                "statement": f"{lhs} = {rhs}",
                "lean_conjunct": c,
            }

    m = re.fullmatch(r"\((\d+)\s*:\s*ℝ\)\s*\^\s*(\d+)\s*=\s*(\d+)", c)
    if m:
        lhs = int(m.group(1)) ** int(m.group(2))
        rhs = int(m.group(3))
        if lhs == rhs:
            return {
                "kind": "r_eq_lit",
                "value": float(lhs),
                "right_value": float(rhs),
                "statement": f"{lhs} = {rhs}",
                "lean_conjunct": c,
            }

    m = re.fullmatch(r"\((\w+),\s*(\w+),\s*(\w+)\)\s*=\s*\((\d+),\s*(\d+),\s*(\d+)\)", c)
    if m and all(m.group(i) in n_defs for i in range(1, 4)):
        if (
            n_defs[m.group(1)] == int(m.group(4))
            and n_defs[m.group(2)] == int(m.group(5))
            and n_defs[m.group(3)] == int(m.group(6))
        ):
            return {
                "kind": "int_tuple3_eq",
                "symbols": [m.group(1), m.group(2), m.group(3)],
                "values": [n_defs[m.group(1)], n_defs[m.group(2)], n_defs[m.group(3)]],
                "right_values": [int(m.group(4)), int(m.group(5)), int(m.group(6))],
                "statement": f"({n_defs[m.group(1)]}, {n_defs[m.group(2)]}, {n_defs[m.group(3)]})",
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

    m = re.fullmatch(r"\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*<\s*(\w+)", c)
    if m:
        bound = _parse_float_lit(m.group(1))
        sym = m.group(2)
        if bound is not None and sym in r_defs:
            val = r_defs[sym]
            return {
                "kind": "gt_lit",
                "symbol": sym,
                "value": val,
                "bound": bound,
                "statement": f"{val} > {bound}",
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

    m = re.fullmatch(r"\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*<\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)", c)
    if m:
        left = _parse_float_lit(m.group(1))
        right = _parse_float_lit(m.group(2))
        if left is not None and right is not None:
            return {
                "kind": "r_lt_lit_pure",
                "left_value": left,
                "right_value": right,
                "statement": f"{left} < {right}",
                "lean_conjunct": c,
            }

    m = re.fullmatch(r"\((\d+)\s*:\s*ℕ\)\s*<\s*(\w+)", c)
    if m and m.group(2) in n_defs:
        return {
            "kind": "nat_gt_lit",
            "symbol": m.group(2),
            "value": n_defs[m.group(2)],
            "bound": int(m.group(1)),
            "statement": f"{m.group(1)} < {n_defs[m.group(2)]}",
            "lean_conjunct": c,
        }

    m = re.fullmatch(r"(\w+)\s*(?:≤|<=)\s*(\w+)", c)
    if m and m.group(1) in n_defs and m.group(2) in n_defs:
        left = n_defs[m.group(1)]
        right = n_defs[m.group(2)]
        if left <= right:
            return {
                "kind": "nat_le_sym",
                "left": m.group(1),
                "right": m.group(2),
                "value": left,
                "right_value": right,
                "statement": f"{left} <= {right}",
                "lean_conjunct": c,
            }

    m = re.fullmatch(r"(\w+)\s*(?:≤|<=)\s*(\w+)", c)
    if m and m.group(1) in r_defs and m.group(2) in r_defs:
        if r_defs[m.group(1)] <= r_defs[m.group(2)]:
            return {
                "kind": "r_le_sym",
                "symbol": m.group(1),
                "value": r_defs[m.group(1)],
                "right_value": r_defs[m.group(2)],
                "statement": f"{r_defs[m.group(1)]} <= {r_defs[m.group(2)]}",
                "lean_conjunct": c,
            }

    m = re.fullmatch(r"(\w+)\s*(?:≤|<=)\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)", c)
    if m and m.group(1) in r_defs:
        bound = _parse_float_lit(m.group(2))
        if bound is not None:
            val = r_defs[m.group(1)]
            return {
                "kind": "r_le_lit",
                "symbol": m.group(1),
                "value": val,
                "bound": bound,
                "statement": f"{val} <= {bound}",
                "lean_conjunct": c,
            }

    m = re.fullmatch(r"(\w+)\s*>\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)", c)
    if m and m.group(1) in n_defs:
        bound = _parse_float_lit(m.group(2))
        if bound is not None:
            return {
                "kind": "nat_gt_lit",
                "symbol": m.group(1),
                "value": n_defs[m.group(1)],
                "bound": int(bound) if bound == int(bound) else int(bound),
                "statement": f"{n_defs[m.group(1)]} > {bound}",
                "lean_conjunct": c,
            }
    if m and m.group(1) in r_defs:
        bound = _parse_float_lit(m.group(2))
        if bound is not None:
            return {
                "kind": "gt_lit",
                "symbol": m.group(1),
                "value": r_defs[m.group(1)],
                "bound": bound,
                "statement": f"{r_defs[m.group(1)]} > {bound}",
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

    m = re.fullmatch(
        r"\|\((.+?)\)\s*-\s*(\d+)\|\s*<\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)",
        c,
    )
    if m:
        bound = _parse_float_lit(m.group(3))
        if bound is not None:
            inner = m.group(1)
            target = int(m.group(2))
            val = None
            if "phi ^ 5" in inner and "phi ^ (-5" in inner:
                try:
                    from cross_proof_lib import _eval_r_expr  # noqa: WPS433

                    expr_val = _eval_r_expr(
                        f"abs((2 * (phi ^ 5 - phi ^ -5)) - {target})",
                        r_defs,
                        n_defs,
                    )
                    if expr_val is not None:
                        val = expr_val
                except Exception:
                    pass
            row: dict[str, Any] = {
                "kind": "abs_diff_lt_lit",
                "left_expr": inner,
                "right": str(target),
                "bound": bound,
                "statement": f"|({inner}) - {target}| < {bound}",
                "lean_conjunct": c,
            }
            if val is not None:
                row["diff"] = val
                row["value"] = val
                row["statement"] = f"{val} < {bound}"
            return row

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
        elif depth == 0:
            if rest.startswith("theorem ", i):
                break
            if re.match(r"\bend\b", rest[i:]):
                break
        i += 1
    return rest[:i]


def _atomic_candidates(sym: str, kind: str | None, val: object | None) -> list[str]:
    val_suffix = ""
    if val is not None and kind == "eq_nat":
        try:
            val_suffix = f"_eq_{int(val)}"
        except (TypeError, ValueError):
            pass
    cands = [
        f"{sym}_pos",
        f"{sym}{val_suffix}",
        f"{sym}_eq_nat",
        sym,
    ]
    if kind in ("lt_lit", "lt_half"):
        cands.extend([f"{sym}_under_half_pct", f"{sym}_in_bounds"])
    if kind == "gt_lit":
        cands.append(f"{sym}_in_bounds")
    if sym.endswith("_pooled_median_error_pct"):
        base = sym[: -len("_pooled_median_error_pct")]
        cands.append(f"{base}_pooled_median_under_half_pct")
    if sym.endswith("_headline_median_error_pct"):
        base = sym[: -len("_headline_median_error_pct")]
        cands.append(f"{base}_headline_median_under_half_pct")
    if sym.endswith("_median_error_pct"):
        base = sym[: -len("_median_error_pct")]
        cands.append(f"{base}_median_under_half_pct")
    if kind == "nat_le_sym":
        left = row.get("left") or sym
        if left:
            cands.extend(
                [
                    f"{left}_match_le_total",
                    f"{left}_le_total",
                ]
            )
            right = row.get("right")
            if right:
                cands.append(f"{left}_le_{right}")
    if kind == "abs_diff_lt_lit":
        cands.extend(
            [
                "autosome_haploid_count_eq_twenty_two",
                "codon_trinary_degeneracy_eq",
            ]
        )
    if kind == "r_eq_lit" and row.get("lean_conjunct", "").find("4 : ℝ) / 3") >= 0:
        cands.append("codon_trinary_degeneracy_eq")
    if kind == "eq_nat_arith" and sym:
        for suffix in ("_counts_sum", "_from_dna", "_count_eq", "_sum"):
            if sym.endswith("_plus") or sym.endswith("_count"):
                base = sym.rsplit("_", 1)[0]
                cands.append(f"{base}_genetic_counts_sum")
                cands.append(f"{base}_counts_sum")
            cands.append(f"{sym}_from_dna")
        if sym.endswith("_count"):
            cands.append(f"{sym[:-6]}_from_dna")
            cands.append(f"{sym}_from_dna")
        if "genetic_plus" in sym or sym.endswith("_plus"):
            region = sym.replace("_genetic_plus", "").replace("_plus", "")
            cands.append(f"{region}_genetic_counts_sum")
        if sym.endswith("_spin_plus"):
            region = sym[: -len("_spin_plus")]
            cands.append(f"{region}_spin_counts_sum")
        if sym == "genetic_trinary_alphabet_card":
            cands.append("brain_prior_codon_pattern_space_eq_twenty_seven")
        if sym.endswith("_count") and "_codon" in sym:
            cands.append("brain_prior_codon_from_dna")
    return cands


def _find_atomic_link(
    row: dict,
    atomic_by_id: dict[str, dict],
) -> str | None:
    sym = row.get("symbol")
    kind = row.get("kind")
    val = row.get("value")
    if row.get("proof_witness_id") and row["proof_witness_id"] in atomic_by_id:
        return row["proof_witness_id"]
    if sym:
        for cand in _atomic_candidates(sym, kind, val):
            if cand in atomic_by_id:
                return cand
        for aid, aob in atomic_by_id.items():
            if aob.get("symbol") == sym and aob.get("kind") == kind:
                return aid
            if sym in aid and aob.get("kind") in (kind, "nat_pos", "eq_nat", "lt_lit", "gt_lit"):
                return aid
    if row.get("kind") == "opaque_conj":
        stmt = row.get("statement") or ""
        for tok in re.findall(r"[a-z][a-z0-9_]*", stmt):
            for cand in (
                tok,
                f"{tok}_in_bounds",
                f"{tok}_under_half_pct",
                f"{tok}_match_le_total",
            ):
                if cand in atomic_by_id:
                    return cand
    left = row.get("left")
    if left and row.get("kind") == "nat_le_sym":
        for cand in (f"{left}_match_le_total", f"{left}_le_total"):
            if cand in atomic_by_id:
                return cand
    return None


def _split_refine_tuple(content: str) -> list[str]:
    items: list[str] = []
    depth = 0
    current: list[str] = []
    for ch in content:
        if ch in "([{⟨<":
            depth += 1
        elif ch in ")]}⟩>":
            depth -= 1
        if ch == "," and depth == 0:
            item = "".join(current).strip()
            if item:
                items.append(item)
            current = []
        else:
            current.append(ch)
    item = "".join(current).strip()
    if item:
        items.append(item)
    return items


def _refine_item_witness(item: str) -> str | None:
    item = item.strip().lstrip("·").strip()
    if not item:
        return None
    if item.startswith("by ") or (NORM_NUM_RE.search(item) and "exact" not in item):
        return None
    em = EXACT_WITNESS_RE.search(item)
    if em:
        return em.group(1)
    m = re.match(r"^(\w+)", item)
    return m.group(1) if m else None


def _witness_ids(proof_body: str) -> list[str | None]:
    witnesses: list[str | None] = []
    refine_m = re.search(r"refine\s*[⟨<](.+?)[⟩>]", proof_body, re.DOTALL)
    if refine_m:
        for item in _split_refine_tuple(refine_m.group(1)):
            witnesses.append(_refine_item_witness(item))
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
        if "∧" not in type_body:
            continue
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
            elif row.get("kind") == "eq_nat" or NORM_NUM_RE.search(proof_body):
                row["proof_style"] = "norm_num"
            linked = _find_atomic_link(row, atomic_by_id)
            if linked:
                row["linked_obligation_id"] = linked
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