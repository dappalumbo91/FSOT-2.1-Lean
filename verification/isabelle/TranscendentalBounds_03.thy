(* FSOT Tier 83 — transcendental bounds chunk 4/4 (generated). *)
theory TranscendentalBounds_03
imports TranscendentalBoundsCert
begin

lemma exp_1253_gt_34: "(3.4 :: real) < exp (1.253 :: real)"
  by (rule certified_exp_1253_gt_34)

end
