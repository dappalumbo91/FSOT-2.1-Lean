# FSOT path-sum — native path integral

**Pin:** D1D38A · Lean: `FSOT/Formal/UniquenessAttractor.lean` (`poof_hold`, `path_sum2`)  
**Python:** `vendor/fsot_path_sum.py`

The path integral **in this model** is a sum over discrete process-time branches
(cell POOF, transfer, quiet hold) with seed-split weights

\[
w_{\mathrm{POOF}}=\frac{\mathrm{POOF}}{\mathrm{POOF}+|\mathrm{SUCTION}|},\qquad
w_{\mathrm{hold}}=1-w_{\mathrm{POOF}}
\]

then \(\kappa_{ij}\) among tanks. Dated-forecast `frozen_potentials` already
emits that sum (weights = 1).

The continuum Yang–Mills *measure* uniqueness theorem is a **different object**.
It stays `OPEN_NOT_CLAIMED` until that exact statement is machine-checked.
What that prize problem actually is: [`MILLENNIUM_YM_VS_FSOT.md`](MILLENNIUM_YM_VS_FSOT.md).
Working the native path-sum is how we do the path-integral job here.

| Check | Meaning |
|-------|---------|
| P1 | \(w_{\mathrm{POOF}}+w_{\mathrm{hold}}=1\) |
| P3 | Loading potentials sum to 1 |
| P4 | \(\int_0^\infty a_0 e^{-\gamma t}\,dt=a_0/\gamma\) finite (\(\gamma_{\mathrm{color}}>0\)) |
| P5 | Area-law identity \(V(1/\sqrt{\sigma})=\sqrt{\sigma}\) |
| P6 | \(\Lambda_{\mathrm{QCD}}\) proxy \(>0\) |

Run: `python vendor/fsot_path_sum.py`

Forbidden: “we proved the Millennium YM mass-gap theorem.” Allowed: free-color
histories integrate and damp; singlets persist; valve branches sum to one.
