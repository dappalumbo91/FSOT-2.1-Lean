---------------------------- MODULE FSOTGRSMCKM ----------------------------
(***************************************************************************
  FSOT GR / SM / CKM / PMNS multi-sector routing flow (TLA+).

  Models the *order* of formal layers:
    Idle → LoadGR → CheckGRGate → LoadSM → CheckSMGate
         → LoadCKM → CheckCKMUnitarity → LoadPMNS → CheckPMNS
         → Certify → Done

  Residual arithmetic is Lean/Coq/Isabelle/SMT/Rust; this checks no skipped
  gates and no illegal transitions between sectors.
 ***************************************************************************)

EXTENDS Naturals

VARIABLES
  phase,
  grOk,
  smOk,
  ckmOk,
  pmnsOk,
  certified,
  stuck

Phases == {
  "Idle", "LoadGR", "CheckGRGate",
  "LoadSM", "CheckSMGate",
  "LoadCKM", "CheckCKMUnitarity",
  "LoadPMNS", "CheckPMNS",
  "Certify", "Done"
}

TypeOK ==
  /\ phase \in Phases
  /\ grOk \in BOOLEAN
  /\ smOk \in BOOLEAN
  /\ ckmOk \in BOOLEAN
  /\ pmnsOk \in BOOLEAN
  /\ certified \in BOOLEAN
  /\ stuck \in BOOLEAN

Init ==
  /\ phase = "Idle"
  /\ grOk = FALSE
  /\ smOk = FALSE
  /\ ckmOk = FALSE
  /\ pmnsOk = FALSE
  /\ certified = FALSE
  /\ stuck = FALSE

StartGR ==
  /\ phase = "Idle"
  /\ phase' = "LoadGR"
  /\ UNCHANGED <<grOk, smOk, ckmOk, pmnsOk, certified, stuck>>

GateGR ==
  /\ phase = "LoadGR"
  /\ phase' = "CheckGRGate"
  /\ grOk' = TRUE
  /\ UNCHANGED <<smOk, ckmOk, pmnsOk, certified, stuck>>

StartSM ==
  /\ phase = "CheckGRGate"
  /\ grOk = TRUE
  /\ phase' = "LoadSM"
  /\ UNCHANGED <<grOk, smOk, ckmOk, pmnsOk, certified, stuck>>

GateSM ==
  /\ phase = "LoadSM"
  /\ phase' = "CheckSMGate"
  /\ smOk' = TRUE
  /\ UNCHANGED <<grOk, ckmOk, pmnsOk, certified, stuck>>

StartCKM ==
  /\ phase = "CheckSMGate"
  /\ smOk = TRUE
  /\ phase' = "LoadCKM"
  /\ UNCHANGED <<grOk, smOk, ckmOk, pmnsOk, certified, stuck>>

GateCKM ==
  /\ phase = "LoadCKM"
  /\ phase' = "CheckCKMUnitarity"
  /\ ckmOk' = TRUE
  /\ UNCHANGED <<grOk, smOk, pmnsOk, certified, stuck>>

StartPMNS ==
  /\ phase = "CheckCKMUnitarity"
  /\ ckmOk = TRUE
  /\ phase' = "LoadPMNS"
  /\ UNCHANGED <<grOk, smOk, ckmOk, pmnsOk, certified, stuck>>

GatePMNS ==
  /\ phase = "LoadPMNS"
  /\ phase' = "CheckPMNS"
  /\ pmnsOk' = TRUE
  /\ UNCHANGED <<grOk, smOk, ckmOk, certified, stuck>>

CertifyAll ==
  /\ phase = "CheckPMNS"
  /\ grOk /\ smOk /\ ckmOk /\ pmnsOk
  /\ phase' = "Certify"
  /\ certified' = TRUE
  /\ UNCHANGED <<grOk, smOk, ckmOk, pmnsOk, stuck>>

Finish ==
  /\ phase = "Certify"
  /\ certified = TRUE
  /\ phase' = "Done"
  /\ UNCHANGED <<grOk, smOk, ckmOk, pmnsOk, certified, stuck>>

\* Illegal skip would set stuck — no such actions defined.
Next ==
  \/ StartGR \/ GateGR
  \/ StartSM \/ GateSM
  \/ StartCKM \/ GateCKM
  \/ StartPMNS \/ GatePMNS
  \/ CertifyAll \/ Finish

Spec == Init /\ [][Next]_<<phase, grOk, smOk, ckmOk, pmnsOk, certified, stuck>>

InvType == TypeOK
InvNotStuck == stuck = FALSE
InvDoneImpliesAll ==
  (phase = "Done") => (grOk /\ smOk /\ ckmOk /\ pmnsOk /\ certified)

=============================================================================
