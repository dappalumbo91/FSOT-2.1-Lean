import math
from domain_scalar_oracle import *

for name, p in DOMAINS.items():
    qm = quirk_mod(p)
    adj = 1 + NEW_PERCEIVED_PARAM * math.log(p.D_eff / 25)
    t1b = term1_base(p)
    exp_part = math.exp(CONSCIOUSNESS_FACTOR * PHASE_VARIANCE)
    cos_part = math.cos(p.delta_psi + PHASE_VARIANCE)
    t1 = term1(p)
    rs = raw_S(p)
    print(f"{name}: t1b={t1b:.6f} adj={adj:.6f} qm={qm:.6f} t1={t1:.6f} raw_S={rs:.6f}")
    if p.observed:
        print(f"  exp={exp_part:.6f} cos={cos_part:.6f} pv={PHASE_VARIANCE:.6f}")