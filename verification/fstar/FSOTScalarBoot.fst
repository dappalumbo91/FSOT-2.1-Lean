module FSOTScalarBoot

open FStar.Real
open FSOTScalarKernel

#push-options "--max_fuel 1 --max_ifuel 1"

/// Universal scaling constant is positive.
let k_positive () : Lemma (k_fsot >. 0.0R) =
  ()

/// Canonical boot scalar is positive.
let boot_scalar_canonical_positive () : Lemma (boot_scalar_canonical >. 0.0R) =
  ()

/// Boot parameters match rust_lean_bridge_summary.json.
let boot_params_match_summary () : Lemma (
  boot_d_eff == 8.0R /\ boot_delta_psi == 0.7R /\ boot_recent_hits == 0.0R
) =
  ()

/// Verified readout — canonical oracle (Rust/Python f64 at POC params).
let boot_scalar () : real =
  boot_scalar_canonical

let boot_scalar_positive () : Lemma (boot_scalar () >. 0.0R) =
  boot_scalar_canonical_positive ()

let boot_scalar_matches_canonical () : Lemma (boot_scalar () == boot_scalar_canonical) =
  ()

#pop-options