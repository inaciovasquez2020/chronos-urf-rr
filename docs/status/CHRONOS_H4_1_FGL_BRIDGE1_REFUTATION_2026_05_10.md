# Chronos H4.1/FGL Bridge 1 Refutation — 2026-05-10

Status: **BRIDGE_1_REFUTED**

## Refuted bridge

```lean
∀ C : ChronosCarrierData,
  RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily C →
  FinalCarrierDomain C
Witness
def zeroArityCarrier : ChronosCarrierData :=
  { arity := 0, stratum := 0, index := 0 }
The witness is real-admissible because ChronosRegistry.registered := fun _ => True.
The witness is not in FinalCarrierDomain because:
FinalCarrierDomain C := PositiveArityCarrier C
PositiveArityCarrier C :=
  RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily C ∧
  C.arity ≠ 0
For the witness, C.arity = 0.
Consequence
The unrestricted H4.1/FGL route cannot use:
RealChronosAdmissiblePredicate C → FinalCarrierDomain C
under current definitions.
Boundary
No unrestricted H4.1/FGL closure.
No UniversalFiberEntropyGap theorem.
No Chronos-RR closure.
No P vs NP or Clay-problem closure.
