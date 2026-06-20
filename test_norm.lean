import Mathlib
example : (0.466942299689 : Real) < 1 / (2.14159265358979323847 : Real) := by norm_num
example : (1 / (2.14159265358979323846 : Real)) < (0.466942299692 : Real) := by norm_num
example : (0.6321205588 : Real) * (0.466942299689 : Real) < (0.295164 : Real) := by norm_num
example : (0.63212055884 : Real) * (0.466942299692 : Real) < (0.295164 : Real) := by norm_num
example : (0.62600 : Real) * (1.6695 : Real) < (1.0455 : Real) := by norm_num
