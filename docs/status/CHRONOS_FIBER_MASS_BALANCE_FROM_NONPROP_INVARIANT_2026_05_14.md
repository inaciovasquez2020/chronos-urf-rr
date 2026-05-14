# Chronos Lake-Native FiberMassBalance From NonProp Invariant

Status: LAKE_NATIVE_FIBER_MASS_BALANCE_FROM_NONPROP_INVARIANT_CLOSED.

Closed theorems:

```lean
theorem fiberMassBalance_from_nonprop_invariant
    (I : NonPropFinalCarrierInvariant) :
    FiberMassBalanceFromNonProp I
theorem countingFiberSeparation_and_fiberMassBalance_from_nonprop_invariant
    (I : NonPropFinalCarrierInvariant) :
    CountingFiberSeparationFromNonProp I ∧ FiberMassBalanceFromNonProp I
Boundary:
Lake-native fiber-mass-balance theorem only.
Does not prove UniversalFiberEntropyGap.
Does not prove Chronos-RR closure.
Does not prove H4.1/FGL closure.
Does not prove P vs NP closure.
Does not prove any Clay-problem closure.
