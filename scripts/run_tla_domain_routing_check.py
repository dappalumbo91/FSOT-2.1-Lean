#!/usr/bin/env python3
"""TLA+ domain-routing / preregistered-fold state-flow check.

Role: model-check *execution flow* (no deadlocks, no gate skips), not residual
arithmetic. TLC is used when installed; otherwise a faithful Python explorer
enumerates the same transition system defined in
verification/tla/FSOTDomainRouting.tla.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TLA_DIR = ROOT / "verification" / "tla"
TLA_FILE = TLA_DIR / "FSOTDomainRouting.tla"
REPORT = ROOT / "data" / "tla_domain_routing_report.json"
MAX_DOMAINS = 3  # small finite model for exhaustive exploration


@dataclass(frozen=True)
class State:
    phase: str
    domains_left: int
    fold_active: bool
    residual_ready: bool
    gate_passed: bool
    certified: int
    stuck: bool


PHASES = {
    "Idle",
    "LoadDomain",
    "ApplyFold",
    "MeasureResidual",
    "GateCheck",
    "Certify",
    "Done",
}


def type_ok(s: State) -> bool:
    return (
        s.phase in PHASES
        and 0 <= s.domains_left <= MAX_DOMAINS
        and 0 <= s.certified <= MAX_DOMAINS
        and isinstance(s.fold_active, bool)
        and isinstance(s.residual_ready, bool)
        and isinstance(s.gate_passed, bool)
        and isinstance(s.stuck, bool)
    )


def inv(s: State) -> bool:
    if not type_ok(s):
        return False
    if s.stuck:
        return False
    if s.certified > MAX_DOMAINS:
        return False
    if s.phase == "Done" and s.domains_left != 0:
        return False
    if s.phase == "Done" and s.certified != MAX_DOMAINS:
        return False
    if s.fold_active and s.phase not in {
        "ApplyFold",
        "MeasureResidual",
        "GateCheck",
        "Certify",
    }:
        return False
    return True


def successors(s: State) -> list[State]:
    out: list[State] = []
    # StartLoad
    if s.phase == "Idle" and s.domains_left > 0:
        out.append(
            State("LoadDomain", s.domains_left, s.fold_active, s.residual_ready, s.gate_passed, s.certified, s.stuck)
        )
    # ApplyPreregisteredFold
    if s.phase == "LoadDomain":
        out.append(State("ApplyFold", s.domains_left, True, False, False, s.certified, s.stuck))
    # Measure
    if s.phase == "ApplyFold" and s.fold_active:
        out.append(State("MeasureResidual", s.domains_left, s.fold_active, True, s.gate_passed, s.certified, s.stuck))
    # CheckGate (legal green path only in safety model)
    if s.phase == "MeasureResidual" and s.residual_ready:
        out.append(State("GateCheck", s.domains_left, s.fold_active, s.residual_ready, True, s.certified, s.stuck))
    # IllegalCertify — model includes the bad transition; Inv forbids reaching stuck=True
    if s.phase == "GateCheck" and not s.gate_passed:
        out.append(
            State(s.phase, s.domains_left, s.fold_active, s.residual_ready, s.gate_passed, s.certified, True)
        )
    # CertifyDomain
    if s.phase == "GateCheck" and s.gate_passed and s.residual_ready and s.fold_active:
        out.append(
            State(
                "Certify",
                s.domains_left - 1,
                False,
                False,
                False,
                s.certified + 1,
                s.stuck,
            )
        )
    # NextDomainOrDone
    if s.phase == "Certify":
        if s.domains_left > 0:
            out.append(
                State("Idle", s.domains_left, s.fold_active, s.residual_ready, s.gate_passed, s.certified, s.stuck)
            )
        else:
            out.append(
                State("Done", s.domains_left, s.fold_active, s.residual_ready, s.gate_passed, s.certified, s.stuck)
            )
    # DoneStutter
    if s.phase == "Done":
        out.append(s)
    return out


def explore() -> dict:
    init = State("Idle", MAX_DOMAINS, False, False, False, 0, False)
    seen: set[State] = set()
    stack = [init]
    violations: list[str] = []
    transitions = 0
    reached_done = False

    while stack:
        s = stack.pop()
        if s in seen:
            continue
        seen.add(s)
        if not inv(s):
            violations.append(f"Inv broken at {s}")
            continue
        if s.phase == "Done":
            reached_done = True
        for t in successors(s):
            transitions += 1
            if t not in seen:
                stack.append(t)

    # Reachability: Done must be reachable for MaxDomains
    if not reached_done:
        violations.append("Done phase never reached")

    # Deadlock check: every non-Done state must have a successor; Done may stutter
    for s in seen:
        succs = successors(s)
        if s.phase != "Done" and not succs:
            violations.append(f"deadlock at {s}")
        if s.stuck:
            violations.append(f"stuck state reachable: {s}")

    ok = not violations
    return {
        "status": "passed" if ok else "failed",
        "states_explored": len(seen),
        "transitions_fired": transitions,
        "max_domains": MAX_DOMAINS,
        "reached_done": reached_done,
        "violations": violations[:20],
        "engine": "python_state_explorer",
    }


def try_tlc() -> dict | None:
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        from tool_path_lib import find_tla2tools_jar  # noqa: WPS433
    except Exception:
        find_tla2tools_jar = lambda: None  # type: ignore

    jar = find_tla2tools_jar()
    tlc = shutil.which("tlc") or shutil.which("tlc.exe") or shutil.which("tlc.cmd")
    cfg = TLA_DIR / "FSOTDomainRouting.cfg"
    try:
        if jar and Path(jar).exists():
            cmd = ["java", "-cp", jar, "tlc2.TLC", "-config", str(cfg), "FSOTDomainRouting"]
            engine = "tlc_jar"
        elif tlc:
            cmd = [tlc, "-config", str(cfg), "FSOTDomainRouting"]
            engine = "tlc"
        else:
            return None
        r = subprocess.run(cmd, cwd=str(TLA_DIR), capture_output=True, text=True, timeout=180)
        text = (r.stdout or "") + (r.stderr or "")
        low = text.lower()
        # TLC prints "Model checking completed. No error has been found."
        ok = r.returncode == 0 and (
            "no error has been found" in low
            or ("error" not in low and "exception" not in low)
        )
        return {
            "status": "passed" if ok else "failed",
            "engine": engine,
            "returncode": r.returncode,
            "stdout_tail": text[-1200:],
        }
    except Exception as e:
        return {"status": "failed", "engine": "tlc", "reason": str(e)}


def main() -> int:
    if not TLA_FILE.exists():
        report = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "missing_spec",
            "overall_ok": False,
        }
        REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return 1

    tlc = try_tlc()
    py = explore()
    # Python explorer is the required offline gate; TLC is bonus when present
    overall = py["status"] == "passed"
    if tlc is not None:
        overall = overall and tlc.get("status") == "passed"

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "purpose": "TLA+ model of domain-routing / preregistered-fold state flow",
        "spec": str(TLA_FILE.relative_to(ROOT)).replace("\\", "/"),
        "python_explorer": py,
        "tlc": tlc,
        "status": "passed" if overall else "failed",
        "overall_ok": overall,
        "invariants_checked": [
            "TypeOK",
            "NeverStuck",
            "CertifiedBound",
            "DoneMeansComplete",
            "no_deadlock_nonterminal",
        ],
        "role": (
            "Ensures preregistered-fold / domain-routing scripts cannot skip residual gates "
            "or deadlock. Complements Lean/SMT arithmetic; does not replace residual math."
        ),
        "note": "Install TLC for independent model checking; Python explorer is always run.",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(
        f"TLA domain routing: {report['status']} "
        f"(states={py['states_explored']}, engine={py['engine']}"
        f"{', tlc=' + tlc['status'] if tlc else ', tlc=not_installed'})"
    )
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
