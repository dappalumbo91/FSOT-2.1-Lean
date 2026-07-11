#!/usr/bin/env python3
"""Generate Isabelle native (non-axiom) proofs for certified pi/e base intervals."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "verification" / "isabelle" / "TranscendentalBoundsNative.thy"


def generate() -> str:
    return """\
(* FSOT Tier 83 — native Isabelle proofs for pi/e base intervals (no axioms). *)
theory TranscendentalBoundsNative
imports "HOL-Decision_Procs.Approximation"
begin

lemma certified_exp_one_lo: "2.7182818283 < exp (1::real)"
  by (approximation 50)

lemma certified_exp_one_hi: "exp (1::real) < 2.7182818286"
  by (approximation 50)

lemma certified_pi_lo: "3.14159265358979323846 < pi"
  by (approximation 80)

lemma certified_pi_hi: "pi < 3.14159265358979323847"
  by (approximation 80)

end
"""


def main() -> int:
    OUT.write_text(generate(), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())