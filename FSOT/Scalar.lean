/-
  # FSOT.Scalar

  Core mathematical definitions and the scalar computation engine for
  Fluid Spacetime Omni-Theory (FSOT) 2.0.

  This module extracts key internal terms (`growth_term`, `quirk_mod`,
  `perceived_adjust`, `term3`) to enable clean, rigorous formal theorems.
-/

namespace FSOT

-- ============================================================
-- FUNDAMENTAL & DERIVED CONSTANTS
-- ============================================================

def phi : Float := (1.0 + Float.sqrt 5.0) / 2.0
def e : Float := Float.exp 1.0
def pi : Float := 3.141592653589793
def sqrt2 : Float := Float.sqrt 2.0
def log2 : Float := Float.log 2.0
def gamma_euler : Float := 0.5772156649015329
def catalan_G : Float := 0.9159655941772190

def alpha : Float := Float.log pi / (e * Float.pow phi 13)
def psi_con : Float := (e - 1.0) / e
def eta_eff : Float := 1.0 / (pi - 1.0)
def beta : Float := 1.0 / Float.exp (Float.pow pi pi + (e - 1.0))
def gamma : Float := -log2 / phi
def omega : Float := Float.sin (pi / e) * sqrt2
def theta_s : Float := Float.sin (psi_con * eta_eff)
def poof_factor : Float := Float.exp (- (Float.log pi / e) / (eta_eff * Float.log phi))
def acoustic_bleed : Float := Float.sin (pi / e) * phi / sqrt2
def phase_variance : Float := - Float.cos (theta_s + pi)
def coherence_efficiency : Float := (1.0 - poof_factor * Float.sin theta_s) * (1.0 + 0.01 * catalan_G / (pi * phi))
def bleed_in_factor : Float := coherence_efficiency * (1.0 - Float.sin theta_s / phi)
def acoustic_inflow : Float := acoustic_bleed * (1.0 + Float.cos theta_s / phi)
def suction_factor : Float := poof_factor * (- Float.cos (theta_s - pi))
def chaos_factor : Float := gamma / omega
def perceived_param_base : Float := gamma_euler / e
def new_perceived_param : Float := perceived_param_base * sqrt2
def consciousness_factor : Float := coherence_efficiency * new_perceived_param
def k : Float := phi * (perceived_param_base * sqrt2) / Float.log pi * 0.99

-- ============================================================
-- EXTRACTED INTERNAL TERMS (for clean theorems)
-- ============================================================

def growth_term (N recent_hits : Nat) : Float :=
  let Nf := Float.ofNat N
  let rhf := Float.ofNat recent_hits
  Float.exp (alpha * (1.0 - rhf / Nf) * gamma_euler / phi)

def quirk_mod (observed : Bool) (delta_psi phase_variance consciousness_factor : Float) : Float :=
  if observed then
    Float.exp (consciousness_factor * phase_variance) * Float.cos (delta_psi + phase_variance)
  else
    1.0

def perceived_adjust (D_eff : Nat) : Float :=
  1.0 + new_perceived_param * Float.log (Float.ofNat D_eff / 25.0)

def term3 
    (N P D_eff : Nat) 
    (delta_psi delta_theta : Float) : Float :=
  let Nf := Float.ofNat N
  let Pf := Float.ofNat P
  let Deff := Float.ofNat D_eff
  beta * Float.cos delta_psi 
    * (Nf * Pf / Float.sqrt Deff)
    * (1.0 + chaos_factor * (Deff - 25.0) / 25.0)
    * (1.0 + poof_factor * Float.cos (theta_s + pi) + suction_factor * Float.sin theta_s)
    * (1.0 + acoustic_bleed * Float.pow (Float.sin delta_theta) 2 / phi 
            + acoustic_inflow * Float.pow (Float.cos delta_theta) 2 / phi)
    * (1.0 + bleed_in_factor * phase_variance)

-- ============================================================
-- CORE RAW COMPUTATION
-- ============================================================

def compute_raw_S_D_chaotic 
    (N : Nat := 1) (P : Nat := 1) (D_eff : Nat := 25) (recent_hits : Nat := 0)
    (delta_psi : Float := 1.0) (delta_theta : Float := 1.0) (rho : Float := 1.0)
    (scale : Float := 1.0) (amplitude : Float := 1.0) (trend_bias : Float := 0.0)
    (observed : Bool := false) : Float :=
  let Nf := Float.ofNat N
  let Pf := Float.ofNat P
  let Deff := Float.ofNat D_eff
  let rhf := Float.ofNat recent_hits
  
  let gt := growth_term N recent_hits
  
  let term1 := (Nf * Pf / Float.sqrt Deff) 
               * Float.cos ((psi_con + delta_psi) / eta_eff)
               * Float.exp (-alpha * rhf / Nf + rho + bleed_in_factor * delta_psi)
               * (1.0 + gt * coherence_efficiency)
  let pa := perceived_adjust D_eff
  let term1' := term1 * pa
  let qm := quirk_mod observed delta_psi phase_variance consciousness_factor
  let term1_final := term1' * qm
  
  let term2 := scale * amplitude + trend_bias
  let t3 := term3 N P D_eff delta_psi delta_theta
  
  term1_final + term2 + t3

def compute_S_D_chaotic 
    (N : Nat := 1) (P : Nat := 1) (D_eff : Nat := 25) (recent_hits : Nat := 0)
    (delta_psi : Float := 1.0) (delta_theta : Float := 1.0) (rho : Float := 1.0)
    (scale : Float := 1.0) (amplitude : Float := 1.0) (trend_bias : Float := 0.0)
    (observed : Bool := false) : Float :=
  compute_raw_S_D_chaotic N P D_eff recent_hits delta_psi delta_theta rho scale amplitude trend_bias observed * k

-- ============================================================
-- DOMAIN MAPPINGS (aligned with Python fsot_verification_runner.py)
-- ============================================================

structure DomainParams where
  D_eff : Nat := 25
  recent_hits : Nat := 0
  delta_psi : Float := 1.0
  delta_theta : Float := 1.0
  observed : Bool := false

def defaultDomainParams : DomainParams := {}

def getDomainParams (domain : String) : DomainParams :=
  match domain with
  | "quantum"         => { D_eff := 6,  recent_hits := 0, delta_psi := 1.0,  delta_theta := 1.0, observed := true }
  | "biological"      => { D_eff := 12, recent_hits := 0, delta_psi := 0.05, delta_theta := 1.0, observed := false }
  | "astronomical"    => { D_eff := 20, recent_hits := 1, delta_psi := 1.0,  delta_theta := 1.0, observed := true }
  | "cosmological"    => { D_eff := 25, recent_hits := 0, delta_psi := 1.0,  delta_theta := 1.0, observed := false }
  | "ai_tech"         => { D_eff := 12, recent_hits := 1, delta_psi := 0.8,  delta_theta := 1.0, observed := true }
  | "engineering"     => { D_eff := 15, recent_hits := 0, delta_psi := 0.5,  delta_theta := 1.0, observed := true }
  | "physics"         => { D_eff := 8,  recent_hits := 0, delta_psi := 1.0,  delta_theta := 1.0, observed := true }
  | "chemistry"       => { D_eff := 10, recent_hits := 0, delta_psi := 0.7,  delta_theta := 1.0, observed := false }
  | "earth_science"   => { D_eff := 18, recent_hits := 1, delta_psi := 0.9,  delta_theta := 1.0, observed := true }
  | "neuroscience"    => { D_eff := 14, recent_hits := 0, delta_psi := 0.1,  delta_theta := 1.0, observed := false }
  | "economics"       => { D_eff := 16, recent_hits := 1, delta_psi := 0.6,  delta_theta := 1.0, observed := true }
  | "meteorology"     => { D_eff := 17, recent_hits := 1, delta_psi := 0.4,  delta_theta := 1.0, observed := true }
  | "oceanography"    => { D_eff := 19, recent_hits := 0, delta_psi := 0.3,  delta_theta := 1.0, observed := false }
  | "anomalies"       => { D_eff := 22, recent_hits := 2, delta_psi := 1.5,  delta_theta := 1.0, observed := true }
  | "social"          => { D_eff := 21, recent_hits := 1, delta_psi := 0.8,  delta_theta := 1.0, observed := true }
  | "planetary"       => { D_eff := 23, recent_hits := 0, delta_psi := 1.0,  delta_theta := 1.0, observed := false }
  | "nuclear"         => { D_eff := 9,  recent_hits := 0, delta_psi := 1.0,  delta_theta := 1.0, observed := true }
  | "atomic"          => { D_eff := 7,  recent_hits := 0, delta_psi := 0.9,  delta_theta := 1.0, observed := true }
  | "molecular"       => { D_eff := 11, recent_hits := 0, delta_psi := 0.6,  delta_theta := 1.0, observed := false }
  | "electromagnetic" => { D_eff := 13, recent_hits := 1, delta_psi := 1.0,  delta_theta := 1.0, observed := true }
  | _                 => defaultDomainParams

def compute_for_domain (domain_name : String) (overrides : Option DomainParams := none) : Float :=
  let base := getDomainParams domain_name
  let p := match overrides with
           | some o => { base with
               D_eff := if o.D_eff != 25 then o.D_eff else base.D_eff,
               recent_hits := if o.recent_hits != 0 then o.recent_hits else base.recent_hits,
               delta_psi := if o.delta_psi != 1.0 then o.delta_psi else base.delta_psi,
               delta_theta := if o.delta_theta != 1.0 then o.delta_theta else base.delta_theta,
               observed := if o.observed != false then o.observed else base.observed }
           | none => base
  compute_S_D_chaotic
    (D_eff := p.D_eff)
    (recent_hits := p.recent_hits)
    (delta_psi := p.delta_psi)
    (delta_theta := p.delta_theta)
    (observed := p.observed)

end FSOT
