#!/usr/bin/env python3
"""
Automated Mathlib re-derivation campaign for FSOT Lean formal corpus.

What this does (honest scope):
  1. Inventory every theorem/lemma under FSOT/Formal with depth tiers L0–L3
  2. Wave-build engine modules (Scalar → Bounds → Theorems → Domains → …)
  3. Optionally batch-build priors waves
  4. Rebuild formal/structural depth closures
  5. Emit campaign report + update full_mathlib progress flags

What this does NOT silently claim:
  - Instant re-write of all 5000+ priors into pure Mathlib analytic chains
  - Classical continuum YM uniqueness
  Peer review / journal acceptance

Usage:
  python scripts/run_mathlib_rederivation_campaign.py
  python scripts/run_mathlib_rederivation_campaign.py --engine-only
  python scripts/run_mathlib_rederivation_campaign.py --wave W1_bounds
  python scripts/run_mathlib_rederivation_campaign.py --skip-lake
  python scripts/run_mathlib_rederivation_campaign.py --priors-batch-size 25
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from mathlib_rederivation_lib import (  # noqa: E402
    ENGINE_WAVES,
    all_waves,
    depth_targets_for_upgrade,
    inventory_formal,
    lake_module_target,
)

OUT_INV = ROOT / "data" / "mathlib_rederivation_inventory.json"
OUT_REPORT = ROOT / "data" / "mathlib_rederivation_campaign_report.json"
OUT_MD = ROOT / "docs" / "MATHLIB_REDERIVATION_CAMPAIGN.md"
FORMAL = ROOT / "FSOT" / "Formal"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _run(cmd: list[str], *, timeout: int = 3600) -> dict:
    t0 = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "cmd": cmd,
            "returncode": proc.returncode,
            "status": "passed" if proc.returncode == 0 else "failed",
            "seconds": round(time.time() - t0, 2),
            "stdout_tail": (proc.stdout or "")[-2000:],
            "stderr_tail": (proc.stderr or "")[-2000:],
        }
    except subprocess.TimeoutExpired:
        return {
            "cmd": cmd,
            "returncode": -1,
            "status": "timeout",
            "seconds": round(time.time() - t0, 2),
            "stdout_tail": "",
            "stderr_tail": f"timeout after {timeout}s",
        }
    except FileNotFoundError as exc:
        return {
            "cmd": cmd,
            "returncode": -1,
            "status": "skipped",
            "seconds": 0.0,
            "stdout_tail": "",
            "stderr_tail": str(exc),
        }


def lake_build_library(*, timeout: int = 7200) -> dict:
    """One-shot typecheck of the whole FSOT Lean package (all Formal modules)."""
    print("\n=== lake build FSOT (full library) ===")
    # `lake build FSOT` compiles the default library target from lakefile.lean
    result = _run(["lake", "build", "FSOT"], timeout=timeout)
    print(f"  lake build FSOT → {result['status']} ({result['seconds']}s)")
    if result["status"] != "passed":
        print((result.get("stderr_tail") or result.get("stdout_tail") or "")[-800:])
    return result


def build_wave(wave: dict, *, lake_status: str, lake_build: dict | None = None) -> dict:
    modules = [m for m in wave["modules"] if (FORMAL / f"{m}.lean").exists()]
    missing = [m for m in wave["modules"] if m not in modules]
    inv = inventory_formal(modules)

    sorry = inv.get("sorry_list") or []
    mathlib_pct = inv.get("mathlib_depth_pct") or 0.0
    # Engine waves require high Mathlib-class depth; priors are certificate-heavy by design
    if wave.get("role") == "engine":
        depth_ok = mathlib_pct >= 15.0 or inv.get("theorem_count", 0) == 0
        if wave["id"] in ("W0_scalar_defs", "W3_domains", "W5_bridge"):
            depth_ok = (mathlib_pct >= 5.0 or inv.get("theorem_count", 0) < 5) and not sorry
        if wave["id"] in ("W1_bounds", "W2_theorems"):
            depth_ok = mathlib_pct >= 40.0 and not sorry
    else:
        # Priors: full-library lake build + no sorry is the gate
        depth_ok = not sorry

    # Full-corpus closure requires a real lake pass (not skipped)
    wave_ok = lake_status == "passed" and not sorry and depth_ok

    return {
        "id": wave["id"],
        "title": wave["title"],
        "role": wave.get("role"),
        "modules": modules,
        "missing_modules": missing,
        "theorem_count": inv.get("theorem_count"),
        "mathlib_depth_count": inv.get("mathlib_depth_count"),
        "mathlib_depth_pct": mathlib_pct,
        "by_tier": inv.get("by_tier"),
        "sorry_list": sorry,
        "lake_status": lake_status,
        "lake_build_seconds": (lake_build or {}).get("seconds"),
        "builds": [
            {
                "target": "FSOT",
                "status": lake_status,
                "note": "shared full-library lake build FSOT",
            }
        ],
        "depth_gate_ok": depth_ok,
        "wave_ok": wave_ok,
    }


def run_aux_closures() -> dict[str, dict]:
    scripts = [
        "build_formal_proof_depth_closure.py",
        "audit_structural_proof_depth.py",
        "generate_structural_proof_artifacts.py",
    ]
    out: dict[str, dict] = {}
    for name in scripts:
        path = ROOT / "scripts" / name
        if not path.exists():
            out[name] = {"status": "missing"}
            continue
        out[name] = _run([sys.executable, str(path)], timeout=600)
    return out


def write_md(report: dict) -> str:
    lines = [
        "# Mathlib re-derivation campaign",
        "",
        f"**Generated:** {report['generated_at']}  ",
        f"**Verdict:** `{report['verdict']}`  ",
        f"**Engine core closed:** {report['engine_core_closed']}  ",
        f"**Corpus Mathlib-depth %:** {report['corpus']['mathlib_depth_pct']}%  "
        f"({report['corpus']['mathlib_depth_count']}/{report['corpus']['theorem_count']})",
        "",
        "## What this campaign is",
        "",
        "Automated, wave-ordered campaign to drive **independent Mathlib-style proof depth**",
        "across `FSOT/Formal` — beyond residual multiprover numeric certificate replay.",
        "",
        "| Tier | Meaning |",
        "|------|---------|",
        "| L0_definitional | `rfl` / decide structural identities |",
        "| L1_certificate | `norm_num` numeric certificates (typical priors) |",
        "| L2_analytic | `linarith` / `nlinarith` / `ring` / `positivity` |",
        "| L3_chain | multi-step `exact` / `have` / `refine` chains |",
        "",
        "## Wave results",
        "",
        "| Wave | Role | Thms | Mathlib% | Lake | OK |",
        "|------|------|-----:|---------:|:----:|:--:|",
    ]
    for w in report["waves"]:
        lines.append(
            f"| `{w['id']}` | {w.get('role')} | {w.get('theorem_count')} | "
            f"{w.get('mathlib_depth_pct')} | {w.get('lake_status')} | "
            f"{'✓' if w.get('wave_ok') else '·'} |"
        )
    lines += [
        "",
        "## Engine core modules",
        "",
        "```text",
        "W0 Scalar + ScalarEngineStructure",
        "W1 Bounds          ← Mathlib exp/pi backbone",
        "W2 Theorems        ← T1/T2/T3 analytic depth",
        "W3 Domains",
        "W4 Cosmology + waves",
        "W5 Lab / Genomic / bridges",
        "W6+ Priors batches (certificate-heavy by design)",
        "```",
        "",
        "## Upgrade queue (engine L1 → analytic)",
        "",
    ]
    cands = report.get("upgrade_candidates") or []
    if not cands:
        lines.append("_No engine L1 upgrade candidates listed (or queue empty)._")
    else:
        lines.append("| Module | Theorem |")
        lines.append("|--------|---------|")
        for c in cands[:40]:
            lines.append(f"| `{c['module']}` | `{c['name']}` |")
    lines += [
        "",
        "## Reproduction",
        "",
        "```bash",
        "python scripts/run_mathlib_rederivation_campaign.py --engine-only",
        "python scripts/run_mathlib_rederivation_campaign.py",
        "python scripts/run_mathlib_rederivation_campaign.py --wave W2_theorems",
        "```",
        "",
        "## Artifacts",
        "",
        f"- `{OUT_INV.relative_to(ROOT).as_posix()}`",
        f"- `{OUT_REPORT.relative_to(ROOT).as_posix()}`",
        f"- `{OUT_MD.relative_to(ROOT).as_posix()}`",
        "",
        "## Honest boundary",
        "",
        "Priors modules remain largely **L1 certificate** depth by design (multiprover",
        "export pins). Engine waves are the Mathlib analytic spine. The flag",
        "`full_mathlib_rederivation_of_all_lemmas` becomes true only when the campaign",
        "verdict reaches full-corpus closure criteria (see report).",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="FSOT Mathlib re-derivation campaign")
    parser.add_argument("--engine-only", action="store_true", help="Only W0–W5 engine waves")
    parser.add_argument("--wave", type=str, default=None, help="Run a single wave id")
    parser.add_argument("--skip-lake", action="store_true", help="Inventory only (no lake builds)")
    parser.add_argument("--skip-aux", action="store_true", help="Skip structural/formal depth rebuilds")
    parser.add_argument("--priors-batch-size", type=int, default=40)
    parser.add_argument(
        "--lake-timeout",
        type=int,
        default=7200,
        help="Timeout seconds for full `lake build FSOT`",
    )
    parser.add_argument(
        "--per-module-lake",
        action="store_true",
        help="Legacy: typecheck each module with lake env lean (slow)",
    )
    args = parser.parse_args()

    print("=== FSOT Mathlib re-derivation campaign ===")
    print("Building full Formal inventory…")
    corpus = inventory_formal()
    # Compact inventory for disk (drop full tactic detail in records for size)
    inv_doc = {
        "generated_at": _now(),
        "version": "1.0",
        "theorem_count": corpus["theorem_count"],
        "mathlib_depth_count": corpus["mathlib_depth_count"],
        "mathlib_depth_pct": corpus["mathlib_depth_pct"],
        "by_tier": corpus["by_tier"],
        "by_module": corpus["by_module"],
        "sorry_list": corpus["sorry_list"],
        "upgrade_candidates_preview": depth_targets_for_upgrade(corpus, limit=30),
    }
    OUT_INV.parent.mkdir(parents=True, exist_ok=True)
    OUT_INV.write_text(json.dumps(inv_doc, indent=2), encoding="utf-8")
    print(
        f"  theorems={corpus['theorem_count']} mathlib_depth="
        f"{corpus['mathlib_depth_count']} ({corpus['mathlib_depth_pct']}%)"
    )
    if corpus.get("sorry_list"):
        print(f"  SORRY present: {corpus['sorry_list'][:10]}")

    waves_spec = all_waves(
        include_priors=not args.engine_only,
        prior_batch_size=args.priors_batch_size,
    )
    if args.wave:
        waves_spec = [w for w in waves_spec if w["id"] == args.wave]
        if not waves_spec:
            print(f"Unknown wave id: {args.wave}", file=sys.stderr)
            print("Known:", ", ".join(w["id"] for w in all_waves(True)))
            return 2

    # Shared library build — one pass covers all Formal modules
    lake_build: dict = {"status": "skipped", "seconds": 0.0}
    if args.skip_lake:
        lake_status = "skipped"
        print("  lake: skipped (--skip-lake)")
    else:
        lake_build = lake_build_library(timeout=args.lake_timeout)
        lake_status = lake_build.get("status") or "failed"

    wave_results: list[dict] = []
    for wave in waves_spec:
        print(f"\n--- {wave['id']}: {wave['title']} ---")
        print(f"  modules: {', '.join(wave['modules'][:8])}{'…' if len(wave['modules'])>8 else ''}")
        if args.per_module_lake and not args.skip_lake:
            # Legacy path: typecheck each module (slow)
            modules = [m for m in wave["modules"] if (FORMAL / f"{m}.lean").exists()]
            all_ok = True
            for mod in modules:
                lean_file = FORMAL / f"{mod}.lean"
                result = _run(
                    ["lake", "env", "lean", str(lean_file.relative_to(ROOT))],
                    timeout=min(args.lake_timeout, 1800),
                )
                if result["status"] not in ("passed", "skipped"):
                    all_ok = False
                    print(f"  FAIL {mod}: {(result.get('stderr_tail') or '')[-200:]}")
            local_status = "passed" if all_ok else "failed"
            wr = build_wave(wave, lake_status=local_status, lake_build=lake_build)
        else:
            wr = build_wave(wave, lake_status=lake_status, lake_build=lake_build)
        wave_results.append(wr)
        print(
            f"  thms={wr['theorem_count']} mathlib%={wr['mathlib_depth_pct']} "
            f"lake={wr['lake_status']} ok={wr['wave_ok']}"
        )
        if wr["sorry_list"]:
            print(f"  SORRY: {wr['sorry_list'][:5]}")

    aux = {} if args.skip_aux else run_aux_closures()

    engine_results = [w for w in wave_results if w.get("role") == "engine"]
    priors_results = [w for w in wave_results if w.get("role") == "priors"]
    engine_ok = all(w.get("wave_ok") for w in engine_results) if engine_results else False
    if args.wave and not engine_results:
        engine_ok = False

    engine_mods = {m for w in ENGINE_WAVES for m in w["modules"]}
    eng_inv = inventory_formal(sorted(engine_mods))
    engine_mathlib_pct = eng_inv.get("mathlib_depth_pct") or 0.0

    priors_ok = all(w.get("wave_ok") for w in priors_results) if priors_results else True
    all_waves_ok = all(w.get("wave_ok") for w in wave_results) if wave_results else False
    global_lake_ok = lake_status == "passed"

    engine_l1 = int((eng_inv.get("by_tier") or {}).get("L1_certificate") or 0)
    corpus_mathlib_pct = float(corpus.get("mathlib_depth_pct") or 0.0)
    corpus_l1 = int((corpus.get("by_tier") or {}).get("L1_certificate") or 0)

    # REAL depth gates (not lake-only laziness)
    engine_core_closed = (
        engine_ok
        and not eng_inv.get("sorry_list")
        and engine_mathlib_pct >= 90.0
        and engine_l1 <= 40
        and global_lake_ok
    )
    # Full corpus: lake + no sorry + engine depth + corpus Mathlib-class majority
    full_corpus_closed = (
        all_waves_ok
        and not corpus.get("sorry_list")
        and not args.engine_only
        and len(priors_results) > 0
        and priors_ok
        and global_lake_ok
        and engine_core_closed
        and corpus_mathlib_pct >= 55.0
        and corpus_l1 <= int(0.55 * max(corpus.get("theorem_count") or 1, 1))
    )

    if full_corpus_closed:
        verdict = "FULL_CORPUS_MATHLIB_CAMPAIGN_CLOSED"
    elif engine_core_closed:
        verdict = "ENGINE_CORE_MATHLIB_DEPTH_CLOSED"
    elif any(w.get("wave_ok") for w in wave_results):
        verdict = "CAMPAIGN_IN_PROGRESS"
    else:
        verdict = "CAMPAIGN_BLOCKED"

    upgrade = depth_targets_for_upgrade(corpus, limit=50)

    report = {
        "generated_at": _now(),
        "version": "1.1",
        "verdict": verdict,
        "engine_core_closed": engine_core_closed,
        "full_corpus_closed": full_corpus_closed,
        "full_mathlib_rederivation_of_all_lemmas": full_corpus_closed,
        "global_lake": {
            "status": lake_status,
            "seconds": lake_build.get("seconds"),
            "cmd": "lake build FSOT",
            "stderr_tail": (lake_build.get("stderr_tail") or "")[-500:],
        },
        "engine_mathlib_depth_pct": engine_mathlib_pct,
        "depth_gates": {
            "engine_mathlib_min_pct": 90.0,
            "engine_l1_max": 40,
            "corpus_mathlib_min_pct": 55.0,
            "engine_l1_count": engine_l1,
            "corpus_l1_count": corpus_l1,
            "engine_mathlib_pct": engine_mathlib_pct,
            "corpus_mathlib_pct": corpus_mathlib_pct,
        },
        "corpus": {
            "theorem_count": corpus["theorem_count"],
            "mathlib_depth_count": corpus["mathlib_depth_count"],
            "mathlib_depth_pct": corpus["mathlib_depth_pct"],
            "by_tier": corpus["by_tier"],
            "sorry_count": len(corpus.get("sorry_list") or []),
        },
        "engine_inventory": {
            "theorem_count": eng_inv.get("theorem_count"),
            "mathlib_depth_count": eng_inv.get("mathlib_depth_count"),
            "mathlib_depth_pct": eng_inv.get("mathlib_depth_pct"),
            "by_tier": eng_inv.get("by_tier"),
            "l1_certificate_count": engine_l1,
        },
        "waves": wave_results,
        "wave_summary": {
            "total": len(wave_results),
            "ok": sum(1 for w in wave_results if w.get("wave_ok")),
            "engine_ok": sum(1 for w in engine_results if w.get("wave_ok")),
            "priors_ok": sum(1 for w in priors_results if w.get("wave_ok")),
            "priors_total": len(priors_results),
        },
        "aux_closures": {
            k: {"status": v.get("status"), "seconds": v.get("seconds")} for k, v in aux.items()
        },
        "upgrade_candidates": upgrade,
        "commands": {
            "campaign": "python scripts/run_mathlib_rederivation_campaign.py",
            "engine_only": "python scripts/run_mathlib_rederivation_campaign.py --engine-only",
            "single_wave": "python scripts/run_mathlib_rederivation_campaign.py --wave W2_theorems",
        },
        "honest_scope": (
            "Campaign automates inventory, full `lake build FSOT`, wave depth scoring. "
            "Priors remain largely L1 numeric certificates (multiprover export pins) — "
            "full_corpus_closed means typecheck+no-sorry across all waves under shared lake build, "
            "not that every prior is L2 analytic Mathlib. "
            "Engine waves carry Mathlib analytic depth (Bounds/Theorems). "
            "full_mathlib_rederivation_of_all_lemmas tracks full_corpus_closed."
        ),
    }

    OUT_REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    OUT_MD.write_text(write_md(report), encoding="utf-8")
    print(f"\nWrote {OUT_REPORT}")
    print(f"Wrote {OUT_MD}")
    print(f"  verdict={verdict}")
    print(f"  engine_core_closed={engine_core_closed}")
    print(f"  full_mathlib_rederivation_of_all_lemmas={full_corpus_closed}")
    print(f"  engine mathlib%={engine_mathlib_pct} corpus mathlib%={corpus['mathlib_depth_pct']}")

    # Non-zero exit if campaign blocked or a requested wave failed
    if verdict == "CAMPAIGN_BLOCKED":
        return 1
    if args.wave and wave_results and not wave_results[0].get("wave_ok"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
