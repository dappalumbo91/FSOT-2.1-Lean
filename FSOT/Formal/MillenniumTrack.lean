/-
  FSOT Millennium Prize *track* — process rules + native identities.

  This module does NOT claim a Clay Prize.
  Clay rules (CMI Board 26 Sep 2018): no direct submission; Qualifying Outlet
  + two years + general acceptance before CMI will consider a solution.
  https://www.claymath.org/millennium-problems/rules/

  Native identities below are the FSOT objects on the same physical questions.
  Clay statements stay OPEN_NOT_CLAIMED until those exact theorems are proved.

  Accuracy vs public SOTA is a *separate* Python scoreboard
  (`vendor/fsot_millennium_accuracy.py`). That contest is not a Prize claim.
  Glueball vs Teper is allowed to lose. ECMWF is not beaten.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum

namespace FSOT.Formal.MillenniumTrack

noncomputable section

open Real

/-- Six remaining Clay problems (Poincaré solved by Perelman). -/
def clay_problems_remaining : ℕ := 6

theorem clay_problems_remaining_eq : clay_problems_remaining = 6 := by
  unfold clay_problems_remaining; decide

/-- CMI does not accept direct submission of proposed solutions. -/
def clay_direct_submit_accepted : ℕ := 0

theorem clay_no_direct_submit : clay_direct_submit_accepted = 0 := by
  unfold clay_direct_submit_accepted; decide

/-- Two years must elapse after Qualifying Outlet publication. -/
def clay_wait_years : ℕ := 2

theorem clay_wait_years_eq : clay_wait_years = 2 := by
  unfold clay_wait_years; decide

/-- Prize not awarded on this track. Honest. -/
def clay_prize_awarded : ℕ := 0

theorem clay_prize_not_awarded : clay_prize_awarded = 0 := by
  unfold clay_prize_awarded; decide

/-- Poincaré is the solved Millennium problem (historical; not an FSOT proof). -/
def poincare_solved_historical : ℕ := 1

theorem poincare_solved_historical_eq : poincare_solved_historical = 1 := by
  unfold poincare_solved_historical; decide

/-- Grover query-complexity exponent 1/2. Not a P vs NP theorem. -/
def grover_exponent : ℝ := 1 / 2

theorem grover_exponent_eq_half : grover_exponent = (1 / 2 : ℝ) := by
  unfold grover_exponent; norm_num

/-- Critical line Re = 1/2 as a *named goal*, not a proof that all zeros lie there. -/
def riemann_critical_line : ℝ := 1 / 2

theorem riemann_critical_line_eq_half : riemann_critical_line = (1 / 2 : ℝ) := by
  unfold riemann_critical_line; norm_num

end

end FSOT.Formal.MillenniumTrack
