---------------------- MODULE FSOTUniquenessResearch ----------------------
(***************************************************************************
  FSOT uniqueness research multiprover routing (TLA+).

  Fluid spacetime omni flow (no skipped gates):
    Idle → LoadFluid → CheckFluidGate
         → LoadConfinement → CheckConfinementDamp
         → LoadCalibration → CheckRealityFiction
         → Certify → Done

  Residual/structural arithmetic is Lean/Coq/Isabelle/SMT/Rust;
  this checks sector order and no illegal skips.
 ***************************************************************************)

EXTENDS Naturals

VARIABLES
  phase,
  fluidOk,
  confinementOk,
  calibrationOk,
  certified,
  stuck

Phases == {
  "Idle", "LoadFluid", "CheckFluidGate",
  "LoadConfinement", "CheckConfinementDamp",
  "LoadCalibration", "CheckRealityFiction",
  "Certify", "Done"
}

TypeOK ==
  /\ phase \in Phases
  /\ fluidOk \in BOOLEAN
  /\ confinementOk \in BOOLEAN
  /\ calibrationOk \in BOOLEAN
  /\ certified \in BOOLEAN
  /\ stuck \in BOOLEAN

Init ==
  /\ phase = "Idle"
  /\ fluidOk = FALSE
  /\ confinementOk = FALSE
  /\ calibrationOk = FALSE
  /\ certified = FALSE
  /\ stuck = FALSE

StartFluid ==
  /\ phase = "Idle"
  /\ phase' = "LoadFluid"
  /\ UNCHANGED <<fluidOk, confinementOk, calibrationOk, certified, stuck>>

GateFluid ==
  /\ phase = "LoadFluid"
  /\ phase' = "CheckFluidGate"
  /\ fluidOk' = TRUE
  /\ UNCHANGED <<confinementOk, calibrationOk, certified, stuck>>

StartConfinement ==
  /\ phase = "CheckFluidGate"
  /\ fluidOk = TRUE
  /\ phase' = "LoadConfinement"
  /\ UNCHANGED <<fluidOk, confinementOk, calibrationOk, certified, stuck>>

GateConfinement ==
  /\ phase = "LoadConfinement"
  /\ phase' = "CheckConfinementDamp"
  /\ confinementOk' = TRUE
  /\ UNCHANGED <<fluidOk, calibrationOk, certified, stuck>>

StartCalibration ==
  /\ phase = "CheckConfinementDamp"
  /\ confinementOk = TRUE
  /\ phase' = "LoadCalibration"
  /\ UNCHANGED <<fluidOk, confinementOk, calibrationOk, certified, stuck>>

GateCalibration ==
  /\ phase = "LoadCalibration"
  /\ phase' = "CheckRealityFiction"
  /\ calibrationOk' = TRUE
  /\ UNCHANGED <<fluidOk, confinementOk, certified, stuck>>

CertifyAll ==
  /\ phase = "CheckRealityFiction"
  /\ fluidOk /\ confinementOk /\ calibrationOk
  /\ phase' = "Certify"
  /\ certified' = TRUE
  /\ UNCHANGED <<fluidOk, confinementOk, calibrationOk, stuck>>

Finish ==
  /\ phase = "Certify"
  /\ certified = TRUE
  /\ phase' = "Done"
  /\ UNCHANGED <<fluidOk, confinementOk, calibrationOk, certified, stuck>>

Next ==
  \/ StartFluid \/ GateFluid
  \/ StartConfinement \/ GateConfinement
  \/ StartCalibration \/ GateCalibration
  \/ CertifyAll \/ Finish

Spec == Init /\ [][Next]_<<phase, fluidOk, confinementOk, calibrationOk, certified, stuck>>

InvType == TypeOK
InvNotStuck == stuck = FALSE
InvDoneImpliesAll ==
  (phase = "Done") => (fluidOk /\ confinementOk /\ calibrationOk /\ certified)

=============================================================================
