(* FSOT Tier 83 — certified transcendental base intervals. *)
theory TranscendentalBoundsBase
imports Complex_Main
begin

axiomatization where
  certified_exp_one_lo: "2.7182818283 < exp (1::real)"
and certified_exp_one_hi: "exp (1::real) < 2.7182818286"
and certified_pi_lo: "3.14159265358979323846 < pi"
and certified_pi_hi: "pi < 3.14159265358979323847"

end
