(* FSOT Tier 83 — transcendental base intervals via Cert axioms. *)
(* Isabelle uses TranscendentalBoundsNative.thy; Coq uses Cert (Rocq 9 lra/PI gap). *)
Require Import TranscendentalBoundsCert.

Lemma nonzero_03 : (0.3%R) <> 0.
Proof. lra. Qed.
