# FSOT FORMAL VERIFICATION PROTOCOL (v1.1)
# Project: fsot QWEN 3VL_Formal_Env

## 1. The Golden Rule: NO PROBABILISTIC MATH
The model is FORBIDDEN from presenting any mathematical derivation, constant mapping, or theorem as "correct" or "final" based on text generation alone.

## 2. The Verification Chain (Autonomous Loop)
The agent must operate in a self-correcting loop:
1. **Reasoning Trace**: Output a detailed `REASONING_TRACE` explaining the mathematical approach.
2. **Formalization**: Translate the hypothesis into a formal Lean 4 theorem/proof.
3. **Execution & Test**: Run the proof through the `lean_bridge.py` tool. **THE AGENT MUST RUN THIS.**
4. **Self-Correction**: If `status: failed`, the agent must treat this as a hard stop. It must analyze the compiler error, refine the reasoning, and re-attempt.
5. **Certification**: An output is only "Certified" when the bridge returns `status: verified`.

## 3. No-Exit Condition
The agent shall not report a task as "complete" to the user until:
- The code has been executed and verified by the compiler.
- Any logical holes identified by Lean have been closed.
- The result is mathematically consistent with the `S_REP` base.

## 4. Output Standard
All certified results must be presented as:
---
**CERTIFIED FSOT DERIVATION**
- **Reasoning Trace**: [Step-by-step logic]
- **Lean Proof**: [The code used in the bridge]
- **Verification**: [The specific success message from Lean]
- **Result**: [The final proven value/relation]
---

## 5. Precision Requirement
All constants must be used to the maximum precision available in `C:\Users\damia\Desktop\FSOTLean\FSOTLean\FSOT\Formal\Constants.lean`. Any approximation is considered a failure of the protocol.
