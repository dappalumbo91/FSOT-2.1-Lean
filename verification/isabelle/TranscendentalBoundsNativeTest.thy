theory TranscendentalBoundsNativeTest
imports Complex_Main "HOL-Computational_Algebra.More_Computational_Algebra"
begin

lemma certified_exp_one_lo: "2.7182818283 < exp (1::real)"
  by (approximation 40)

lemma certified_exp_one_hi: "exp (1::real) < 2.7182818286"
  by (approximation 40)

lemma certified_pi_lo: "3.14159265358979323846 < pi"
  by (approximation 40)

lemma certified_pi_hi: "pi < 3.14159265358979323847"
  by (approximation 40)

end