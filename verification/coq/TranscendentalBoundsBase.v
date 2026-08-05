(* FSOT Tier 83 — transcendental base: Native Interval + Cert re-exports. *)
From Stdlib Require Import Reals.
From Stdlib Require Import Psatz.
Require Import TranscendentalBoundsNative.
Require Import TranscendentalBoundsCert.
Local Open Scope R_scope.

Lemma nonzero_03 : (0.3%R) <> 0.
Proof. lra. Qed.
