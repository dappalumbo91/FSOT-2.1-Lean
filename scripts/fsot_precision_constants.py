"""FSOT official precision gates — single source of truth for audits and Lean bounds."""

from __future__ import annotations

# Official manifest gate (was legacy 5.0% loose GREEN; tightened to strict band).
MAX_MEDIAN_ERROR_PCT = 0.5

# Max material scalar prediction error per domain.
MAX_SCALAR_ERROR_PCT = 0.5

# Tier aspiration band (~0.02% pooled median standard).
TIER_SCALAR_MAX_ERROR_PCT = 0.05

# Binary classifiers: accuracy floor (complement of 0.5% misclass rate).
MIN_CLASSIFIER_ACCURACY_PCT = 99.5

# Lean theorem bound literal (ℝ).
LEAN_MEDIAN_BOUND = 0.5

# Deprecated legacy loose gate — retained for sota baseline comparisons only.
LEGACY_LOOSE_GATE_PCT = 5.0

# Benchmark stubs excluded from margin audit (non-v1.1 material panels).
AUDIT_EXCLUDED_BENCHMARKS = frozenset(
    {
        "structure_calibration_benchmark.json",
        # toe_ckm_pmns + toe_gr_sm_deep re-included once seed NLO + ultra-subtle
        # net_mod closed all PDG comparison residuals under the ≤0.5% green gate.
    }
)