(* FSOT Tier 83 — transcendental base intervals via Cert axioms. *)
(* Isabelle uses TranscendentalBoundsNative.thy; Coq uses Cert (Rocq 9 lra/PI gap). *)
From Stdlib Require Import Reals.
From Stdlib Require Import Psatz.
Require Import TranscendentalBoundsCert.
Local Open Scope R_scope.

Lemma nonzero_03 : (0.3%R) <> 0.
Proof. lra. Qed.
