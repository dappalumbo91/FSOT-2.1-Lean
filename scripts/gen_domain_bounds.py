#!/usr/bin/env python3
"""Generate conservative interval bounds for domain sign proofs."""
import math
from domain_scalar_oracle import *

# Tight intervals from canonical_constants + margin
MARGIN = 0.002

def perceived_adj_bounds(D):
    lo = 1 + 0.3000 * math.log(D / 25)
    hi = 1 + 0.3010 * math.log(D / 25)
    return lo, hi

print("=== perceived_adjust bounds ===")
for D in [6,7,8,9,11,13,14,16,20,21,23,24]:
    lo, hi = perceived_adj_bounds(D)
    print(f"D={D}: lo={lo:.6f} hi={hi:.6f}")

print("\n=== quirkMod cos arg bounds (delta_psi + phase_variance) ===")
pv_lo, pv_hi = 0.955, 0.961
for dp in [0.35, 0.5, 0.6, 0.7, 0.85, 0.9, 0.95, 1.0, 1.15, 1.25]:
    arg_lo = dp + pv_lo
    arg_hi = dp + pv_hi
    cos_lo = math.cos(arg_hi)
    cos_hi = math.cos(arg_lo)
    print(f"dp={dp}: cos in [{cos_lo:.6f}, {cos_hi:.6f}]")

print("\n=== exp(consciousness_factor * phase_variance) ===")
cf_lo, cf_hi = 0.287, 0.288
for pv in [pv_lo, pv_hi]:
    pass
exp_lo = math.exp(cf_lo * pv_lo)
exp_hi = math.exp(cf_hi * pv_hi)
print(f"exp in [{exp_lo:.6f}, {exp_hi:.6f}]")

print("\n=== term1_base magnitude targets ===")
for name, p in DOMAINS.items():
    lo, hi = perceived_adj_bounds(p.D_eff)
    t1b = term1_base(p)
    if p.observed:
        qm = quirk_mod(p)
        # conservative qm bounds
        print(f"{name}: t1b={t1b:.4f} need t1 {'> -0.8' if raw_S(p)>0 else '< -0.8'} actual t1={term1(p):.4f}")
    else:
        t1_lo = t1b * hi  # base neg, adj pos
        t1_hi = t1b * lo
        print(f"{name}: t1b={t1b:.4f} t1 in [{t1_lo:.4f},{t1_hi:.4f}]")

print("\n=== cos((psi_con+delta_psi)/eta) - need sign ===")
for dp in [0.5, 0.8]:
    arg = (PSI_CON + dp) / ETA_EFF
    print(f"dp={dp}: arg={arg:.4f} cos={math.cos(arg):.4f}")